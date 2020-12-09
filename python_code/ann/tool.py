import numpy as np


def binary_to_decimal(binary_number):
    """TODO: Docstring for binary_to_decimal.
    :returns: decimal value
    """
    decimal = 0
    for i in range(len(binary_number)):
        decimal = decimal + binary_number[i]*np.power(2,len(binary_number)-i-1)
    return int(decimal)

"""
def get_result(neural_network_result):
    if(neural_network_result<=0.125):
        return  0
    elif(neural_network_result>=0.125 and neural_network_result <= 0.25+0.125):
        return  0.25
    elif(neural_network_result>=0.25+0.125 and neural_network_result <= 0.5+0.125):
        return  0.5
    elif(neural_network_result>=0.5+0.125 and neural_network_result <= 0.75+0.125):
        return 0.75
    else:
        return 1
"""

def get_result(neural_network_result):
    if(neural_network_result<=0.5):
        return  0
    else:
        return 1

def get_accuracy_rate(test_result, actual_result):
    """TODO: Docstring for .
    :arg1: numpy array
    :arg2: numpy array
    """
    correct_counter = 0
    for i in range(test_result.shape[0]):
        for j in range(test_result.shape[1]):
            result = get_result(test_result[i,j])
            if(np.abs(result - actual_result[i][j]) <= 0.001):
                correct_counter = correct_counter + 1;
   
    experiment_number = np.multiply(test_result.shape[0],test_result.shape[1])
    return np.divide(correct_counter, experiment_number)
