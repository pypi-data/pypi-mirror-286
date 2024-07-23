"""Constrained Event Move kernel for DiscreteTimeStateTransitionModel"""

from typing import Callable, List, NamedTuple
from warnings import warn

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

from gemlib.mcmc.experimental.mcmc_base import (
    Position,
)

from .event_time_proposal import (
    filtered_event_time_proposal,
)
from .util import TransitionTopology

tfd = tfp.distributions

__all__ = ["UncalibratedEventTimesUpdate"]


class EventTimesKernelResults(NamedTuple):
    log_acceptance_correction: float
    target_log_prob: float
    m: int
    t: int
    delta_t: int
    x_star: int
    seed: List[int]


def _is_within(x, low, high):
    """Returns true if low <= x < high"""
    return tf.logical_and(tf.less_equal(low, x), tf.less(x, high))


def _nonzero_rows(m):
    return tf.cast(tf.reduce_sum(m, axis=-1) > 0.0, m.dtype)


def _move_events(event_tensor, event_id, m, from_t, to_t, n_move):
    """Subtracts n_move from event_tensor[m, from_t, event_id]
    and adds n_move to event_tensor[m, to_t, event_id].

    :param event_tensor: shape [M, T, X]
    :param event_id: the event id to move
    :param m: the metapopulation to move
    :param from_t: the move-from time
    :param to_t: the move-to time
    :param n_move: the number of events to move
    :return: the modified event_tensor
    """
    # Todo rationalise this -- compute a delta, and add once.
    indices = tf.stack(
        [m, from_t, tf.broadcast_to(event_id, m.shape)],
        axis=-1,  # All meta-populations
    )  # Event
    # Subtract x_star from the [from_t, :, event_id] row of the state tensor
    n_move = tf.cast(n_move, event_tensor.dtype)
    new_state = tf.tensor_scatter_nd_sub(event_tensor, indices, n_move)
    indices = tf.stack([m, to_t, tf.broadcast_to(event_id, m.shape)], axis=-1)
    # Add x_star to the [to_t, :, event_id] row of the state tensor
    new_state = tf.tensor_scatter_nd_add(new_state, indices, n_move)
    return new_state


def _reverse_move(move):
    move["t"] = move["t"] + move["delta_t"]
    move["delta_t"] = -move["delta_t"]
    return move


class UncalibratedEventTimesUpdate(tfp.mcmc.TransitionKernel):
    """UncalibratedEventTimesUpdate"""

    def __init__(
        self,
        target_log_prob_fn: Callable[[Position], float],
        topology: TransitionTopology,
        initial_state: tf.Tensor,
        dmax: float,
        mmax: float,
        nmax: int,
        name: str = None,
    ):
        """An uncalibrated random walk for event times.
        :param target_log_prob_fn: the log density of the target distribution
        :param target_event_id: the position in the first dimension of the
                                events tensor that we wish to move
        :param prev_event_id: the position of the previous event in the events
                              tensor
        :param next_event_id: the position of the next event in the events
                              tensor
        :param initial_state: the initial state tensor
        :param seed: a random seed
        :param name: the name of the update step
        """
        self._name = name
        self._parameters = {
            "target_log_prob_fn": target_log_prob_fn,
            "topology": topology,
            "initial_state": initial_state,
            "dmax": dmax,
            "mmax": mmax,
            "nmax": nmax,
            "name": name,
        }
        self.time_offsets = tf.range(self.parameters["dmax"])
        self._dtype = initial_state.dtype

    @property
    def target_log_prob_fn(self):
        return self._parameters["target_log_prob_fn"]

    @property
    def topology(self):
        return self._parameters["topology"]

    @property
    def seed(self):
        return self._parameters["seed"]

    @property
    def name(self):
        return self._parameters["name"]

    @property
    def parameters(self):
        """Return `dict` of ``__init__`` arguments and their values."""
        return self._parameters

    @property
    def is_calibrated(self):
        return False

    def one_step(self, current_events, previous_kernel_results, seed=None):
        """One update of event times.
        :param current_events: a [T, M, X] tensor containing number of events
                               per time t, metapopulation m,
                               and transition x.
        :param previous_kernel_results: an object of type
                                        UncalibratedRandomWalkResults.
        :returns: a tuple containing new_state and UncalibratedRandomWalkResults
        """
        with tf.name_scope("uncalibrated_event_times_rw/onestep"):
            seed = samplers.sanitize_seed(
                seed, salt="uncalibrated_event_times_rw"
            )

            step_events = current_events
            if mcmc_util.is_list_like(current_events):
                step_events = current_events[0]
                warn(
                    "Batched event times updates are not supported.  Using \
first event item only.",
                    stacklevel=2,
                )

            proposal = filtered_event_time_proposal(
                events=step_events,
                initial_state=self.parameters["initial_state"],
                topology=self.topology,
                m_max=self.parameters["mmax"],
                d_max=self.parameters["dmax"],
                n_max=self.parameters["nmax"],
                name=self.name,
            )
            update = proposal.sample(seed=seed)

            move = update["move"]
            to_t = move["t"] + move["delta_t"]

            # Prob of fwd move
            q_fwd = proposal.log_prob(update)

            # Propagate state
            next_state = _move_events(
                event_tensor=step_events,
                event_id=self.topology.target,
                m=update["m"],
                from_t=move["t"],
                to_t=to_t,
                n_move=move["x_star"],
            )

            next_target_log_prob = self.target_log_prob_fn(next_state)

            # Calculate proposal mass ratio
            rev_move = _reverse_move(move.copy())
            rev_update = {"m": update["m"], "move": rev_move}
            Q_rev = filtered_event_time_proposal(
                events=next_state,
                initial_state=self.parameters["initial_state"],
                topology=self.topology,
                m_max=self.parameters["mmax"],
                d_max=self.parameters["dmax"],
                n_max=self.parameters["nmax"],
            )

            # Prob of reverse move and q-ratio
            q_rev = Q_rev.log_prob(rev_update)
            log_acceptance_correction = tf.reduce_sum(q_rev - q_fwd)

            if mcmc_util.is_list_like(current_events):
                next_state = [next_state]

            return [
                next_state,
                EventTimesKernelResults(
                    log_acceptance_correction=log_acceptance_correction,
                    target_log_prob=next_target_log_prob,
                    m=update["m"],
                    t=update["move"]["t"],
                    delta_t=update["move"]["delta_t"],
                    x_star=update["move"]["x_star"],
                    seed=seed,
                ),
            ]

    def bootstrap_results(self, init_state):
        with tf.name_scope("uncalibrated_event_times_rw/bootstrap_results"):
            if not mcmc_util.is_list_like(init_state):
                init_state = [init_state]
            init_state = [
                tf.convert_to_tensor(x, dtype=self._dtype) for x in init_state
            ]
            init_target_log_prob = self.target_log_prob_fn(*init_state)
            return EventTimesKernelResults(
                log_acceptance_correction=tf.zeros_like(init_target_log_prob),
                target_log_prob=init_target_log_prob,
                m=tf.zeros(self.parameters["mmax"], dtype=tf.int32),
                t=tf.zeros(self.parameters["mmax"], dtype=tf.int32),
                delta_t=tf.zeros(self.parameters["mmax"], dtype=tf.int32),
                x_star=tf.zeros(self.parameters["mmax"], dtype=tf.int32),
                seed=samplers.zeros_seed(),
            )
