"""Sampler for discrete-space occult events"""

from typing import NamedTuple, Tuple
from warnings import warn

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

from gemlib.mcmc.discrete_time_state_transition_model.right_censored_events_proposal import (  # noqa:E501
    add_occult_proposal,
    del_occult_proposal,
)

tfd = tfp.distributions

__all__ = ["UncalibratedOccultUpdate"]


PROB_DIRECTION = 0.5


class OccultKernelResults(NamedTuple):
    log_acceptance_correction: float
    target_log_prob: float
    m: int
    t: int
    delta_t: int
    x_star: int
    seed: Tuple[int, int]


def _nonzero_rows(m):
    return tf.cast(tf.reduce_sum(m, axis=-1) > 0.0, m.dtype)


def _maybe_expand_dims(x):
    """If x is a scalar, give it at least 1 dimension"""
    x = tf.convert_to_tensor(x)
    if x.shape == ():
        return tf.expand_dims(x, axis=0)
    return x


def _add_events(events, m, t, x, x_star):
    """Adds `x_star` events to metapopulation `m`,
    time `t`, transition `x` in `events`.
    """
    x = _maybe_expand_dims(x)
    indices = tf.stack([m, t, x], axis=-1)
    return tf.tensor_scatter_nd_add(events, indices, x_star)


class UncalibratedOccultUpdate(tfp.mcmc.TransitionKernel):
    """UncalibratedOccultUpdate"""

    def __init__(
        self,
        target_log_prob_fn,
        topology,
        cumulative_event_offset,
        nmax,
        t_range=None,
        name=None,
    ):
        """An uncalibrated random walk for event times.
        :param target_log_prob_fn: the log density of the target distribution
        :param target_event_id: the position in the last dimension of the events
                                tensor that we wish to move
        :param t_range: a tuple containing earliest and latest times between
                         which to update occults.
        :param seed: a random seed
        :param name: the name of the update step
        """
        self._name = name or "uncalibrated_occult_update"
        self._parameters = {
            "target_log_prob_fn": target_log_prob_fn,
            "topology": topology,
            "cumulative_event_offset": cumulative_event_offset,
            "nmax": nmax,
            "t_range": t_range,
            "name": name,
        }
        self.tx_topology = topology
        self.initial_state = cumulative_event_offset
        self._dtype = self.initial_state.dtype

    @property
    def target_log_prob_fn(self):
        return self._parameters["target_log_prob_fn"]

    @property
    def target_event_id(self):
        return self._parameters["topology"]["target_transition"]

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
        :param current_events: a [M, T, X] tensor containing number of events
                               per time t, metapopulation m,
                               and transition x.
        :param previous_kernel_results: an object of type
                                        UncalibratedRandomWalkResults.
        :returns: a tuple containing new_state and UncalibratedRandomWalkResults
        """
        with tf.name_scope("occult_rw/onestep"):
            seed = samplers.sanitize_seed(seed, salt="occult_rw")
            proposal_seed, add_del_seed = samplers.split_seed(seed)

            if mcmc_util.is_list_like(current_events):
                step_events = current_events[0]
                warn(
                    "Batched updating of occults is not supported.",
                    stacklevel=2,
                )
            else:
                step_events = current_events

            def add_occult_fn():
                with tf.name_scope("true_fn"):
                    proposal = add_occult_proposal(
                        events=step_events,
                        topology=self.tx_topology,
                        initial_state=self.initial_state,
                        n_max=self.parameters["nmax"],
                        t_range=self.parameters["t_range"],
                        name=self.name,
                    )
                    update = proposal.sample(seed=proposal_seed)
                    next_state = _add_events(
                        events=step_events,
                        m=update["m"],
                        t=update["t"],
                        x=self.tx_topology.target,
                        x_star=tf.cast(update["x_star"], step_events.dtype),
                    )
                    reverse = del_occult_proposal(
                        events=next_state,
                        topology=self.tx_topology,
                        initial_state=self.initial_state,
                        t_range=self.parameters["t_range"],
                        n_max=self.parameters["nmax"],
                    )
                    q_fwd = tf.reduce_sum(proposal.log_prob(update))
                    q_rev = tf.reduce_sum(reverse.log_prob(update))
                    log_acceptance_correction = q_rev - q_fwd

                return (
                    update,
                    next_state,
                    log_acceptance_correction,
                    tf.ones(1, dtype=tf.int32),
                )

            def del_occult_fn():
                with tf.name_scope("false_fn"):
                    proposal = del_occult_proposal(
                        events=step_events,
                        topology=self.tx_topology,
                        initial_state=self.initial_state,
                        t_range=self.parameters["t_range"],
                        n_max=self.parameters["nmax"],
                    )
                    update = proposal.sample(seed=proposal_seed)
                    next_state = _add_events(
                        events=step_events,
                        m=update["m"],
                        t=update["t"],
                        x=[self.tx_topology.target],
                        x_star=tf.cast(-update["x_star"], step_events.dtype),
                    )
                    reverse = add_occult_proposal(
                        events=next_state,
                        topology=self.tx_topology,
                        initial_state=self.initial_state,
                        n_max=self.parameters["nmax"],
                        t_range=self.parameters["t_range"],
                        name=f"{self.name}rev",
                    )
                    q_fwd = tf.reduce_sum(proposal.log_prob(update))
                    q_rev = tf.reduce_sum(reverse.log_prob(update))
                    log_acceptance_correction = q_rev - q_fwd

                return (
                    update,
                    next_state,
                    log_acceptance_correction,
                    -tf.ones(1, dtype=tf.int32),
                )

            u = tfd.Uniform().sample(seed=add_del_seed)
            delta, next_state, log_acceptance_correction, direction = tf.cond(
                (u < PROB_DIRECTION)
                & (
                    tf.math.count_nonzero(
                        step_events[..., self.tx_topology.target]
                    )
                    > 0
                ),
                del_occult_fn,
                add_occult_fn,
            )

            next_target_log_prob = self.target_log_prob_fn(next_state)

            if mcmc_util.is_list_like(current_events):
                next_state = [next_state]

            return [
                next_state,
                OccultKernelResults(
                    log_acceptance_correction=log_acceptance_correction,
                    target_log_prob=next_target_log_prob,
                    m=delta["m"],
                    t=delta["t"],
                    delta_t=direction,
                    x_star=delta["x_star"],
                    seed=add_del_seed,
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
            return OccultKernelResults(
                log_acceptance_correction=tf.constant(
                    0.0, dtype=init_target_log_prob.dtype
                ),
                target_log_prob=init_target_log_prob,
                m=tf.zeros([1], dtype=tf.int32),
                t=tf.zeros([1], dtype=tf.int32),
                delta_t=tf.zeros([1], dtype=tf.int32),
                x_star=tf.zeros([1], dtype=tf.int32),
                seed=samplers.zeros_seed(),
            )
