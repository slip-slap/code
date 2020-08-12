import tensorflow as tf

def read_and_decode(filename):
    filename_queue = tf.train.string_input_producer([filename])

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw' : tf.FixedLenFeature([], tf.string),
                                       })

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [224, 224, 3])
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
    label = tf.cast(features['label'], tf.int32)

    return label

if __name__ == '__main__':
    label = read_and_decode("/Users/kismet/Desktop/datatf")

    label_batch = tf.train.shuffle_batch([label],
                                                    batch_size=30, capacity=2000,
                                                    min_after_dequeue=1000)
    #初始化所有的op
    init = tf.initialize_all_variables()

    with tf.Session() as sess:
        sess.run(init)
	#启动队列
        threads = tf.train.start_queue_runners(sess=sess)
        for i in range(3):
            l= sess.run(label_batch)
            #l = to_categorical(l, 12)
            print(l)

