"""Implementation of Metropolis-within-Gibbs framework"""

from collections import ChainMap, namedtuple
from typing import AnyStr, Callable, List, Optional, Tuple

import tensorflow_probability as tfp

from .mcmc_base import (
    ChainState,
    KernelInfo,
    KernelState,
    Position,
    SamplingAlgorithm,
)

split_seed = tfp.random.split_seed

__all__ = ["Step"]


def _maybe_list(x):
    if isinstance(x, list):
        return x
    return [x]


def _project_position(
    position: Position, varnames: List[AnyStr]
) -> Tuple[Position, Position]:
    """Splits `position` into `position[varnames]` and
    `position[~varnames]`
    """
    if varnames is None:
        return (position, ())

    target = {k: v for k, v in position._asdict().items() if k in varnames}
    target_compl = {
        k: v for k, v in position._asdict().items() if k not in varnames
    }

    return (
        namedtuple("Target", target.keys())(**target),
        namedtuple("TargetCompl", target_compl.keys())(**target_compl),
    )


def _join_dicts(a: dict, b: dict):
    """Joins two dictionaries `a` and `b`"""
    return dict(ChainMap(a, b))


def _maybe_flatten(x: List):
    """Flatten a list if `len(x) <= 1`"""
    if len(x) == 0:
        return None
    if len(x) == 1:
        return x[0]
    return x


class KernelInitMonad:
    """KernelInitMonad is a Writer monad allowing us to build an initial
    state tuple for a Metropolis-within-Gibbs algorithm
    """

    def __init__(self, fn: SamplingAlgorithm):
        """The monad 'unit' function"""
        self.__fn = fn

    def __call__(self, *args, **kwargs):
        """Monad ``run'' function"""
        return self.__fn(*args, **kwargs)

    def fish(self, next_kernel):
        """Monad combination, i.e. Haskell fish operator"""

        @KernelInitMonad
        def compound_init_fn(
            target_log_prob_fn: Callable[[Position], float],
            initial_position: ChainState,
        ):
            _, self_kernel_state = self(target_log_prob_fn, initial_position)
            next_chain_state, next_kernel_state = next_kernel(
                target_log_prob_fn, initial_position
            )

            return (
                next_chain_state,
                _maybe_list(self_kernel_state) + _maybe_list(next_kernel_state),
            )

        return compound_init_fn

    def __rshift__(self, next_kernel):
        return self.fish(next_kernel)


class KernelStepMonad:
    """StepMonad is a state monad that allows us to chain MCMC kernels
    together.
    """

    def __init__(self, fn: SamplingAlgorithm):
        """The monad 'unit' function"""
        self.__fn = fn  # Make private

    def __call__(self, *args, **kwargs):
        """Apply the state transformer computation to a state."""
        return self.__fn(*args, **kwargs)

    def __rshift__(self, next_kernel_fn):
        """The monad 'bind' operator which allows chaining.
        ma >> f :: ma -> (a -> mb) -> mb
        """

        def compound_step_kernel(
            target_log_prob_fn: Callable[[Position], float],
            chain_and_kernel_state: Tuple[ChainState, KernelState],
            seed,
        ):
            first_seed, second_seed = split_seed(seed)
            # Pre-order recursive descent
            chain_state, kernel_state = chain_and_kernel_state

            self_kernel_state = kernel_state[:-1]
            next_kernel_state = kernel_state[-1]

            # Execute self kernel step
            (chain_state, self_kernel_state), self_info = self.__fn(
                target_log_prob_fn,
                (chain_state, _maybe_flatten(self_kernel_state)),
                seed=first_seed,
            )

            # Descend right hand branch
            (chain_state, next_kernel_state), next_info = next_kernel_fn(
                target_log_prob_fn,
                (chain_state, next_kernel_state),
                seed=second_seed,
            )

            return (
                (
                    chain_state,
                    _maybe_list(self_kernel_state)
                    + _maybe_list(next_kernel_state),
                ),
                self_info + next_info,
            )

        return KernelStepMonad(compound_step_kernel)


class ComposableSamplingAlgorithm:
    """ComposableSamplingAlgorithm implements a Metropolis-within-Gibbs step"""

    def __init__(self, init: KernelInitMonad, step: KernelStepMonad):
        self.__initialize = init
        self.__step = step

    @property
    def init(self):
        """Initialize an MCMC chain"""
        return self.__initialize

    @property
    def step(self):
        """Function to invoke the MCMC kernel"""
        return self.__step

    def __rshift__(self, rhs):
        """Combinator"""
        return ComposableSamplingAlgorithm(
            init=self.init >> rhs.init, step=self.step >> rhs.step
        )


class Step:  # pylint: disable=too-few-public-methods
    """A Metropolis-within-Gibbs step"""

    def __new__(
        cls,
        sampling_algorithm: SamplingAlgorithm,
        target_names: Optional[List[str]] = None,
        step_kwargs_fn: Callable[[Position], dict] = lambda _: {},
    ):
        """Transforms a base kernel to operate on a substate of a Markov chain.

        Args:
        ----
        sampling_algorithm: a named tuple containing the generic kernel `init`
                            and `step` function.
        target_log_prob_fn: a list of variable names on which the
                            Metropolis-within-Gibbs step is to operate
        step_kwargs_fn: a callable taking the chain position as an argument,
                        and returning a dictionary of extra kwargs to
                        `sampling_algorithm.step`.

        Returns:
        -------
        A monad of type StepMonad (State -> (State, Info))

        """

        @KernelInitMonad
        def init(
            target_log_prob_fn: Callable[[Position], float],
            initial_position: Position,
        ):
            target, target_compl = _project_position(
                initial_position, target_names
            )

            def conditional_tlp(*args):
                state = _join_dicts(
                    dict(zip(target._fields, args)),
                    target_compl._asdict(),
                )
                return target_log_prob_fn(**state)

            kernel_state = sampling_algorithm.init(conditional_tlp, target)

            chain_state = ChainState(
                position=initial_position,
                log_density=kernel_state[0].log_density,
                log_density_grad=kernel_state[0].log_density_grad,
            )

            return chain_state, kernel_state[1]

        @KernelStepMonad
        def step(
            target_log_prob_fn: Callable[[Position], float],
            chain_and_kernel_state: Tuple[ChainState, KernelState],
            seed,
        ) -> Tuple[Tuple[ChainState, KernelState], KernelInfo]:
            chain_state, kernel_state = chain_and_kernel_state

            # Split global state and generate conditional density
            target, target_compl = _project_position(
                chain_state.position, target_names
            )

            # Calculate the conditional log density
            def conditional_tlp(*args):
                state = _join_dicts(
                    dict(zip(target._fields, args)),
                    target_compl._asdict(),
                )
                return target_log_prob_fn(**state)

            # Invoke the kernel on the target state
            (new_target, new_kernel_state), info = sampling_algorithm.step(
                conditional_tlp,
                (chain_state._replace(position=target), kernel_state),
                seed,
                **step_kwargs_fn(chain_state.position),
            )

            # Stitch the global position back together
            new_global_position = chain_state.position.__class__(
                **new_target.position._asdict(), **target_compl._asdict()
            )
            new_global_state = new_target._replace(
                position=new_global_position,
            )

            return (new_global_state, new_kernel_state), info

        return ComposableSamplingAlgorithm(init, step)
