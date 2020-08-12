import tensorflow as tf
import numpy as np

def layer(layer_name, data, output_channels):
    with tf.variable_scope(layer_name,reuse=tf.AUTO_REUSE):
        w = tf.get_variable(name="weight",shape=[data.shape[-1],output_channels])
        b = tf.get_variable(name="bias",shape=[output_channels])
        summary_bias = tf.summary.histogram("bias",b)
        y = tf.matmul(data,w)
        y = tf.add(y,b,name="result")
    return y

# use NumPy to produce data
x_data = np.float32(np.random.rand(100, 2))
y_data = np.dot(x_data,[[0.1],[0.2]]) + 0.300


x = tf.placeholder("float", [None,2],name="input_x")
y_ = tf.placeholder("float", [None,1],name="input_y")

y=layer("first",x,6)
y=layer("second",y,2)
y=layer("third",y,3)
y=layer("fourth",y,1)

# loss
loss = tf.reduce_mean(tf.square(y - y_))
summary_loss = tf.summary.scalar(name="loss",tensor=loss)
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

# init

init = tf.initialize_all_variables()
merged = tf.summary.merge_all()

saver = tf.train.Saver()

# run graph
with tf.Session() as sess:
    sess.run(init)
    writer = tf.summary.FileWriter("./ann",sess.graph)
    for step in range(0, 40000):
        if(step%2000 == 0):
            saver.save(sess, "./train_model/model.ckpt")
        sess.run(train,feed_dict={x:x_data, y_:y_data})
        summary = sess.run(merged,feed_dict={x:x_data,y_:y_data})
        writer.add_summary(summary, step)
        if step % 20 == 0:
            print(step,sess.run(loss,feed_dict={x:x_data,y_:y_data}))

