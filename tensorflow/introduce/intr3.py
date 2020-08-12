import tensorflow as tf
import numpy
import pdb

BATCHSIZE=6

label = tf.expand_dims(tf.constant([0,2,3,6,7,9]),1)
index = tf.expand_dims(tf.range(0, BATCHSIZE),1)

#concated = tf.concat(1, [index, label])
concated = tf.concat([index, label], 1)
onehot_labels = tf.sparse_to_dense(concated, tf.stack([BATCHSIZE,10]), 1.0, 0.0)

# use a vector
concated2 = tf.constant([1, 3, 4])
onehot_labels2 = tf.sparse_to_dense(concated2, tf.stack([10]), 1.0, 0.0)

# use a scalar
concated = tf.constant(5)
onehot_labels3 = tf.sparse_to_dense(concated2, tf.stack([10]), 1.0, 0.0)

pdb.set_trace()

with tf.Session() as sess:
    #label, index = sess.run([label,index])
    #print(label)
    #print(index)
    result1, result2, result3=sess.run([onehot_labels, onehot_labels2, onehot_labels3])
    print(result1)
    print(result2)
    print(result3)
