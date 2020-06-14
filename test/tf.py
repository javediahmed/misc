import tensorflow as tf
from pdb import set_trace as st

x = tf.Variable(3, name='x')
y = tf.Variable(4, name='y')

f = x*x*y + y + 2

sess = tf.Session()
sess.run(tf.global_variables_initializer())
result = sess.run(f)
print(result)

st()

