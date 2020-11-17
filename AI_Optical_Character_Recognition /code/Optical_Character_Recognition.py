import numpy as np
import neurolab as nl

input_file = 'letter.data'

num_datapts = 50

# String containing all the distinct characters
o_label = 'omandig'

num_o_label = len(o_label)

# Defin the training and testing parameters
num_train = int(0.9 * num_datapts)
num_test = num_datapts - num_train

# Defining the dataset extraction parameters 
start = 6
end = -1

# Creating the dataset
data = []
labels = []
with open(input_fileile, 'r') as f:
    for line in f.readlines():
        list_values = line.split('\t')

        # Checking if the label is in ground truth 
        # labels. If not, skip it.
        if list_values[1] not in o_label:
            continue

        label = np.zeros((num_o_label, 1))
        label[o_label.index(list_values[1])] = 1
        labels.append(label)

        # Extracting the character vector and appending it to the main list
        current_char = np.array([float(x) for x in list_values[start:end]])
        data.append(current_char)

        if len(data) >= num_datapts:
            break

# Converting the data and labels to numpy arrays
data = np.asfarray(data)
labels = np.array(labels).reshape(num_datapts, num_o_label)

# Extracting the number of dimensions
num_dimensions = len(data[0])

# Create a feedforward neural network
nn = nl.net.newff([[0, 1] for _ in range(len(data[0]))], 
        [128, 16, num_o_label])

# Training algorithm to be used is gradient descent
nn.trainf = nl.train.train_gd

# Training the network
error_progress = nn.train(data[:num_train,:], labels[:num_train,:], 
        epochs=10000, show=100, goal=0.01)

# Predicting the output for test inputs 
print('\nTesting on unknown data:')
predicted_test = nn.sim(data[num_train:, :])
for i in range(num_test):
    print('\nOriginal:', o_label[np.argmax(labels[i])])
    print('Predicted:', o_label[np.argmax(predicted_test[i])])

