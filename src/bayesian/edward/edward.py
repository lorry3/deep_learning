import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import edward as ed
from edward.models import RandomVariable


x_train = np.linspace(-3, 3, num=50)
y_train = np.cos(x_train) + np.random.normal(0, 0.1, size=50)
x_train = x_train.astype(np.float32).reshape((50, 1))
y_train = y_train.astype(np.float32).reshape((50, 1))

plt.scatter(x_train, y_train)
plt.show()


W_0 = RandomVariable(loc=tf.zeros([1, 2]), scale=tf.ones([1, 2]))
W_1 = RandomVariable(loc=tf.zeros([2, 1]), scale=tf.ones([2, 1]))
b_0 = RandomVariable(loc=tf.zeros(2), scale=tf.ones(2))
b_1 = RandomVariable(loc=tf.zeros(1), scale=tf.ones(1))

x = x_train
y = RandomVariable(loc=tf.matmul(tf.tanh(tf.matmul(x, W_0) + b_0), W_1) + b_1, scale=0.1)


qW_0 = RandomVariable(loc=tf.get_variable("qW_0/loc", [1, 2]), scale=tf.nn.softplus(tf.get_variable("qW_0/scale", [1, 2])))
qW_1 = RandomVariable(loc=tf.get_variable("qW_1/loc", [2, 1]), scale=tf.nn.softplus(tf.get_variable("qW_1/scale", [2, 1])))
qb_0 = RandomVariable(loc=tf.get_variable("qb_0/loc", [2]), scale=tf.nn.softplus(tf.get_variable("qb_0/scale", [2])))
qb_1 = RandomVariable(loc=tf.get_variable("qb_1/loc", [1]), scale=tf.nn.softplus(tf.get_variable("qb_1/scale", [1])))

inference = ed.KLqp({W_0: qW_0, b_0: qb_0, W_1: qW_1, b_1: qb_1}, data={y: y_train})
inference.run(n_iter=1000)
