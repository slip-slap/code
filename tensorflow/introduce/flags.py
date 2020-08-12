import tensorflow as tf

tf.app.flags.DEFINE_integer("batch_size", 64, "the default batch is 64")
tf.app.flags.DEFINE_float("dropout_keep_prob", 0.5, "the default keep probability is 0.5")

FLAGS = tf.app.flags.FLAGS

def main(_):
    print(FLAGS.batch_size)
    print(FLAGS.dropout_keep_prob)

if __name__ == '__main__':
    tf.app.run()


