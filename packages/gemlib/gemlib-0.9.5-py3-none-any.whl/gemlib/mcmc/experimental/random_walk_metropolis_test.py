"""Test the random walk metropolis kernel"""

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from .composable_kernel import Step
from .mcmc_sampler import mcmc
from .random_walk_metropolis import RwmhInfo, rwmh

NUM_SAMPLES = 100000


def split_seed(seed, n):
    n = tf.convert_to_tensor(n)
    return tfp.random.split_seed(seed, n=n)


def tree_map(fn, *args):
    return tf.nest.map_structure(fn, *args)


def tree_flatten(tree):
    return tf.nest.flatten(tree)


def get_seed():
    # jax.random.PRNGKey(42)
    return [0, 0]


@tfp.distributions.JointDistributionCoroutine
def simple_model():
    yield tfp.distributions.Normal(loc=0.0, scale=1.0, name="foo")
    yield tfp.distributions.Normal(loc=1.0, scale=1.0, name="bar")
    yield tfp.distributions.Normal(loc=2.0, scale=1.0, name="baz")


def test_rwmh_1kernel():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = rwmh(scale=0.3)

    state = kernel.init(simple_model.log_prob, initial_position)
    new_state, results = kernel.step(simple_model.log_prob, state, seed)

    assert tree_map(lambda x, y: None, new_state, state)

    expected_results = (RwmhInfo(is_accepted=True),)
    assert tree_map(lambda x, y: x == y, results, expected_results)


def test_rwmh_2kernel():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = Step(rwmh(scale=0.3), ["foo"]) >> Step(
        rwmh(scale=0.1), ["bar", "baz"]
    )

    state = kernel.init(simple_model.log_prob, initial_position)
    new_state, results = kernel.step(simple_model.log_prob, state, seed)

    assert tree_map(lambda x, y: None, new_state, state)

    expected_results = (RwmhInfo(is_accepted=True), RwmhInfo(is_accepted=True))
    assert tree_map(lambda x, y: x == y, results, expected_results)


def test_rwmh_3kernel():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = (
        Step(rwmh(scale=0.3), ["foo"])
        >> Step(rwmh(scale=0.1), ["bar"])
        >> Step(rwmh(scale=0.2), ["baz"])
    )

    state = kernel.init(simple_model.log_prob, initial_position)
    new_state, results = kernel.step(simple_model.log_prob, state, seed)

    assert tree_map(lambda x, y: None, new_state, state)

    expected_results = (
        RwmhInfo(is_accepted=True),
        RwmhInfo(is_accepted=True),
        RwmhInfo(is_accepted=True),
    )
    assert tree_map(lambda x, y: x == y, results, expected_results)


def test_rwmh_1kernel_mcmc():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = rwmh(scale=1.8)

    posterior, info = tf.function(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=kernel,
            target_density_fn=simple_model.log_prob,
            initial_position=initial_position,
            seed=get_seed(),
        ),
        jit_compile=True,
    )()

    # Test results
    np.testing.assert_approx_equal(
        np.mean(info[0].is_accepted), 0.23, significant=1
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.mean(x), posterior),
        [0.0, 1.0, 2.0],
        rtol=0.01,
        atol=0.05,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.var(x), posterior),
        [1.0, 1.0, 1.0],
        rtol=0.01,
        atol=0.05,
    )


def test_rwmh_2kernel_mcmc():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = Step(rwmh(scale=2.3), ["foo"]) >> Step(
        rwmh(scale=1.8), ["bar", "baz"]
    )

    posterior, info = tf.function(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=kernel,
            target_density_fn=simple_model.log_prob,
            initial_position=initial_position,
            seed=get_seed(),
        ),
        jit_compile=True,
    )()

    # Test results
    np.testing.assert_allclose(
        tree_flatten(tree_map(lambda x: np.mean(x), info)),
        [0.45, 0.33],
        atol=0.01,
        rtol=0.05,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.mean(x), posterior),
        [0.0, 1.0, 2.0],
        rtol=0.01,
        atol=0.05,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.var(x), posterior),
        [1.0, 1.0, 1.0],
        rtol=0.01,
        atol=0.05,
    )


def test_rwmh_3kernel_mcmc():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = (
        Step(rwmh(scale=2.3), ["foo"])
        >> Step(rwmh(scale=2.3), ["bar"])
        >> Step(rwmh(scale=2.3), ["baz"])
    )

    posterior, info = tf.function(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=kernel,
            target_density_fn=simple_model.log_prob,
            initial_position=initial_position,
            seed=get_seed(),
        ),
        jit_compile=True,
    )()

    # Test results
    np.testing.assert_allclose(
        tree_flatten(tree_map(lambda x: np.mean(x), info))[0],
        [0.45, 0.45, 0.45],
        atol=0.01,
        rtol=0.05,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.mean(x), posterior),
        [0.0, 1.0, 2.0],
        rtol=0.01,
        atol=0.05,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.var(x), posterior),
        [1.0, 1.0, 1.0],
        rtol=0.01,
        atol=0.05,
    )
