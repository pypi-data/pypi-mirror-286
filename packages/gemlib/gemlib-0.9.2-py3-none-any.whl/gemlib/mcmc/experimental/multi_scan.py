"""MultiScanKernel calls one_step a number of times on an inner kernel"""

from functools import partial

import tensorflow as tf
from tensorflow_probability.python.internal import samplers

from .mcmc_base import SamplingAlgorithm

__all__ = ["multi_scan"]


def multi_scan(
    num_updates: int, sampling_algorithm: SamplingAlgorithm
) -> SamplingAlgorithm:
    """Performs multiple applications of a kernel

    `sampling_algorithm` is invoked `num_updates` times
    returning the state and info after the last step.

    Args
    ----
    num_updates: integer giving the number of updates
    sampling_algorithm: an instance of `SamplingAlgorithm`

    Return
    ------
    An instance of `SamplingAlgorithm`
    """

    num_updates_ = tf.convert_to_tensor(num_updates)
    init_fn = sampling_algorithm.init

    def step_fn(target_log_prob_fn, current_state, seed=None):
        seed = samplers.sanitize_seed(seed, salt="multi_scan_kernel")
        seeds = samplers.split_seed(seed, n=num_updates)
        kernel = partial(sampling_algorithm.step, target_log_prob_fn)

        def body(i, state, _):
            state, info = kernel(state, seeds[i])
            return i + 1, state, info

        def cond(i, *_):
            return i < num_updates_

        init_state, init_info = kernel(current_state, seed)  # unrolled first it

        _, last_state, last_info = tf.while_loop(
            cond, body, loop_vars=(1, init_state, init_info)
        )
        return last_state, last_info

    return SamplingAlgorithm(init_fn, step_fn)
