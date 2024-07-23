"""Right-censored events MCMC test"""

import pytest
import tensorflow as tf

from gemlib.mcmc.discrete_time_state_transition_model import TransitionTopology

from .right_censored_events_mh import right_censored_events_mh


@pytest.mark.skip("Work in progress")
def test_right_censored_events_mh(random_events, initial_state):
    def tlp(_):
        return tf.constant(0.0, tf.float64)

    kernel = right_censored_events_mh(
        topology=TransitionTopology(0, 1, 2),
        nmax=10,
        t_range=(6, 10),
    )

    state = kernel.init(tlp, random_events, initial_state)
    seed = [0, 0]
    new_state, info = kernel.step(tlp, state, seed, initial_state)

    print(info)

    raise AssertionError()
