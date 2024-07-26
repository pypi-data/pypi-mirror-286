"""The UniformInteger distribution class"""

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    reparameterization,
    samplers,
)

tfd = tfp.distributions


class UniformInteger(tfd.Distribution):
    def __init__(
        self,
        low=0,
        high=1,
        validate_args=False,
        allow_nan_stats=True,
        dtype=tf.int32,
        float_dtype=tf.float32,
        name="UniformInteger",
    ):
        """Integer uniform distribution.

        Args:
        ----
          low: Integer tensor, lower boundary of the output interval. Must have
            `low <= high`.
          high: Integer tensor, _inclusive_ upper boundary of the output
            interval.  Must have `low <= high`.
          validate_args: Python `bool`, default `False`. When `True`
            distribution parameters are checked for validity despite possibly
            degrading runtime performance. When `False` invalid inputs may
            silently render incorrect outputs.
          allow_nan_stats: Python `bool`, default `True`. When `True`,
           statistics (e.g., mean, mode, variance) use the value "`NaN`" to
           indicate the result is undefined. When `False`, an exception is
           raised if one or more of the statistic's batch members are undefined.
          dtype: returned integer dtype when sampling.
          float_dtype: returned float dtype of log probability.
          name: Python `str` name prefixed to Ops created by this class.

        Example 1: sampling
        ```python
        import tensorflow as tf
        from gemlib.distributions.uniform_integer import UniformInteger

        tf.random.set_seed(10402302)
        X = UniformInteger(0, 10, dtype=tf.int32)
        x = X.sample([3, 3], seed=1)
        tf.print("samples:", x, "=", [[8, 4, 8], [2, 7, 9], [6, 0, 9]])
        ```

        Example 2: log probability
        ```python
        import tensorflow as tf
        from gemlib.distributions.uniform_integer import UniformInteger

        X = UniformInteger(0, 10, float_dtype=tf.float32)
        lp = X.log_prob([[8, 4, 8], [2, 7, 9], [6, 0, 9]])
        total_lp = tf.math.round(tf.math.reduce_sum(lp) * 1e5) / 1e5
        tf.print("total lp:", total_lp, "= -20.72327")
        ```

        Raises:
        ------
          InvalidArgument if `low > high` and `validate_args=False`.

        """
        parameters = dict(locals())
        with tf.name_scope(name) as name:
            self._low = tf.cast(low, name="low", dtype=dtype)
            self._high = tf.cast(high, name="high", dtype=dtype)
            super().__init__(
                dtype=dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                parameters=parameters,
                name=name,
            )
        self.float_dtype = float_dtype
        if validate_args is True:
            tf.assert_greater(
                self._high, self._low, "Condition low < high failed"
            )

    @staticmethod
    def _param_shapes(sample_shape):
        return dict(
            zip(
                ("low", "high"),
                ([tf.convert_to_tensor(sample_shape, dtype=tf.int32)] * 2),
            )
        )

    @classmethod
    def _params_event_ndims(cls):
        return {"low": 0, "high": 0}

    @property
    def low(self):
        """Lower boundary of the output interval."""
        return self._low

    @property
    def high(self):
        """Upper boundary of the output interval."""
        return self._high

    def range(self, name="range"):
        """`high - low`."""
        with self._name_and_control_scope(name):
            return self._range()

    def _range(self, low=None, high=None):
        low = self.low if low is None else low
        high = self.high if high is None else high
        return high - low

    def _batch_shape_tensor(self, low=None, high=None):
        return tf.broadcast_dynamic_shape(
            tf.shape(self.low if low is None else low),
            tf.shape(self.high if high is None else high),
        )

    def _batch_shape(self):
        return tf.broadcast_static_shape(self.low.shape, self.high.shape)

    def _event_shape_tensor(self):
        return tf.constant([], dtype=tf.int32)

    def _event_shape(self):
        return tf.TensorShape([])

    def _sample_n(self, n, seed=None):
        with tf.name_scope("sample_n"):
            low = tf.convert_to_tensor(self.low)
            high = tf.convert_to_tensor(self.high)
            shape = tf.concat(
                [[n], self._batch_shape_tensor(low=low, high=high)], 0
            )
            samples = samplers.uniform(shape=shape, dtype=tf.float32, seed=seed)
            return low + tf.cast(
                tf.cast(self._range(low=low, high=high), tf.float32) * samples,
                self.dtype,
            )

    def _prob(self, x):
        with tf.name_scope("prob"):
            low = tf.cast(self.low, self.float_dtype)
            high = tf.cast(self.high, self.float_dtype)
            x = tf.cast(x, dtype=self.float_dtype)

            return tf.where(
                tf.math.is_nan(x),
                x,
                tf.where(
                    (x < low) | (x >= high),
                    tf.zeros_like(x),
                    tf.ones_like(x) / self._range(low=low, high=high),
                ),
            )

    def _log_prob(self, x):
        with tf.name_scope("log_prob"):
            res = tf.math.log(self._prob(x))
            return res
