import numpy as np
import tensorflow as tf
import data
import tool


def dimision_keep_cell(x):
    y1 = layer("first",x,39)
    y1_slice1 = tf.slice(y1,[0,0],[-1,26])
    y1_slice2 = tf.slice(y1,[0,26],[-1,13])
    y2 = layer("second", y1_slice1, 13)
    y3_input = tf.concat(axis=1, values=[y2, y1_slice2], name="my_slice")
    y3  = layer("last", y3_input, 1)
    return y3


def normal_net_cell(x):
    y1 = layer("first",x,3)
    y1_slice1 = tf.slice(y1,[0,0],[-1,2])
    y1_slice2 = tf.slice(y1,[0,2],[-1,-1])
    y2 = layer("second", y1_slice1, 1)
    y3_input = tf.concat(axis=1, values=[y2, y1_slice2], name="my_slice")
    y3  = layer("last", y3_input, 1)
    return y3
# obtain data

def feature_net_cell(x):
    y1 = layer("first",x,6)
    y  = layer("last",y1,1)
    return y

def feature2_net_cell(x):
    y1 = layer("first",x,7)
    y  = layer("last",y1,1)
    return y
def feature3_net_cell(x):
    y1 = layer("first",x,8)
    y  = layer("last",y1,1)
    return y

def feature4_net_cell(x):
    y1 = layer("first",x,9)
    y  = layer("last",y1,1)
    return y

def combine_cell(x):
    y  = layer("last", x, 1)
    return y





# for internal use, module programming
def layer(layer_name, data, output_channels):
    with tf.variable_scope(layer_name,reuse=tf.AUTO_REUSE):
        w = tf.get_variable(name="weight",shape=[data.shape[-1],output_channels])
        b = tf.get_variable(name="bias",shape=[output_channels])
        summary_bias = tf.summary.histogram("bias",b)
        y = tf.matmul(data,w)
        y = tf.add(y,b)
        y = tf.sigmoid(y,name="result")
    return y

