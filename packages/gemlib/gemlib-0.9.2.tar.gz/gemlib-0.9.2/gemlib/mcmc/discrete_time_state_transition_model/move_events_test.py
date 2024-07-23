"""Test event time samplers"""

# ruff: noqa: PLR2004

import pytest
import tensorflow as tf

from gemlib.mcmc.discrete_time_state_transition_model.move_events import (
    TransitionTopology,
    UncalibratedEventTimesUpdate,
)


@pytest.fixture
def random_events():
    """SEIR model with prescribed starting conditions"""
    events = tf.random.uniform(
        [10, 10, 3], minval=0, maxval=100, dtype=tf.float64, seed=0
    )
    return events


@pytest.fixture
def initial_state():
    popsize = tf.fill([10], tf.constant(100.0, tf.float64))
    initial_state = tf.stack(
        [
            popsize,
            tf.ones_like(popsize),
            tf.zeros_like(popsize),
            tf.zeros_like(popsize),
        ],
        axis=-1,
    )
    return initial_state


@pytest.mark.skipif(
    len(tf.config.get_visible_devices("GPU")) > 0,
    reason="Inconsitent results between GPU and CPU",
)
def test_uncalibrated_event_time_update(random_events, initial_state):
    def tlp(_):
        return tf.constant(0.0, tf.float64)

    kernel = UncalibratedEventTimesUpdate(
        target_log_prob_fn=tlp,
        topology=TransitionTopology(prev=0, target=1, next=2),
        initial_state=initial_state,
        dmax=4,
        mmax=1,
        nmax=10,
    )

    pkr = kernel.bootstrap_results(random_events)

    _, results = kernel.one_step(random_events, pkr, seed=[0, 1])

    assert results.m == 1
    assert results.t == 6
    assert results.delta_t == -1
    assert results.x_star == 4
    assert results.target_log_prob == 0.0
