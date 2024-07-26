"""Test partially censored events move for DiscreteTimeStateTransitionModel"""

import pytest
import tensorflow as tf

from gemlib.mcmc.discrete_time_state_transition_model import TransitionTopology

from .move_events import move_events


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


def test_move_events(random_events, initial_state):
    def tlp(x):
        return tf.constant(0.0, dtype=tf.float64)

    kernel = move_events(
        topology=TransitionTopology(0, 1, 2),
        dmax=5,
        mmax=1,
        nmax=10,
    )

    state = kernel.init(tlp, random_events, initial_state)
    seed = [0, 0]
    new_state, results = kernel.step(tlp, state, seed, initial_state)
