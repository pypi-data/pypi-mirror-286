"""Describes a DiscreteTimeStateTransitionModel."""

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    dtype_util,
    reparameterization,
    samplers,
)

from gemlib.distributions.discrete_markov import (
    compute_state,
    discrete_markov_log_prob,
    discrete_markov_simulation,
)
from gemlib.util import batch_gather, transition_coords

Tensor = tf.Tensor
tla = tf.linalg
tfd = tfp.distributions


class DiscreteTimeStateTransitionModel(tfd.Distribution):
    """Discrete-time state transition model

    A discrete-time state transition model assumes a population of
    individuals is divided into a number of mutually exclusive states,
    where transitions between states occur according to a Markov process.
    Such models are commonly found in epidemiological and ecological
    applications, where rapid implementation and modification is necessary.

    This class provides a programmable implementation of the discrete-time
    state transition model, compatible with TensorFlow Probability.
    """

    def __init__(
        self,
        transition_rates,
        incidence_matrix,
        initial_state,
        initial_step,
        time_delta,
        num_steps,
        validate_args=False,
        allow_nan_stats=True,
        name="DiscreteTimeStateTransitionModel",
    ):
        """A discrete-time Markov jump process for a state transition model.

        Args:
        ----
          transition_rates: Python callable of the form `fn(t, state)` taking
            the current time `t` (Python float) and state tensor `state`. This
            function returns a tensor which broadcasts to the first dimension of
            `incidence_matrix`.
          incidence_matrix: `Tensor` representing the stochiometry matrix for
            the state transition model where rows represent the transitions and
            columns states.
          initial_state: `Tensor` representing an initial state of counts per
            compartment.  The inner dimension is equal to the first dimension
            of `incidence_matrix`.
          initial_step: Python float representing an offset giving the time `t`
            of the first time step in the model.
          time_delta: Python float representing the size of the time step to be
                      used.
          num_steps: Python integer representing the number of time steps across
             which the model runs.


        Example:
        -------
          A homogeneously mixing SIR model implementation::

            import tensorflow as tf
            from gemlib.distributions.discrete_time_state_transition_model \
              import (
                DiscreteTimeStateTransitionModel
            )
            from gemlib.util import compute_state

            dtype = tf.float32

            # Initial state, counts per compartment (S, I, R), for one
            #   population
            initial_state = tf.constant([[99, 1, 0]], dtype)

            # incidence_matrix              S->I, I->R,
            incidence_matrix = tf.constant([[-1, 0], # S
                                            [1,-1],  # I
                                            [0,1]],  # R

                                        dtype)

            # time parameters
            initial_step, time_delta, num_steps = 0.0, 1.0, 100

            def txrates(t, state):
                # Transition rate per individual corresponding to each row of
                # the incidence matrix.
                #
                # state: `Tensor` representing the current state (count of
                #        individuals in each compartment).
                # t: Python float representing the current time. For example
                #        seasonality in the S->I
                #    transition could be driven by tensors of the following form
                #        seasonality = tf.math.sin(2 * 3.14159 * t / 20) + 1
                #        si = seasonality * beta * state[:, 1] / tf.reduce_sum(
                #                                                         state)
                #
                # Returns: List of `Tensor`(s) each of which corresponds to a
                #          transition.

                beta, gamma = 0.28, 0.14  # note R0=beta/gamma
                si = beta * state[:, 1] / tf.reduce_sum(state)
                ir = tf.constant([gamma], dtype)
                return [si, ir]

            # Instantiate model
            sir = DiscreteTimeStateTransitionModel(
                    transition_rates=txrates,
                    incidence_matrix=incidence_matrix,
                    initial_state=initial_state,
                    initial_step=initial_step,
                    time_delta=time_delta,
                    num_steps=num_steps,
            )

            # One realisation of the epidemic process
            @tf.function
            def simulate_one(elems):
            return sir.sample()

            nsim = 15  # Number of realisations of the epidemic process
            eventlist = tf.map_fn(simulate_one,
                                  tf.ones([nsim, incidence_matrix.shape[0]]),
                                  fn_output_signature=dtype)

            # Events for each transition with shape (simulation, population,
            #     time, transition)
            print('I->R events:', eventlist[0, 0, :, 1])

            # Log prob of observing the eventlist, of first simulation, given
            #     the model
            print('Log prob:', sir.log_prob(eventlist[0, ...]))

            # Timeseries of counts per state with shape (simulation, population,
            #  time, state)
            state_timeseries = compute_state(
                initial_state,
                eventlist,
                incidence_matrix,
            )
            print('Susceptible state counts for first simulation:',
                  state_timeseries[0, 0, :, 0])

        Note:
        ----
          See http://gitlab.com/gem-epidemics/gemlib/distributions/discrete_time_state_transition_model_examples.py
          for further examples.

        """
        parameters = dict(locals())
        with tf.name_scope(name) as name:
            self._transition_rates = transition_rates
            self._incidence_matrix = tf.convert_to_tensor(
                incidence_matrix, dtype=initial_state.dtype
            )
            self._source_states = _compute_source_states(incidence_matrix)
            self._initial_state = initial_state
            self._initial_step = initial_step
            self._time_delta = time_delta
            self._num_steps = num_steps

            super().__init__(
                dtype=initial_state.dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                parameters=parameters,
                name=name,
            )

        self.dtype = initial_state.dtype

    @property
    def transition_rates(self):
        return self._transition_rates

    @property
    def incidence_matrix(self):
        return self._incidence_matrix

    @property
    def initial_state(self):
        return self._initial_state

    @property
    def initial_step(self):
        return self._initial_step

    @property
    def source_states(self):
        return self._source_states

    @property
    def time_delta(self):
        return self._time_delta

    @property
    def num_steps(self):
        return self._num_steps

    def _batch_shape(self):
        return tf.TensorShape([])

    def _event_shape(self):
        shape = tf.TensorShape(
            [
                self.initial_state.shape[0],
                tf.get_static_value(self._num_steps),
                self._incidence_matrix.shape[1],
            ]
        )
        return shape

    def compute_state(
        self, events: Tensor, include_final_state: bool = False
    ) -> Tensor:
        """Computes a state timeseries given a transition events

        Args
        ----
            events: a `[self.num_steps, self.num_steps, self.num_events]`
                    shaped tensor of events
            include_final_state: should the result include the final state?  If
                                 `False` (default), then `result.shape[1] ==
                                 events.shape[1]`.  If `True`, then
                                 `results.shape[1] == events.shape[1]  + 1`.

        Returns
        -------
            A tensor of shape `[self.num_meta, self.num_steps, self.num_states]`
            giving the number of individuals in each state at each time point in
             each unit.
        """
        return compute_state(
            incidence_matrix=self.incidence_matrix,
            initial_state=self.initial_state,
            events=events,
            closed=include_final_state,
        )

    def _sample_n(self, n, seed=None):
        """Runs a simulation from the epidemic model

        :param param: a dictionary of model parameters
        :param state_init: the initial state
        :returns: a tuple of times and simulated states.
        """
        seed = samplers.sanitize_seed(
            seed, salt="DiscreteTimeStateTransitionModel"
        )
        t, sim = discrete_markov_simulation(
            hazard_fn=self.transition_rates,
            state=self.initial_state,
            start=self.initial_step,
            end=self.initial_step + self.num_steps * self.time_delta,
            time_step=self.time_delta,
            incidence_matrix=self.incidence_matrix,
            seed=seed,
        )

        # `sim` is `[T, M, S, S]`, and we need to pick out
        # elements `[..., i, j]` for all our relevant transitions
        # `i->j`.  `batch_gather` computes these coordinates and
        # invokes tf.gather.
        indices = transition_coords(self.incidence_matrix)
        sim = batch_gather(sim, indices)

        # `sim` is now `[T, M, R]` structure for T times,
        # M population units, and R transitions.
        sim = tf.transpose(sim, perm=(1, 0, 2))
        return tf.expand_dims(sim, 0)

    def _log_prob(self, y, **kwargs):
        dtype = dtype_util.common_dtype(
            [y, self.initial_state], dtype_hint=self.dtype
        )
        y = tf.convert_to_tensor(y, dtype)

        hazard = self.transition_rates
        return discrete_markov_log_prob(
            events=y,
            init_state=self.initial_state,
            init_step=self.initial_step,
            time_delta=self.time_delta,
            hazard_fn=hazard,
            incidence_matrix=self.incidence_matrix,
        )


def _compute_source_states(incidence_matrix, dtype=tf.int32):
    """Computes the indices of the source states for each
       transition in a state transition model.

    :param incidence_matrix: incidence matrix in `[S, R]` orientation
                          for `S` states and `R` transitions.
    :returns: a tensor of shape `(R,)` containing source state indices.
    """
    incidence_matrix = tf.transpose(incidence_matrix)

    source_states = tf.reduce_sum(
        tf.cumsum(
            tf.clip_by_value(
                -incidence_matrix, clip_value_min=0, clip_value_max=1
            ),
            axis=-1,
            reverse=True,
            exclusive=True,
        ),
        axis=-1,
    )

    return tf.cast(source_states, dtype)
