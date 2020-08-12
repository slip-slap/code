import numpy as np
import tensorflow as tf
import data
import tool

my_data = data.data()
test_data= my_data.get_test_data()
test_data_input = test_data[:,0:13]
test_data_output = test_data[:,13].reshape(test_data_input.shape[0],1)

def get_cell_result(train_data_input, train_data_output, \
        meta_graph="", checkpoint=""):
    g1 = tf.Graph()
    with g1.as_default() as g:
        saver = tf.train.import_meta_graph(meta_graph)
        input_x = g.get_tensor_by_name("input_x:0")
        input_y = g.get_tensor_by_name("input_y:0")
        output  = g.get_tensor_by_name("last_layer/result:0")
        with tf.Session() as sess:
            saver.restore(sess, tf.train.latest_checkpoint(checkpoint))

            my_output = sess.run(output, \
                    feed_dict={input_x:train_data_input,input_y:train_data_output})


            my_accurate = tool.get_accuracy_rate(my_output,train_data_output)
            print(" experiment accuracy is "+ \
                        str(my_accurate))
    return my_accurate

if __name__=='__main__':
    accurate = get_cell_result(test_data_input, test_data_output, \
            meta_graph="./trained_model/chrosome/model.meta",\
            checkpoint='./trained_model/chrosome')
    print(" accuracy is "+  str(accurate))
"""
    feature_result2 = get_cell_result(test_data_input, test_data_output, \
            meta_graph="./trained_model/feature2_cell/model.meta",\
            checkpoint='./trained_model/feature2_cell')
    feature_result3 = get_cell_result(test_data_input, test_data_output, \
            meta_graph="./trained_model/feature3_cell/model.meta",\
            checkpoint='./trained_model/feature3_cell')
    feature_result4 = get_cell_result(test_data_input, test_data_output, \
            meta_graph="./trained_model/feature4_cell/model.meta",\
            checkpoint='./trained_model/feature4_cell')



# combniationg model
    test_data_input = np.concatenate((feature_result2, \
        feature_result1,feature_result3,feature_result4), 1)
    normal_result = get_cell_result(test_data_input, test_data_output, \
            meta_graph="./trained_model/combination/model.meta",\
            checkpoint='./trained_model/combination')
"""

