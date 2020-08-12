import tensorflow as tf

for serialized_example in tf.python_io.tf_record_iterator("/Users/kismet/Desktop/datatf"):
    example = tf.train.Example()
    example.ParseFromString(serialized_example)

    label = example.features.feature['label'].int64_list.value

    print(label) 
