"""Test ContinuousTimeStateTransitionModel"""

import numpy as np
import pytest
import tensorflow as tf
from scipy.optimize import minimize

from gemlib.distributions.continuous_time_state_transition_model import (
    ContinuousTimeStateTransitionModel,
    EpidemicEvent,
    compute_state,
)

NUM_EVENTS = 1999


@pytest.fixture
def example_ilm():
    """A simple event list with 4 individuals, SIR model"""
    return {
        "incidence_matrix": np.array(
            [[-1, 0], [1, -1], [0, 1]], dtype=np.float32
        ),
        "event_list": EpidemicEvent(
            time=np.array(
                [0.4, 1.3, 1.5, 1.9, 2.3, np.inf, np.inf], dtype=np.float32
            ),
            transition=np.array([0, 0, 1, 1, 1, 2, 2], dtype=np.int32),
            individual=np.array([1, 2, 0, 2, 1, 0, 0], dtype=np.int32),
        ),
        "initial_conditions": np.array(
            [[0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]], dtype=np.float32
        ),
    }


@pytest.fixture
def simple_sir_model():
    def rate_fn(t, state):
        si_rate = 0.25 * state[:, 1] / tf.reduce_sum(state, axis=-1)
        ir_rate = tf.broadcast_to([0.14], si_rate.shape)

        return si_rate, ir_rate

    # [3 species, 2 reactions]
    incidence_matrix = np.array([[-1, 0], [1, -1], [0, 1]], dtype=np.float32)

    initial_state = np.array(
        [[999, 1, 0]], dtype=np.float32
    )  # [1 unit, 3 classes]

    return ContinuousTimeStateTransitionModel(
        transition_rate_fn=rate_fn,
        incidence_matrix=incidence_matrix,
        initial_state=initial_state,
        num_events=NUM_EVENTS,
        initial_time=0.0,
    )


def test_simple_sir_shapes(simple_sir_model):
    """Test expected output shape"""
    tf.debugging.assert_equal(
        simple_sir_model.event_shape_tensor(), tf.constant(NUM_EVENTS)
    )
    tf.debugging.assert_equal(
        simple_sir_model.event_shape, tf.TensorShape([NUM_EVENTS])
    )
    tf.debugging.assert_equal(
        simple_sir_model.batch_shape_tensor(), tf.constant([], tf.int32)
    )
    tf.debugging.assert_equal(simple_sir_model.batch_shape, tf.TensorShape([]))


def test_simple_sir_eager(simple_sir_model):
    """Test a simple SIR model"""

    sample = simple_sir_model.sample(seed=[0, 0])

    assert isinstance(sample, EpidemicEvent)

    state = simple_sir_model.compute_state(sample)
    tf.debugging.assert_non_negative(state)


def test_simple_sir_graph(simple_sir_model):
    """Test a simple SIR model"""

    @tf.function
    def fn():
        return simple_sir_model.sample(seed=[0, 0])

    sample = fn()

    assert isinstance(sample, EpidemicEvent)

    state = simple_sir_model.compute_state(sample)
    tf.debugging.assert_non_negative(state)


def test_compute_state(example_ilm):
    expected_state_eager = compute_state(
        example_ilm["incidence_matrix"],
        example_ilm["initial_conditions"],
        example_ilm["event_list"],
        include_final_state=True,
    )

    @tf.function
    def compute_state_graph(*args):
        return compute_state(*args)

    expected_state_graph = compute_state_graph(
        example_ilm["incidence_matrix"],
        example_ilm["initial_conditions"],
        example_ilm["event_list"],
        True,
    )

    actual_state = np.array(
        [
            [
                [0, 1, 0],  # T=0
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
            ],
            [
                [0, 1, 0],  # T=1
                [0, 1, 0],
                [1, 0, 0],
                [1, 0, 0],
            ],
            [
                [0, 1, 0],  # T=2
                [0, 1, 0],
                [0, 1, 0],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=3
                [0, 1, 0],
                [0, 1, 0],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=4
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=5
                [0, 0, 1],
                [0, 0, 1],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=6
                [0, 0, 1],
                [0, 0, 1],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=7
                [0, 0, 1],
                [0, 0, 1],
                [1, 0, 0],
            ],
        ],
        dtype=np.float32,
    )

    np.testing.assert_array_equal(expected_state_eager, actual_state)
    np.testing.assert_array_equal(expected_state_graph, actual_state)


def test_simple_sir_loglik(example_ilm):
    """Test loglikelihood function"""
    # epi constants
    incidence_matrix = example_ilm["incidence_matrix"]
    initial_population = example_ilm["initial_conditions"]

    def rate_fn(t, state):
        si_rate = tf.broadcast_to([0.5], [state.shape[0]])
        ir_rate = tf.broadcast_to([0.7], si_rate.shape)

        return si_rate, ir_rate

    # create an instance of the model
    epi_model = ContinuousTimeStateTransitionModel(
        transition_rate_fn=rate_fn,
        incidence_matrix=incidence_matrix,
        initial_state=initial_population,
        num_events=NUM_EVENTS,
        initial_time=0.0,
    )

    log_lik = epi_model.log_prob(example_ilm["event_list"])
    # hand calculated log likelihood
    actual_loglik = -7.256319192936088

    np.testing.assert_almost_equal(log_lik, desired=actual_loglik, decimal=5)


def test_simple_sir_loglik_graph_mode(example_ilm):
    """Test loglikelihood function"""
    # epi constants
    incidence_matrix = example_ilm["incidence_matrix"]
    initial_population = example_ilm["initial_conditions"]

    def rate_fn(t, state):
        si_rate = tf.broadcast_to([0.5], [state.shape[0]])
        ir_rate = tf.broadcast_to([0.7], si_rate.shape)

        return si_rate, ir_rate

    # create an instance of the model
    epi_model = ContinuousTimeStateTransitionModel(
        transition_rate_fn=rate_fn,
        incidence_matrix=incidence_matrix,
        initial_state=initial_population,
        num_events=NUM_EVENTS,
        initial_time=0.0,
    )

    @tf.function
    def fn():
        log_lik = epi_model.log_prob(example_ilm["event_list"])
        return log_lik

    log_lik = fn()
    # hand calculated log likelihood
    actual_loglik = -7.256319192936088

    np.testing.assert_almost_equal(log_lik, desired=actual_loglik, decimal=5)


def test_simple_sir_workflow(simple_sir_model):
    """Using an instance of the ContinuousTimeStateTransitionModel"""

    # sample from the model
    sample_epi_path = simple_sir_model.sample(seed=[20240820, 1347])

    # maximize the likelihood to estimate the parameters of the model
    def make_rate_fn(rate_parameters):
        SI_rate = rate_parameters[0]
        IR_rate = rate_parameters[1]

        def rate_fn(t, state):
            si_rate = SI_rate * state[:, 1] / tf.reduce_sum(state, axis=-1)
            ir_rate = tf.broadcast_to([IR_rate], si_rate.shape)

            return si_rate, ir_rate

        return rate_fn

    def mle_fn(log_rate_parameters):
        rate_parameters = tf.math.exp(log_rate_parameters)
        rate_fn = make_rate_fn(rate_parameters)

        model = ContinuousTimeStateTransitionModel(
            transition_rate_fn=rate_fn,
            incidence_matrix=simple_sir_model.incidence_matrix,
            initial_state=simple_sir_model.initial_state,
            num_events=NUM_EVENTS,
            initial_time=0.0,
        )

        log_lik = model.log_prob(sample_epi_path)
        return -log_lik

    initial_parameters = np.array([-0.1, -0.1], dtype=np.float32)
    opt = minimize(
        mle_fn,
        initial_parameters,
        method="L-BFGS-B",
        jac="3-point",
        options={"finite_diff_rel_step": None},
    )

    std_errors = np.sqrt(np.diagonal(opt.hess_inv.todense()))
    lower_ci = np.exp(opt.x - 1.96 * std_errors)  # 95% CI
    upper_ci = np.exp(opt.x + 1.96 * std_errors)

    actuals = np.array([0.25, 0.14])

    assert opt.success
    assert np.all((lower_ci < actuals) & (actuals < upper_ci))
