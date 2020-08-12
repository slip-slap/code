import tensorflow as tf

classes = 3

labels = tf.constant([0,1,2])
output = tf.one_hot(labels, classes)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    output = sess.run(output)
    print(output)
