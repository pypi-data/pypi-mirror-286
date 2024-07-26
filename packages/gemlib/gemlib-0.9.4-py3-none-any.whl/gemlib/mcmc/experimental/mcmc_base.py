"""Base MCMC datatypes"""

from typing import Callable, NamedTuple, Optional, Tuple

Position = NamedTuple
KernelInfo = NamedTuple


class ChainState(NamedTuple):
    """Represent the state of an MCMC probability space"""

    position: Position
    log_density: float
    log_density_grad: Optional[float] = None


class KernelState(NamedTuple):
    """Represent the state of a stateful MCMC kernel"""

    pass


class SamplingAlgorithm(NamedTuple):
    """Represent a sampling algorithm"""

    init: Callable[[NamedTuple], Tuple[ChainState, KernelState]]
    step: Callable[
        [
            ChainState,
            Callable[[NamedTuple], float],
        ],
        Callable[[ChainState], Tuple[ChainState, KernelInfo]],
    ]
