"""Continuous time state transition model"""

from typing import Callable, Optional

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import reparameterization

from gemlib.distributions.continuous_markov import (
    EpidemicEvent,
    compute_state,
    continuous_markov_simulation,
    continuous_time_log_likelihood,
)

# aliasing for convenience
tfd = tfp.distributions
Tensor = tf.Tensor
DTYPE = tf.float32


class ContinuousTimeStateTransitionModel(tfd.Distribution):
    """Continuous time state transition model."""

    def __init__(
        self,
        transition_rate_fn: Callable[[Tensor], Tensor],
        incidence_matrix: Tensor,
        initial_state: Tensor,
        num_events: int,
        initial_time: Optional[float] = 0.0,
        validate_args: Optional[bool] = False,
        allow_nan_stats: Optional[bool] = True,
        name: Optional[str] = "ContinuousTimeStateTransitionModel",
    ) -> None:
        """
        Initializes a ContinuousTimeStateTransitionModel object.

        Args:
            transition_rate_fn: Python callable of the form `fn(t, state)`
                                taking the current time `t: float` and state
                                tensor `state`, and returning a tuple of tensors
                                containing transition rates between states.
            incidence_matrix: Matrix representing the incidence of transitions
                              between states.
            initial_state: A `[N, S]` tensor containing the initial state of the
                           population of `N` individuals in `S` epidemiological
                           classes.
            num_events: the number of events to simulate
            initial_time: Initial time of the model. Defaults to 0.0.
            name: Name of the model. Defaults to
                  "ContinuousTimeStateTransitionModel".
        """
        parameters = dict(locals())

        self._incidence_matrix = tf.convert_to_tensor(incidence_matrix)
        self._initial_state = tf.convert_to_tensor(initial_state)
        self._initial_time = tf.convert_to_tensor(initial_time)

        super().__init__(
            dtype=self._incidence_matrix.dtype,
            reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            parameters=parameters,
            name=name,
        )

    @property
    def transition_rate_fn(self):
        """Transition rate function for the model."""
        return self._parameters["transition_rate_fn"]

    @property
    def incidence_matrix(self):
        """Incidence matrix for the model."""
        return self._parameters["incidence_matrix"]

    @property
    def initial_state(self):
        """Initial state of the model."""
        return self._parameters["initial_state"]

    @property
    def num_events(self):
        """Number of events to simulate."""
        return self._parameters["num_events"]

    @property
    def initial_time(self):
        """Initial wall clock for the model. Sets the time scale."""
        return self._parameters["initial_time"]

    def compute_state(
        self, event_list: EpidemicEvent, include_final_state: bool = False
    ) -> Tensor:
        """Given an event list `event_list`, compute a timeseries
           of state given the model.

        Args
        ----
            event_list: the event list, assumed to be sorted by time.
            include_final_state: should the final state be included in the
                returned timeseries?  If `True`, then the time dimension of
                the returned tensor will be 1 greater than the length of the
                event list.  If `False` (default) these will be equal.

        Return
        ------
        A `[T, N, S]` tensor where `T` is the number of events, `N` is the
        number of individuals, and `S` is the number of states.
        """
        return compute_state(
            self.incidence_matrix,
            self.initial_state,
            event_list,
            include_final_state,
        )

    # Bypass the reshaping that tfd.Distribution._call_sample_n does
    def _call_sample_n(self, sample_shape, seed) -> EpidemicEvent:
        return self._sample_n(sample_shape, seed)

    def _sample_n(self, sample_shape: int, seed=None) -> EpidemicEvent:
        """
        Samples n outcomes from the continuous time state transition model.

        Args:
            n (int): The number of realisations of the Markov process to sample
                     (currently ignored).
            seed (int, optional): The seed value for random number generation.
                                  Defaults to None.

        Returns:
            EpidemicEvent: A list of n outcomes sampled from the continuous time
                           state transition model.
        """

        outcome = continuous_markov_simulation(
            transition_rate_fn=self.transition_rate_fn,
            incidence_matrix=self._incidence_matrix,
            initial_state=self._initial_state,
            initial_time=self._initial_time,
            num_markov_jumps=self.num_events,
            seed=seed,
        )

        return outcome

    def log_prob(self, value: EpidemicEvent) -> float:
        return self._log_prob(value)

    def _log_prob(self, value: EpidemicEvent) -> float:
        """
        Computes the log probability of the given outcomes.

        Args:
            value (EpidemicEvent): an EpidemicEvent object representing the
                                   outcomes.

        Returns:
            float: The log probability of the given outcomes.
        """
        log_lik = continuous_time_log_likelihood(
            transition_rate_fn=self.transition_rate_fn,
            incidence_matrix=self.incidence_matrix,
            initial_state=self.initial_state,
            initial_time=self.initial_time,
            num_jumps=self.num_events,
            event_list=value,
        )

        return log_lik

    def _event_shape_tensor(self) -> Tensor:
        return tf.constant([self.num_events], dtype=tf.int32)

    def _event_shape(self) -> tf.TensorShape:
        return tf.TensorShape([self.num_events])

    def _batch_shape_tensor(self) -> Tensor:
        return tf.constant([])

    def _batch_shape(self) -> tf.TensorShape:
        return tf.TensorShape([])
