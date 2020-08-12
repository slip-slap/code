import tensorflow as tf
import data
import tool
import net_cell



input_x = tf.placeholder("float", [None,13],name="input_x")
input_y = tf.placeholder("float", [None,1],name="input_y")

#y = net_cell.normal_net_cell(input_x)
#y = net_cell.feature_net_cell(input_x)
y = net_cell.feature2_net_cell(input_x)
#y = net_cell.feature3_net_cell(input_x)
#y = net_cell.feature4_net_cell(input_x)
#y = net_cell.dimision_keep_cell(input_x)

# loss
loss = tf.reduce_mean(tf.square(y - input_y),name="loss")
summary_loss = tf.summary.scalar(name="loss",tensor=loss)
optimizer = tf.train.GradientDescentOptimizer(0.1)
train = optimizer.minimize(loss,name="train")

# init

init = tf.global_variables_initializer()
merged = tf.summary.merge_all()

saver = tf.train.Saver()

data = data.data()

# run graph
with tf.Session() as sess:
    sess.run(init)
    writer = tf.summary.FileWriter("./log",sess.graph)
    for step in range(0, 2000000):
        if(step%1000 == 0):
            saver.save(sess, "./trained_model/dimension_keep_cell/model")

        # get data
        train_data = data.get_batch_train_data()
        train_data_input = train_data[:,0:13]
        train_data_output = train_data[:,13].reshape(train_data_input.shape[0],1)

        sess.run(train,feed_dict={input_x:train_data_input, input_y:train_data_output})
        summary = \
        sess.run(merged,feed_dict={input_x:train_data_input,input_y:train_data_output})
        writer.add_summary(summary, step)

        if step % 500 == 0:
            # can't name this variable loss, it will overwrite the tensor in the 
            # graph
            my_loss = sess.run(loss,feed_dict={input_x:train_data_input,input_y:train_data_output})
            my_y   = sess.run(y,feed_dict={input_x:train_data_input,input_y:train_data_output})
            my_accurate = tool.get_accuracy_rate(my_y,train_data_output)
            print("step="+str(step)+" "+str(my_loss)+" accuracy is "+ \
                    str(my_accurate))
