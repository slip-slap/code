from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

testlabel = mnist.test.labels
#print(testlabel)
print(" 训练数据%d" % (mnist.train.num_examples))


import tensorflow as tf

x = tf.placeholder("float", [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))




y = tf.nn.softmax(tf.matmul(x,W)+b)




y_ = tf.placeholder("float", [None,10])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
init = tf.initialize_all_variables()
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
sess = tf.Session()
sess.run(init)

num=0

for i in range(10):
    batch_xs, batch_ys = mnist.train.next_batch(10)
    if i%100 ==0:
        print(num+1)
    #print(batch_ys)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    #print(sess.run(b))

#batch = mnist.train.next_batch(10)
#sess.run(train_step,feed_dict={x: batch[0],y_: batch[1]})


correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
