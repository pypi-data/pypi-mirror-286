"""Move partially-censored events in DiscreteTimeStateTransitionModel"""

from typing import NamedTuple

import tensorflow_probability as tfp

from gemlib.mcmc.discrete_time_state_transition_model import (
    TransitionTopology,
    UncalibratedEventTimesUpdate,
)
from gemlib.mcmc.experimental.mcmc_base import ChainState, SamplingAlgorithm


class MoveEventsState(NamedTuple):
    dmax: int
    mmax: int
    nmax: int


class MoveEventsInfo(NamedTuple):
    is_accepted: bool


def move_events(topology: TransitionTopology, dmax, mmax, nmax):
    def _build_kernel(target_log_prob_fn, initial_conditions):
        return tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedEventTimesUpdate(
                target_log_prob_fn,
                topology,
                initial_conditions,
                dmax,
                mmax,
                nmax,
            )
        )

    def init_fn(target_log_prob_fn, target_state, initial_conditions):
        kernel = _build_kernel(target_log_prob_fn, initial_conditions)
        results = kernel.bootstrap_results(target_state)
        chain_state = ChainState(
            position=target_state,
            log_density=results.accepted_results.target_log_prob,
        )
        kernel_state = MoveEventsState(dmax=dmax, mmax=mmax, nmax=nmax)

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

        return new_chain_and_kernel_state, MoveEventsInfo(results.is_accepted)

    return SamplingAlgorithm(init_fn, step_fn)
