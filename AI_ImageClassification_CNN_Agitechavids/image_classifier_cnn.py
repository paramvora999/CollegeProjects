#Image data used from Tensorflow in-built library for demonstrative purposes. Agitechavids Project included database collection and work on that specific category map.

import argparse

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

def build_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', dest='input_dir', type=str, 
            default='./mnist_data')
    return parser

def get_weight(shape):
    data = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(data)

def get_biase(shape):
    data = tf.constant(0.1, shape=shape)
    return tf.Variable(data)

def create_layer(shape):
    W = get_weight(shape)
    b = get_biase([shape[-1]])

    return W, b

def cnn_2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], 
            padding='SAME')

def max_pooling(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], 
            strides=[1, 2, 2, 1], padding='SAME')

if __name__ == '__main__':
    args = build_arg_parser().parse_args()

    mnist = input_data.read_data_sets(args.input_dir, one_hot=True)

    x = tf.placeholder(tf.float32, [None, 784])

    x_image = tf.reshape(x, [-1, 28, 28, 1])

    # Defining the first convolutional layer
    W_conv1, b_conv1 = create_layer([5, 5, 1, 32])

    # Convolving the image with weight tensor, and then adding the 
    # bias, and then applying the ReLU function
    h_conv1 = tf.nn.relu(convolution_2d(x_image, W_conv1) + b_conv1)

    h_pool1 = max_pooling(h_conv1)

    # Defining the second convolutional layer
    W_conv2, b_conv2 = create_layer([5, 5, 32, 64])

  
    h_conv2 = tf.nn.relu(convolution_2d(h_pool1, W_conv2) + b_conv2)

    h_pool2 = max_pooling(h_conv2)

    # Defining the fully connected layer
    W_fc1, b_fc1 = create_layer([7 * 7 * 64, 1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])

    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # Defining the readout layer (output layer)
    W_fc2, b_fc2 = create_layer([1024, 10])
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

    y_loss = tf.placeholder(tf.float32, [None, 10])
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_loss))
    optimiser = tf.train.AdamOptimizer(1e-4).minimize(loss)

    # Defining the accuracy computation
    predicted_val = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_loss, 1))
    accuracy_val = tf.reduce_mean(tf.cast(predicted, tf.float32))

    sess = tf.InteractiveSession()
    init = tf.initialize_all_variables()
    sess.run(init)

    num_iteration = 27000
    batch_size = 72
    
    for i in range(num_iteration):

        batch = mnist.train.next_batch(batch_size)

        if i % 50 == 0:
            cur_accuracy = accuracy.eval(feed_dict = {
                    x: batch[0], y_loss: batch[1], keep_prob: 1.0})
            print('Iteration', i, ', Accuracy =', cur_accuracy)
        
        optimiser.run(feed_dict = {x: batch[0], y_loss: batch[1], keep_prob: 0.5})

    print('Test accuracy =', accuracy.eval(feed_dict = {
            x: mnist.test.images, y_loss: mnist.test.labels, 
            keep_prob: 1.0}))

