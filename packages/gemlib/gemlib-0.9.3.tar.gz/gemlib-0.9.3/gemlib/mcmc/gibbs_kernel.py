"""Gibbs sampling kernel"""
# ruff: noqa: B023

import logging
from collections import namedtuple
from typing import Callable, List, Tuple

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers, unnest
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

tfd = tfp.distributions  # pylint: disable=no-member
tfb = tfp.bijectors  # pylint: disable=no-member
mcmc = tfp.mcmc  # pylint: disable=no-member

logging.basicConfig(format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("gemlib.gibbs_kernel")
logger.setLevel(logging.DEBUG)


class GibbsKernelResults(
    mcmc_util.PrettyNamedTupleMixin,
    namedtuple(
        "GibbsKernelResults",
        ["target_log_prob", "inner_results", "seed"],
    ),
):
    """Represents kernel results"""

    __slots__ = ()


class GibbsStep(
    mcmc_util.PrettyNamedTupleMixin,
    namedtuple(
        "GibbsStep",
        ["state_parts", "kernel_fn"],
    ),
):
    """Represents a Gibbs step"""

    __slots__ = ()


def is_namedtuple(x):
    """Return `True` if `x` looks like a `namedtuple`."""
    return hasattr(x, "_fields")


def _flatten_results(results):
    """Results structures from nested Gibbs samplers sometimes
    need flattening for writing out purposes.
    """

    def recurse(r):
        for i in iter(r):
            if isinstance(i, list):
                yield from _flatten_results(i)
            else:
                yield i

    return list(recurse(results))


def _has_gradients(results):
    return unnest.has_nested(results, "grads_target_log_prob")


def _get_target_log_prob(results):
    """Fetches a target log prob from a results structure"""
    return unnest.get_innermost(results, "target_log_prob")


def _update_target_log_prob(results, target_log_prob):
    """Puts a target log prob into a results structure"""
    if isinstance(results, GibbsKernelResults):
        replace_fn = unnest.replace_outermost
    else:
        replace_fn = unnest.replace_innermost
    return replace_fn(results, target_log_prob=target_log_prob)


def _maybe_transform_value(tlp, state, kernel, direction):
    if not isinstance(kernel, tfp.mcmc.TransformedTransitionKernel):
        return tlp

    jacobian_parts = [
        b.inverse_log_det_jacobian(x)
        for b, x in zip(
            tf.nest.flatten(kernel.bijector), tf.nest.flatten(state)
        )
    ]
    jacobian = tf.math.add_n(jacobian_parts)

    if direction == "forward":
        return tlp + jacobian
    if direction == "inverse":
        return tlp - jacobian

    raise AttributeError("`direction` must be `forward` or `inverse`")


def _make_namedtuple(input_dict):
    return namedtuple("NamedTuple", input_dict.keys())(**input_dict)


def _split_namedtuple(full_namedtuple, subset_names):
    """Splits a StructTuple of variables into `subset` and `compl`

    :param full_struct_tuple: `namedtuple` to split
    :param subset_names: names of required subset vars
    :returns: a tuple `(subset: namedtuple, compl: namedtuple)`
    """
    full_dict = full_namedtuple._asdict()
    subset = _make_namedtuple(
        {k: v for k, v in full_dict.items() if k in subset_names}
    )
    compl = _make_namedtuple(
        {k: v for k, v in full_dict.items() if k not in subset_names}
    )
    return subset, compl


def _split_state(global_state, indices):
    """Split a global state into subset and complement

    Args:
    ----
        global_state: a tuple or namedtuple representing the global state
        subset: a tuple of indices or names (if `global_state` is a namedtuple)
            representing a subset.

    Returns:
    -------
        a tuple of `(subset, complement)`

    """
    if is_namedtuple(global_state):
        return _split_namedtuple(global_state, indices)

    return (
        [s for i, s in enumerate(global_state) if i in indices],
        [s for i, s in enumerate(global_state) if i not in indices],
    )


def _scatter_state(global_state, subset, indices=()):
    """Scatters `subset` into `global_state`.

    Args:
    ----
        global_state: a tuple or namedtuple representing the global state
        subset: a tuple or namedtuple containing values to be scattered into
            `global_state`.
        indices: if `subset` is a tuple, `indices` is a tuple of corresponding
            indices into `global_state`.

    Returns:
    -------
        a tuple or namedtuple of the same structure as `global_state`.

    """
    if is_namedtuple(global_state) and is_namedtuple(subset):
        return global_state._replace(**subset._asdict())

    for i, state_part in zip(indices, subset):
        global_state[i] = state_part

    return global_state


class GibbsKernel(mcmc.TransitionKernel):
    """Component-wise MCMC sampling.

    ``GibbsKernel`` is designed to fit within TensorFlow Probability's MCMC
    framework, essentially acting as a "meta-kernel" that aggregates a
    sequence of component-wise kernels.

    Example:
    -------
        Sample from the posterior of a linear model::

            import numpy as np
            import tensorflow as tf
            import tensorflow_probability as tfp
            from gemlib.mcmc.gibbs_kernel import GibbsKernel

            tfd = tfp.distributions

            dtype = np.float32

            # data
            x = dtype([2.9, 4.2, 8.3, 1.9, 2.6, 1.0, 8.4, 8.6, 7.9, 4.3])
            y = dtype([6.2, 7.8, 8.1, 2.7, 4.8, 2.4, 10.7, 9.0, 9.6, 5.7])


            # define linear regression model
            def Model(x):
                def alpha():
                    return tfd.Normal(loc=dtype(0.0), scale=dtype(1000.0))

                def beta():
                    return tfd.Normal(loc=dtype(0.0), scale=dtype(100.0))

                def sigma():
                    return tfd.Gamma(concentration=dtype(0.1), rate=dtype(0.1))

                def y(alpha, beta, sigma):
                    mu = alpha + beta * x
                    return tfd.Normal(mu, scale=sigma)

                return tfd.JointDistributionNamed(
                    dict(alpha=alpha, beta=beta, sigma=sigma, y=y)
                )


            # target log probability of linear model
            def log_prob(alpha, beta, sigma):
                lp = model.log_prob(
                    {"alpha": alpha, "beta": beta, "sigma": sigma, "y": y}
                )
                return tf.reduce_sum(lp)


            # random walk Markov chain function
            def kernel_make_fn(target_log_prob_fn, state):
                return tfp.mcmc.RandomWalkMetropolis(
                    target_log_prob_fn=target_log_prob_fn
                )


            # posterior distribution MCMC chain
            @tf.function
            def posterior(iterations, burnin, thinning, initial_state):
                kernel_list = [
                    (
                        0,
                        kernel_make_fn,
                    ),  # conditional probability for zeroth parmeter alpha
                    (
                        1,
                        kernel_make_fn,
                    ),  # conditional probability for first parameter beta
                    (2, kernel_make_fn),
                ]  # conditional probability for second parameter sigma
                kernel = GibbsKernel(
                    target_log_prob_fn=log_prob, kernel_list=kernel_list
                )
                return tfp.mcmc.sample_chain(
                    num_results=iterations,
                    current_state=initial_state,
                    kernel=kernel,
                    num_burnin_steps=burnin,
                    num_steps_between_results=thinning,
                    parallel_iterations=1,
                    trace_fn=None,
                )


            # initialize model
            model = Model(x)
            initial_state = [
                dtype(0.1),
                dtype(0.1),
                dtype(0.1),
            ]  # start chain at alpha=0.1, beta=0.1, sigma=0.1

            # estimate posterior distribution
            samples = posterior(
                iterations=10000,
                burnin=1000,
                thinning=0,
                initial_state=initial_state,
            )

            tf.print("alpha samples:", samples[0])
            tf.print("beta  samples:", samples[1])
            tf.print("sigma samples:", samples[2])
            tf.print(
                "sample means: [alpha, beta, sigma] =",
                tf.math.reduce_mean(samples, axis=1),
            )

    """

    def __init__(
        self,
        target_log_prob_fn: Callable[[float], float],
        kernel_list: List[Tuple[Tuple[int, ...], Callable]],
        name: str = None,
    ):
        """Build a Gibbs sampling scheme from component kernels.

        Args:
        ----
            target_log_prob_fn: a function that takes `state` arguments
                                   and returns the target log probability
                                   density.
            kernel_list: a list of tuples `(state_part_idx, kernel_make_fn)`.
                            `state_part_idx` denotes the index (relative to
                            positional args in `target_log_prob_fn`) of the
                            state the kernel updates.  `kernel_make_fn` takes
                            arguments `target_log_prob_fn` and `state`,
                            returning a `tfp.mcmc.TransitionKernel`.

        Returns:
        -------
            an instance of `GibbsKernel`

        """
        # Require to check if all kernel.is_calibrated is True
        self._parameters = {
            "target_log_prob_fn": target_log_prob_fn,
            "kernel_list": kernel_list,
            "name": name,
        }

    @property
    def is_calibrated(self):
        return True

    @property
    def target_log_prob_fn(self):
        """Target log probability function."""
        return self._parameters["target_log_prob_fn"]

    @property
    def kernel_list(self):
        """List of kernel-build functions."""
        return self._parameters["kernel_list"]

    @property
    def name(self):
        """Name of the kernel."""
        return self._parameters["name"]

    def one_step(self, current_state, previous_results, seed=None):
        """Iterate over the state elements, calling each kernel in turn.

        The ``target_log_prob`` is forwarded to the next ``previous_results``
        such that each kernel has a current ``target_log_prob`` value.
        Transformations are automatically performed if the kernel is of
        type ``tfp.mcmc.TransformedTransitionKernel``.

        In graph and XLA modes, the for loop should be unrolled.

        Args:
        ----
            current_state: the current chain state
            previous_results: a ``GibbsKernelResults`` instance
            seed: an optional list of two scalar ``int`` tensors.

        Returns:
        -------
            a tuple of ``(next_state, results)``.

        """
        seed = samplers.sanitize_seed(seed, salt="GibbsKernel")

        global_state_parts = current_state

        next_results = []
        untransformed_target_log_prob = previous_results.target_log_prob
        seeds = samplers.split_seed(seed, n=len(self.kernel_list))

        for (state_part_indices, kernel_fn), previous_step_results, seed in zip(
            self.kernel_list, previous_results.inner_results, seeds
        ):
            if not mcmc_util.is_list_like(state_part_indices):
                state_part_indices = [state_part_indices]  # noqa: PLW2901

            # Extract state parts required for step
            step_state_parts, _ = _split_state(
                global_state_parts, state_part_indices
            )

            def target_log_prob_fn(*kernel_state):
                if is_namedtuple(step_state_parts):
                    kernel_state = step_state_parts.__class__(*kernel_state)
                state_parts = _scatter_state(
                    global_state_parts,
                    kernel_state,
                    state_part_indices,
                )
                return self.target_log_prob_fn(*state_parts)

            # Build kernel function
            kernel = kernel_fn(target_log_prob_fn, global_state_parts)

            # Forward the current tlp to the kernel.  If the kernel is
            # gradient-based, we need to calculate fresh gradients,
            # as these cannot easily be forwarded
            # from the previous Gibbs step.
            if _has_gradients(previous_step_results):
                # TODO would be better to avoid re-calculating the whole of
                # `bootstrap_results` when we just need to calculate gradients.
                fresh_previous_results = unnest.UnnestingWrapper(
                    kernel.bootstrap_results(step_state_parts)
                )
                previous_step_results = unnest.replace_innermost(  # noqa: PLW2901
                    previous_step_results,
                    target_log_prob=fresh_previous_results.target_log_prob,
                    grads_target_log_prob=fresh_previous_results.grads_target_log_prob,
                )

            else:
                previous_step_results = _update_target_log_prob(  # noqa: PLW2901
                    previous_step_results,
                    _maybe_transform_value(
                        tlp=untransformed_target_log_prob,
                        state=step_state_parts,
                        kernel=kernel,
                        direction="inverse",
                    ),
                )

            new_step_state_parts, next_kernel_results = kernel.one_step(
                step_state_parts, previous_step_results, seed
            )
            if is_namedtuple(step_state_parts):
                new_step_state_parts = step_state_parts.__class__(
                    *new_step_state_parts,
                )

            next_results.append(next_kernel_results)

            # Cache the new tlp for use in the next Gibbs step
            untransformed_target_log_prob = _maybe_transform_value(
                tlp=_get_target_log_prob(next_kernel_results),
                state=new_step_state_parts,
                kernel=kernel,
                direction="forward",
            )

            global_state_parts = _scatter_state(
                global_state_parts, new_step_state_parts, state_part_indices
            )

            if is_namedtuple(current_state):
                global_state_parts = current_state.__class__(
                    *global_state_parts,
                )

        return (
            global_state_parts
            if mcmc_util.is_list_like(current_state)
            else global_state_parts[0],
            GibbsKernelResults(
                target_log_prob=untransformed_target_log_prob,
                inner_results=next_results,
                seed=seeds[-1],
            ),
        )

    def bootstrap_results(self, current_state):
        """Set up the results tuple.

        Args:
        ----
            current_state: a list of state parts representing the Markov chain
                           state
        Returns:
            an instance of `GibbsKernelResults`

        """
        global_state_parts = current_state
        inner_results = []
        untransformed_target_log_prob = 0.0

        for state_part_indices, kernel_fn in self.kernel_list:
            if not mcmc_util.is_list_like(state_part_indices):
                state_part_indices = [state_part_indices]  # noqa: PLW2901

            step_state_parts, _ = _split_state(
                global_state_parts, state_part_indices
            )

            def tlp_fn(*kernel_state):
                if is_namedtuple(step_state_parts):
                    kernel_state = step_state_parts.__class__(*kernel_state)
                state_parts = _scatter_state(
                    global_state_parts,
                    kernel_state,
                    state_part_indices,
                )

                return self.target_log_prob_fn(*state_parts)

            kernel = kernel_fn(tlp_fn, global_state_parts)
            kernel_results = kernel.bootstrap_results(step_state_parts)

            inner_results.append(kernel_results)
            untransformed_target_log_prob = _maybe_transform_value(
                tlp=_get_target_log_prob(kernel_results),
                state=step_state_parts,
                kernel=kernel,
                direction="forward",
            )

        return GibbsKernelResults(
            target_log_prob=untransformed_target_log_prob,
            inner_results=inner_results,
            seed=samplers.zeros_seed(),
        )
