import numpy as np

#data going into our neural network. 
input_data = np.array([[0,0,1],
                       [0,1,1]
                       [1,0,1],
                       [1,1,1]])

output_labels = np.array([[0],
                          [1],
                          [1],
                          [1]])

#sigmoid activation function
def activate(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))

#weight values

synaptic_weight_0 = 2*np.random.random((3,4)) - 1
synaptic_weight_1 = 2*np.random.random((4,1)) - 1

print 'weight matrix 1: ', synaptic_weight_0

for j in xrange(60000):

