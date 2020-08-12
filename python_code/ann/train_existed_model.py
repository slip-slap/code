import tensorflow as tf
import tool
import data

def get_cell_result(meta_graph="", checkpoint=""):
    g1 = tf.Graph()
    with g1.as_default() as g:
        saver = tf.train.import_meta_graph(meta_graph)
        input_x = g.get_tensor_by_name("input_x:0")
        input_y = g.get_tensor_by_name("input_y:0")
        loss  = g.get_tensor_by_name("loss:0")
        train = g.get_operation_by_name("train")
        output  = g.get_tensor_by_name("last/result:0")

        my_data = data.data()

        with tf.Session() as sess:
            saver.restore(sess, tf.train.latest_checkpoint(checkpoint))

            for step in range(800000):
                # get data
                train_data = my_data.get_batch_train_data()
                train_data_input = train_data[:,0:13]
                train_data_output = train_data[:,13].reshape(train_data_input.shape[0],1)
                if(step%2000 == 0):
                    saver.save(sess, "./trained_model/normal_cell/model")
                sess.run(train,feed_dict={input_x:train_data_input, input_y:train_data_output})
                if step % 1000 == 0:
                    # can't name this variable loss, it will overwrite the tensor in the 
                    # graph
                    my_loss = sess.run(loss,feed_dict={input_x:train_data_input,input_y:train_data_output})
                    my_y   = sess.run(output,feed_dict={input_x:train_data_input,input_y:train_data_output})
                    my_accurate = tool.get_accuracy_rate(my_y,train_data_output)
                    print("step="+str(step)+" "+str(my_loss)+" accuracy is "+ \
                            str(my_accurate))


feature_result1 = get_cell_result(\
        meta_graph="./trained_model/normal_cell/model.meta",\
        checkpoint='./trained_model/normal_cell')
