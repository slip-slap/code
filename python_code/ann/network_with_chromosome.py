import tensorflow as tf
import data
import tool
import net_cell
import numpy as np


def binary_to_decimal(binary_number):
    """TODO: Docstring for binary_to_decimal.
    :returns: decimal value
    """
    decimal = 0
    for i in range(len(binary_number)):
        decimal = decimal + binary_number[i]*np.power(2,len(binary_number)-i-1)
    return int(decimal)

def activation_function(input_data,activation_function_code=0):
    if(activation_function_code == 0):
        y = tf.sigmoid(input_data,name="result")
        #print("activation_function is sigmoid")
    if(activation_function_code == 1):
        y = tf.nn.relu(input_data,name="result")
        #y = tf.sigmoid(input_data,name="result")
        #print("activation_function is relu")
    if(activation_function_code == 2):
        y = tf.nn.tanh(input_data,name="result")
        #y = tf.sigmoid(input_data,name="result")
        #print("activation_function is tanh")
    if(activation_function_code == 3):
        y = tf.nn.softmax(input_data,name="result")
        #y = tf.sigmoid(input_data,name="result")
        #print("activation_function is softmax")
    return y




def gene_unit_to_node(input_data,node_name,gene_unit,activation_function_unit):
    #layerout = tf.Variable(tf.zeros([input_data.shape[0],1]),trainable=False)
    layer_output = tf.Variable(tf.zeros([60,1]),trainable=False)
    for i in range(len(gene_unit)):
            if(gene_unit[i]==1):
                temp_slice = tf.slice(input_data,[0,i],[-1,1])
                layer_output = tf.concat(axis=1, values=[layer_output,temp_slice])
    layer_output = tf.slice(layer_output,[0,1],[-1,-1])

    with tf.variable_scope(node_name,reuse=tf.AUTO_REUSE):
        w = tf.get_variable(name="weight",shape=[sum(gene_unit),1])
        weight_summary = tf.summary.histogram("weight",w)
        b = tf.get_variable(name="bias",shape=[1])
        y = tf.matmul(layer_output,w)
        y = tf.add(y,b)
        activation_function_code = binary_to_decimal(activation_function_unit)
        #y = tf.sigmoid(y,name="result")
        y = activation_function(y,activation_function_code)
    return y

def chromosome_to_layer(input_data,chromosome,activation_function_chromosome):
    layer_result = list()
    for i in range(len(chromosome)):
        node_result = \
        gene_unit_to_node(input_data,"node_"+str(i),chromosome[i],activation_function_chromosome[i])
        layer_result.append(node_result)
    with tf.variable_scope("first_layer",reuse=tf.AUTO_REUSE):   
        layer_output = tf.concat(axis=1, values=layer_result, name="layer_ouput")

    return layer_output

def last_layer(input_data):
    with tf.variable_scope("last_layer",reuse=tf.AUTO_REUSE):
        w = tf.get_variable(name="weight",shape=[input_data.shape[-1],1])
        b = tf.get_variable(name="bias",shape=[1])
        y = tf.matmul(input_data,w)
        y = tf.add(y,b)
        y = tf.sigmoid(y,name="result")
    return y

def train_network(chromosome,activation_function_chromosome):
    tf.reset_default_graph()
    input_x = tf.placeholder("float", [None,13],name="input_x")
    input_y = tf.placeholder("float", [None,1],name="input_y")


    layer_output = \
    chromosome_to_layer(input_x,chromosome,activation_function_chromosome)
    y = last_layer(layer_output)


# loss
    loss = tf.reduce_mean(tf.square(y - input_y),name="loss")
    summary_loss = tf.summary.scalar(name="loss",tensor=loss)
    optimizer = tf.train.GradientDescentOptimizer(0.02)
    train = optimizer.minimize(loss,name="train")

# init

    init = tf.global_variables_initializer()
    merged = tf.summary.merge_all()
    saver = tf.train.Saver()
    my_data = data.data()

    previous_loss= 0
    current_loss= 0.01 
    step = 0
# run graph
    with tf.Session() as sess:
        sess.run(init)
        #writer = tf.summary.FileWriter("./log",sess.graph)
        while(np.abs(current_loss- previous_loss)> 0.001):
            step = step + 1
            # get data
            train_data = my_data.get_batch_train_data()
            train_data_input = train_data[:,0:13]
            train_data_output = train_data[:,13].reshape(train_data_input.shape[0],1)
            sess.run(train,feed_dict={input_x:train_data_input, input_y:train_data_output})
            summary = \
            sess.run(merged,feed_dict={input_x:train_data_input,input_y:train_data_output})
            #writer.add_summary(summary, step)
            if step % 10000 == 0:
                # can't name this variable loss, it will overwrite the tensor in the 
                # graph
                my_loss = sess.run(loss,feed_dict={input_x:train_data_input,input_y:train_data_output})
                saver.save(sess, "./trained_model/chrosome/model")
                summary = sess.run(merged,feed_dict={input_x:train_data_input, input_y:train_data_output})
                #writer.add_summary(summary,step)
                my_y   = sess.run(y,feed_dict={input_x:train_data_input,input_y:train_data_output})
                my_accurate = tool.get_accuracy_rate(my_y,train_data_output)
                print("step="+str(step)+" "+str(my_loss)+" accuracy is "+ \
                            str(my_accurate))
                previous_loss= current_loss
                current_loss= my_loss

            


if __name__=="__main__":
    chromosome = list()
    for i in range(5):
        gene_unit = np.random.randint(0,2,(13))
        chromosome.append(gene_unit)
    train_network(chromosome,[[1,1],[0,0],[0,1],[1,0],[1,1]])
    print("train is over")
