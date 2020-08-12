import tensorflow as tf

filename_queue = tf.train.string_input_producer(['/Users/kismet/Desktop/datatf'])

reader = tf.TFRecordReader()
_, serialized_example = reader.read(filename_queue)
features = tf.parse_single_example(serialized_example,
                                   features= {
                                       'label': tf.FixedLenFeature([],tf.int64),
                                       'img_raw': tf.FixedLenFeature([], tf.string)
                                   })
label = tf.cast(features['label'],tf.int32)
label_batch = tf.train.shuffle_batch([label],batch_size=2, capacity=2000,min_after_dequeue=1000)
with tf.Session() as sess:
    threads = tf.train.start_queue_runners(sess=sess)
    #label = sess.run(label)
    #print("the length is %d :"%label)
    for i in range(5):
        l=sess.run(label_batch)
        print(l)

