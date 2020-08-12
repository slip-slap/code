
import tensorflow as tf

def graph_add():
    g = tf.Graph()
    with g.as_default() as g:
        a = tf.placeholder(tf.float32, [], name='a')
        b = tf.placeholder(tf.float32, [], name='b')
        my_variable = tf.get_variable("my_variable",shape=[1,])
        c = tf.add(a, b, name='c')
        return g.as_graph_def()

def graph_pow():
    g = tf.Graph()
    with g.as_default() as g:
        d = tf.placeholder(tf.float32, [], name='d')
        e = tf.pow(d, 2, name='e')
    return g.as_graph_def()


tf.reset_default_graph()
a = tf.placeholder(tf.float32, [], name='a')
b = tf.placeholder(tf.float32, [], name='b')
first_graph = tf.import_graph_def(graph_add(),name="first")

"""
g2 = tf.import_graph_def(graph_pow(), input_map={'d': g1}, \
        return_elements=['e:0'])  
"""

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    c  = sess.run(first_graph, feed_dict={a:10, b:20})
    print(c)
