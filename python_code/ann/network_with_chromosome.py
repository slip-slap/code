import tensorflow as tf
import data
import tool
import numpy as np
import yaml

CONFIGURATION = None;
with open('configuration.yaml') as input_stream:
    CONFIGURATION = yaml.load(input_stream, Loader=yaml.FullLoader)


def activation_function(input_data,activation_function_code=0):
    if(activation_function_code == 0):
        y = tf.sigmoid(input_data,name="sigmoid_function")
    if(activation_function_code == 1):
        y = tf.nn.relu(input_data,name="relu_function")
    if(activation_function_code == 2):
        y = tf.nn.tanh(input_data,name="tanh_function")
    if(activation_function_code == 3):
        y = tf.nn.softmax(input_data,name="softmax_function")
    return y


def gene_unit_to_node(input_data,node_name,gene_unit,activation_function_unit):
    #layerout = tf.Variable(tf.zeros([input_data.shape[0],1]),trainable=False)
    layer_output = tf.Variable(tf.zeros([CONFIGURATION['BATCH'],1]),trainable=False)
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
        activation_function_code = tool.binary_to_decimal(activation_function_unit)
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
        w = tf.get_variable(name="weight",shape=[input_data.shape[-1],CONFIGURATION['NUMBER_OF_OUTPUTS']])
        b = tf.get_variable(name="bias",shape=[CONFIGURATION['NUMBER_OF_OUTPUTS']])
        y = tf.matmul(input_data,w)
        y = tf.add(y,b)
        y = tf.nn.relu(y,name="result")
    return y

def train_network(chromosome,activation_function_chromosome):
    tf.reset_default_graph()
    input_x = tf.placeholder("float", [None,CONFIGURATION['NUMBER_OF_INPUTS']],name="input_x")
    input_y = tf.placeholder("float", [None,CONFIGURATION['NUMBER_OF_OUTPUTS']],name="input_y")


    layer_output = \
    chromosome_to_layer(input_x,chromosome,activation_function_chromosome)
    y = last_layer(layer_output)


# loss
    loss = tf.reduce_mean(tf.square(y - input_y),name="loss")
    summary_loss = tf.summary.scalar(name="loss",tensor=loss)
    optimizer = tf.train.GradientDescentOptimizer(CONFIGURATION['LEARNING_RATE'])
    train = optimizer.minimize(loss,name="train")

# init

    init = tf.global_variables_initializer()
    merged = tf.summary.merge_all()
    saver = tf.train.Saver()
    my_data = data.data(
            batch=CONFIGURATION["BATCH"],total_data_number=CONFIGURATION['TOTAL_DATA_NUMBER'],
            training_percent=CONFIGURATION["TRAINING_PERCENT"],
            file_path=CONFIGURATION["FILE_PATH"],file_name=CONFIGURATION["FILE_NAME"])

    previous_loss= 0
    current_loss= 0.01 
    step = 0
# run graph
    with tf.Session() as sess:
        sess.run(init)
        writer = \
            tf.summary.FileWriter(CONFIGURATION["SAVING_PLACE_OF_TRAINING_MODEL"],sess.graph)
        while(np.abs(current_loss- previous_loss)> 0.000001):
            step = step + 1
            # get data
            train_data = my_data.get_batch_train_data()
            train_data_input = train_data[:,0:CONFIGURATION['NUMBER_OF_INPUTS']]
            train_data_output = \
            train_data[:,CONFIGURATION['NUMBER_OF_INPUTS']:CONFIGURATION['NUMBER_OF_INPUTS']
                    + \
                    CONFIGURATION['NUMBER_OF_OUTPUTS']].reshape(train_data_input.shape[0],CONFIGURATION['NUMBER_OF_OUTPUTS'])

            sess.run(train,feed_dict={input_x:train_data_input, input_y:train_data_output})
            summary = \
            sess.run(merged,feed_dict={input_x:train_data_input,input_y:train_data_output})
            writer.add_summary(summary, step)
            if step % CONFIGURATION['NUMBER_OF_TRAINING_SAVE_STATE']== 0:
                # can't name this variable loss, it will overwrite the tensor in the 
                # graph
                my_loss = sess.run(loss,feed_dict={input_x:train_data_input,input_y:train_data_output})
                saver.save(sess, CONFIGURATION["SAVING_PLACE_OF_TRAINING_PROCESS"])
                summary = sess.run(merged,feed_dict={input_x:train_data_input, input_y:train_data_output})
                writer.add_summary(summary,step)
                my_y   = sess.run(y,feed_dict={input_x:train_data_input,input_y:train_data_output})
                my_accurate = tool.get_accuracy_rate(my_y,train_data_output)
                print("step="+str(step)+" "+str(my_loss)+" accuracy is "+ \
                            str(my_accurate))
                previous_loss= current_loss
                current_loss= my_loss

def get_activation_function_gene(number=5):
    gene = list()
    for i in range(5):
        a = int(np.random.randint(0,2,1))
        b = int(np.random.randint(0,2,1))
        gene.append([a,b])
    return gene

def get_connection_gene(number=5):
    chromosome = list()
    for i in range(5):
        gene_unit = np.random.randint(0,2,(CONFIGURATION['NUMBER_OF_INPUTS']))
        chromosome.append(gene_unit)
    return chromosome

if __name__=="__main__":
    train_network(get_connection_gene(), get_activation_function_gene())
    print("train is over")

