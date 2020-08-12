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

        my_data = data.data()

        with tf.Session() as sess:
            saver.restore(sess, tf.train.latest_checkpoint(checkpoint))
            # get data
            train_data = my_data.get_batch_train_data()
            train_data_input = train_data[:,0:13]
            train_data_output = train_data[:,13].reshape(train_data_input.shape[0],1)
            my_loss = sess.run(loss,feed_dict={input_x:train_data_input,input_y:train_data_output})
    return my_loss;


loss = get_cell_result(\
        meta_graph="./trained_model/dimension_keep_cell/model.meta",\
        checkpoint='./trained_model/dimension_keep_cell')
print(loss)

