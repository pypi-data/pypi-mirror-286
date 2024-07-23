# Dependency imports
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import test_util

from gemlib.distributions.discrete_markov import compute_state
from gemlib.distributions.discrete_time_state_transition_model import (
    DiscreteTimeStateTransitionModel,
)


@test_util.test_all_tf_execution_regimes
class TestDiscreteTimeStateTransitionModel(test_util.TestCase):
    def setUp(self):
        self.dtype = tf.float32
        self.incidence_matrix = [[-1, 0], [1, -1], [0, 1]]
        self.initial_state_A = [[99, 1, 0]]
        self.initial_state_B = [[8000, 2000, 0]]
        self.beta = 0.28
        self.gamma = 0.14
        self.nsim = 50

    def init_model(
        self,
        beta,
        gamma,
        incidence_matrix,
        initial_state,
        initial_step=0.0,
        time_delta=1.0,
        num_steps=100,
        dtype=tf.float32,
    ):
        def txrates(t, state):
            si = beta * state[:, 1] / tf.reduce_sum(state)
            ir = tf.constant([gamma], dtype)
            return [si, ir]

        return DiscreteTimeStateTransitionModel(
            transition_rates=txrates,
            incidence_matrix=incidence_matrix,
            initial_state=initial_state,
            initial_step=initial_step,
            time_delta=time_delta,
            num_steps=num_steps,
        )

    def test_float32(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_A, self.dtype)

        sir = self.init_model(
            self.beta, self.gamma, incidence_matrix, initial_state, num_steps=5
        )

        eventlist = sir.sample()
        eventlist_ = self.evaluate(eventlist)
        self.assertDTypeEqual(eventlist_, np.float32)

        lp = sir.log_prob(eventlist)
        lp_ = self.evaluate(lp)
        self.assertDTypeEqual(lp_, np.float32)

    def test_float64(self):
        dtype = tf.float64
        incidence_matrix = tf.constant(self.incidence_matrix, dtype)
        initial_state = tf.constant(self.initial_state_A, dtype)

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            num_steps=5,
            dtype=dtype,
        )

        eventlist = sir.sample()
        eventlist_ = self.evaluate(eventlist)
        self.assertDTypeEqual(eventlist_, np.float64)

        lp = sir.log_prob(eventlist)
        lp_ = self.evaluate(lp)
        self.assertDTypeEqual(lp_, np.float64)

    def test_non_integer_time_steps(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_A, self.dtype)

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            initial_step=1.5,
            time_delta=0.5,
            num_steps=100,
        )

        eventlist = sir.sample()
        self.assertShapeEqual(np.ndarray(shape=(1, 100, 2)), eventlist)

        lp = sir.log_prob(eventlist)
        self.assertShapeEqual(np.ndarray(shape=()), lp)

    def test_log_prob_over_simuations(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_B, self.dtype)

        sir = self.init_model(
            self.beta, self.gamma, incidence_matrix, initial_state, num_steps=60
        )

        def simulate_one(elems):
            return sir.sample()

        eventlist = tf.map_fn(
            simulate_one,
            tf.ones([self.nsim, incidence_matrix.shape[1]]),
            fn_output_signature=self.dtype,
        )

        lp = tf.vectorized_map(
            fn=lambda i: sir.log_prob(eventlist[i, ...]),
            elems=tf.range(self.nsim),
        )
        lp_mean = tf.math.reduce_mean(lp)
        lp_mean_ = self.evaluate(lp_mean)
        actual_mean = (
            -395
        )  # sample_mean ~= -395 derived from 1000 simulations of this model
        self.assertAllClose(
            lp_mean_, actual_mean, rtol=1e-06, atol=8.1
        )  # sample_variance ~= 65

    def test_model_constraints(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_A, self.dtype)
        time_delta = 1.0
        num_steps = 100

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            time_delta=time_delta,
            num_steps=num_steps,
        )

        def simulate_one(elems):
            return sir.sample()

        eventlist = tf.map_fn(
            simulate_one,
            tf.ones([self.nsim, incidence_matrix.shape[1]]),
            fn_output_signature=self.dtype,
        )
        ts = compute_state(initial_state, eventlist, incidence_matrix)

        # Crude check that some simulations have nontrivial dynamics
        # i.e. some units arrived in recovered compartments for some simulations
        sum_at_tmax = tf.reduce_sum(ts[:, :, num_steps - 1, 2])
        test_sum_at_tmax = (
            tf.cast(self.nsim * num_steps, self.dtype) / 4
        )  # factor 4 is a choice
        self.assertGreater(
            self.evaluate(sum_at_tmax), self.evaluate(test_sum_at_tmax)
        )

        # Check N is conserved at each time point
        # Note dS/dt + dI/dt + dR/dt = 0 then integrating over dt leads to
        # N = S + I + R
        sums_at_t = tf.vectorized_map(
            fn=lambda i: tf.reduce_sum(ts[:, :, i, :]),
            elems=tf.range(num_steps),
        )
        expected_sums = tf.broadcast_to(
            tf.cast(self.nsim * num_steps, self.dtype), [num_steps]
        )
        self.assertAllClose(sums_at_t, expected_sums, rtol=1e-06, atol=1e-06)

        # Check dS/dt + dI/dt + dR/dt = 0 at each time point
        def forward_difference(i):
            """Numerical differentiation of states wrt time using forward
            difference.
            """
            x1 = ts[i, 0, :, :]
            x2 = tf.roll(x1, shift=-1, axis=0)
            diffs = (
                tf.math.subtract(
                    x2[0 : ts.shape[-2] - 1, :], x1[0 : ts.shape[-2] - 1, :]
                )
                / time_delta
            )
            return tf.math.reduce_sum(diffs, axis=-1)

        finite_diffs = tf.vectorized_map(
            fn=forward_difference, elems=tf.range(self.nsim)
        )
        expected_diffs = tf.zeros_like(finite_diffs, self.dtype)
        self.assertAllClose(
            finite_diffs, expected_diffs, rtol=1e-06, atol=1e-06
        )

    def test_model_dynamics(self):
        """Check simulation adheres to the SIR system of ODEs.

        This check is performed without being in the thermodynamic limit
        (N->inf, t->inf).

        Let dS/dt=-bIS/N, dI/dt=bIS/N-gI and dR/dt=gI.
        Dividing first equation by third gives dS/dR=-b/g.S/N.
        Separating variables and integrating wrt dR yields
        int(1/S, dS)=-b/g.1/N.int(1, dR).
        Let the integrals have limits S(0), S(t), R(0), R(t).
        The solution to this integral is the transcendental equation
        S(t)=S(0)exp(-b/g.(R(t)-R(0))/N).  Due the stochastic nature of the
        chain binomial algorithm naively checking the simulated right
        hand side of this solution equals (with a given tolerence) the simulated
        left hand side is fraught with difficulty.  However rearranging the
        solution in terms of the time invariant factor
        b/g=-N.ln(S(t)/S(0))/(R(t)-R(0)) makes it possible to check the
        simulated dynamics adhere to the dynamics given by the SIR system of
        ODEs (except when R(t)=R0).

        """

        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_B, self.dtype) * 10
        num_steps = 200
        buffer = 20  # number if initial steps to be omitted

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            time_delta=0.25,
            num_steps=num_steps,
        )

        def simulate_one(elems):
            return sir.sample()

        eventlist = tf.map_fn(
            simulate_one,
            tf.ones([self.nsim, incidence_matrix.shape[1]]),
            fn_output_signature=self.dtype,
        )
        ts = compute_state(initial_state, eventlist, incidence_matrix)

        S0 = initial_state[0, -3]
        R0 = initial_state[0, -1]
        St = ts[:, 0, :, -3]
        Rt = ts[:, 0, :, -1]
        N = tf.reduce_sum(initial_state)
        r0_sim = -N * tf.math.log(St / S0) / (Rt - R0)  # r0=beta/gamma

        # Crude check that some simulations have nontrivial dynamics
        sum_at_tmax = tf.reduce_sum(ts[:, :, num_steps - 1, 2])
        test_sum_at_tmax = (
            tf.cast(self.nsim * num_steps, self.dtype) / 4
        )  # factor 4 is a choice
        self.assertGreater(
            self.evaluate(sum_at_tmax), self.evaluate(test_sum_at_tmax)
        )

        # First time step must be omitted as it will be undefined due to
        #   division by zero n.b. R(t=0)=R0
        # Soft test - summarise the mean of each simulation
        mean_r0_sim = tf.reduce_mean(r0_sim[:, buffer:num_steps], axis=1)
        r0_actual = tf.broadcast_to(self.beta / self.gamma, [self.nsim])
        self.assertAllClose(
            mean_r0_sim, r0_actual, rtol=1e-06, atol=0.11
        )  # atol scales inversely with the size of N

        # Hard test - check all times apart from a few initial steps when R(t)
        # may equal R0
        r0_all_actual = tf.broadcast_to(
            self.beta / self.gamma, [self.nsim, num_steps - buffer]
        )
        self.assertAllClose(
            r0_sim[:, buffer:num_steps], r0_all_actual, rtol=1e-06, atol=0.14
        )


@test_util.test_all_tf_execution_regimes
class TestDiscreteTimeStateTransitionModelLogProbMaxima(test_util.TestCase):
    def init_model(self, params, incidence_matrix, initial_state):
        def txrates(t, state):
            si = 1e-9 + beta * state[:, 1] / tf.reduce_sum(state)
            ir = tf.expand_dims(gamma, axis=0)
            return [si, ir]

        beta, gamma = tf.unstack(params)
        return DiscreteTimeStateTransitionModel(
            transition_rates=txrates,
            incidence_matrix=incidence_matrix,
            initial_state=initial_state,
            initial_step=0.0,
            time_delta=1.0,
            num_steps=100,
        )

    def test_log_prob_mle(self):
        """Test maximum likelihood estimation"""

        dtype = np.float32
        incidence_matrix = tf.constant([[-1, 0], [1, -1], [0, 1]], dtype)
        initial_state = tf.constant([[8000, 2000, 0]], dtype)
        pars = tf.constant([0.5, 0.3], dtype)

        # Simulate a dataset
        sir_orig = self.init_model(pars, incidence_matrix, initial_state)
        events = self.evaluate(sir_orig.sample(seed=(0, 0)))
        print(np.sum(events, axis=-2))

        def logp(pars):
            return -self.init_model(
                pars, incidence_matrix, initial_state
            ).log_prob(events)

        optim_results = tfp.optimizer.nelder_mead_minimize(
            logp,
            initial_vertex=tf.zeros_like(pars),
        )
        print(self.evaluate(optim_results))

        self.assertAllTrue(optim_results.converged)
        self.assertAllClose(optim_results.position, pars, rtol=0.01, atol=0.005)


if __name__ == "__main__":
    tf.test.main()
