import tensorflow as tf
import data
import tool
import net_cell
import numpy as np
import valuation



train_data= data.get_train_data(number=100)
#train_data= data.get_test_data()
train_data_input = train_data[:,0:13]
train_data_output = train_data[:,13].reshape(100,1)

feature_result1= valuation.get_cell_result(train_data_input, train_data_output, \
        meta_graph="./trained_model/feature_cell/model.meta",\
        checkpoint='./trained_model/feature_cell')
feature_result2 = valuation.get_cell_result(train_data_input, train_data_output, \
        meta_graph="./trained_model/feature2_cell/model.meta",\
        checkpoint='./trained_model/feature2_cell')
feature_result3 = valuation.get_cell_result(train_data_input, train_data_output, \
        meta_graph="./trained_model/feature3_cell/model.meta",\
        checkpoint='./trained_model/feature3_cell')
feature_result4 = valuation.get_cell_result(train_data_input, train_data_output, \
        meta_graph="./trained_model/feature4_cell/model.meta",\
        checkpoint='./trained_model/feature4_cell')

train_data_input = np.concatenate((feature_result1, feature_result2, \
    feature_result3, feature_result4),1)



g = tf.Graph()
with g.as_default() as g:
    input_x = tf.placeholder("float", [None,4],name="input_x")
    input_y = tf.placeholder("float", [None,1],name="input_y")

    y = net_cell.combine_cell(input_x)
# loss
    loss = tf.reduce_mean(tf.square(y - input_y))
    summary_loss = tf.summary.scalar(name="loss",tensor=loss)
    optimizer = tf.train.GradientDescentOptimizer(0.1)
    train = optimizer.minimize(loss)

# init

    init = tf.global_variables_initializer()
    merged = tf.summary.merge_all()

    saver = tf.train.Saver()

# run graph
    with tf.Session() as sess:
        sess.run(init)
        writer = tf.summary.FileWriter("./log",sess.graph)


        for step in range(0, 2000000):
            sess.run(train,feed_dict={input_x:train_data_input, input_y:train_data_output})
            summary = \
            sess.run(merged,feed_dict={input_x:train_data_input,input_y:train_data_output})
            writer.add_summary(summary, step)
            if step % 500 == 0:
                # can't name this variable loss, it will overwrite the tensor in the 
                # graph
                saver.save(sess, "./trained_model/combination/model")
                my_loss = sess.run(loss,feed_dict={input_x:train_data_input,input_y:train_data_output})
                my_y   = sess.run(y,feed_dict={input_x:train_data_input,input_y:train_data_output})
                my_accurate = tool.get_accuracy_rate(my_y,train_data_output)
                print("step="+str(step)+" "+str(my_loss)+" accuracy is "+ \
                        str(my_accurate))
