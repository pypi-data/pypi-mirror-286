"""Right-censored events MCMC kernel for DiscreteTimeStateTransitionModel"""

from typing import NamedTuple, Optional, Tuple

import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.discrete_time_state_transition_model import (
    TransitionTopology,
    UncalibratedOccultUpdate,
)
from gemlib.mcmc.experimental.mcmc_base import ChainState, SamplingAlgorithm


class RightCensoredEventsState(NamedTuple):
    nmax: int
    t_range: Tuple[int, int]


class RightCensoredEventsInfo(NamedTuple):
    is_accepted: bool
    m: int
    t: int
    delta: int
    x_star: int
    proposed_state: tf.Tensor
    seed: Tuple[int, int]


def right_censored_events_mh(
    topology: TransitionTopology,
    nmax: int = 1,
    t_range: Optional[Tuple[int, int]] = None,
    name: Optional[str] = None,
):
    def _build_kernel(target_log_prob_fn, initial_conditions):
        return tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedOccultUpdate(
                target_log_prob_fn,
                topology,
                initial_conditions,
                nmax,
                t_range,
                name,
            ),
        )

    def init_fn(target_log_prob_fn, target_state, initial_conditions):
        kernel = _build_kernel(target_log_prob_fn, initial_conditions)
        results = kernel.bootstrap_results(target_state)
        chain_state = ChainState(
            position=target_state,
            log_density=results.accepted_results.target_log_prob,
        )
        kernel_state = RightCensoredEventsState(nmax=nmax, t_range=t_range)

        return chain_state, kernel_state

    def step_fn(
        target_log_prob_fn, target_and_kernel_state, seed, initial_conditions
    ):
        kernel = _build_kernel(target_log_prob_fn, initial_conditions)
        target_chain_state, kernel_state = target_and_kernel_state

        new_target_position, results = kernel.one_step(
            target_chain_state.position,
            kernel.bootstrap_results(target_chain_state.position),
            seed=seed,
        )

        new_chain_and_kernel_state = (
            ChainState(
                position=new_target_position,
                log_density=results.accepted_results.target_log_prob,
            ),
            kernel_state,
        )

        return new_chain_and_kernel_state, RightCensoredEventsInfo(
            results.is_accepted,
            m=results.proposed_results.m,
            t=results.proposed_results.t,
            delta=results.proposed_results.delta_t,
            x_star=results.proposed_results.x_star,
            proposed_state=results.proposed_state,
            seed=seed,
        )

    return SamplingAlgorithm(init_fn, step_fn)
