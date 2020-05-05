import tensorflow as tf
from tensorflow.keras import layers

from ..initializers import GlorotOrthogonal


class OutputBlock(layers.Layer):
    def __init__(self, emb_size, num_dense, num_targets=12,
                 activation=None, name='output', **kwargs):
        super().__init__(name=name, **kwargs)
        weight_init = GlorotOrthogonal()

        self.dense_rbf = layers.Dense(emb_size, use_bias=False,
                                      kernel_initializer=weight_init)
        self.dense_layers = []
        for i in range(num_dense):
            self.dense_layers.append(
                layers.Dense(emb_size, activation=activation, use_bias=True,
                             kernel_initializer=weight_init))
        self.dense_final = layers.Dense(num_targets, use_bias=False,
                                        kernel_initializer='zeros')

    def call(self, inputs, extract_flag=False):
        x, rbf, idnb_i, n_atoms = inputs

        g = self.dense_rbf(rbf)
        x = g * x
        x = tf.math.unsorted_segment_sum(x, idnb_i, n_atoms)

        for layer in self.dense_layers:
            x = layer(x)
        out = self.dense_final(x)
        if not extract_flag:
            return out
        else:
            return out, x
