import tensorflow as tf
import tools
def net(x, n_classes):
    with tf.name_scope('net'):
        x = tools.conv('conv1_1',x,32,kernel_size=[5,5],stride=[1,1,1,1])
        x = tools.pool('pool1',x)

        x = tools.conv('conv2_1',x,64,kernel_size=[5,5],stride=[1,1,1,1])
        x = tools.pool('pool2',x)
        x = tools.fc_layer('fc_layer1',x,1024)
        x = tools.fc_layer('fc_layer2',x,10)
        return x



        


