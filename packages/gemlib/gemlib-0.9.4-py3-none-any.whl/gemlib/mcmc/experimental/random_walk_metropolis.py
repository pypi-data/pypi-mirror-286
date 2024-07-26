"""Implementation of the Random Walk Metropolis algorithm"""

from typing import Callable, NamedTuple, Tuple

import tensorflow_probability as tfp

from .mcmc_base import ChainState, SamplingAlgorithm


class RwmhInfo(NamedTuple):
    """Represents the information about a random walk Metropolis-Hastings (RWMH)
      step.
    This can be expanded to include more information in the future (as needed
      for a specific kernel).

    Attributes
    ----------
        is_accepted (bool): Indicates whether the proposal was accepted or not.

    """

    is_accepted: bool


class RwmhKernelState(NamedTuple):
    """Represents the kernel state of an arbitrary MCMC kernel.

    Attributes
    ----------
        scale (float): The scale parameter for the RWMH kernel.

    """

    scale: float


def rwmh(scale=1.0):
    def _build_kernel(log_prob_fn):
        """Partial"""
        return tfp.mcmc.RandomWalkMetropolis(
            target_log_prob_fn=log_prob_fn,
            new_state_fn=tfp.mcmc.random_walk_normal_fn(scale=scale),
        )

    def init_fn(target_log_prob_fn, target_state):
        kernel = _build_kernel(target_log_prob_fn)
        results = kernel.bootstrap_results(target_state)

        chain_state = ChainState(
            position=target_state,
            log_density=results.accepted_results.target_log_prob,
            log_density_grad=(),
        )
        kernel_state = RwmhKernelState(scale=scale)

        return chain_state, kernel_state

    def step_fn(
        target_log_prob_fn: Callable[[NamedTuple], float],
        target_and_kernel_state: Tuple[ChainState, RwmhKernelState],
        seed,
    ) -> Callable[[ChainState], Tuple[ChainState, RwmhInfo]]:
        """Computation that calls a kernel.

        Args:
        ----
        target_log_prob_fn: the conditional log target density/mass function
        conditioned_state: Parts of the global state that are not updated by
                           the kernel, but may be needed to instantiate it.
        chain_and_kernel_state: a tuple containing a ChainState object and
                        kernel-specific state.
        target_state: the sub-state on which the kernel operates.

        Returns:
        -------
        a tuple of the new target sub-state and information about the sampler

        """
        # This could be replaced with BlackJAX easily
        kernel = _build_kernel(target_log_prob_fn)

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
                log_density_grad=(),
            ),
            kernel_state,
        )

        info = (
            RwmhInfo(
                results.is_accepted,
            ),
        )

        return new_chain_and_kernel_state, info

    return SamplingAlgorithm(init_fn, step_fn)
