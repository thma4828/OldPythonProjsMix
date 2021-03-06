import numpy as np
import random

"""
We will be building a feed forward network. Feed forward means
that we will map our output from our input patterns.
Rec Nets take time into account! (good for music, words, etc.)
h(t) = f(h, x(t), theta)
loss function is going to be negative log likelyhood!
we are using back propogation in this method to optimize error.
(minimize duh!)
we will be using gradient descent optimiztion
we connect each hidden state to previous hidden state
good for wheather data, video, ANY SEQUENTIAL DATA

1) Load training data.
    1a) encode chars into vectors
2) define the Recurrent Network
3) define the loss function
    3a)forward loss
    3b)loss
    3c)Backward pass
4)define model to create sentences from the model
5)train the network
    5a)feed the network
    5b)calculate gradient and update model
"""

data = open('kavka.txt', 'r').read()
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)
print('data has %d chars, %d unique'%(data_size, vocab_size))
#dictionary that matches char to number
char_to_ix = {ch:i for i, ch in enumerate(chars)}
#dictionary that maches number to char
ix_to_char = {i:ch for i, ch in enumerate(chars)}
#num nodes in hidden layer!
hidden_size = 93
#25 chars generated at every time step
seq_length = 20
#lower the learning rate the less outliers have an effect!
learning_rate = .005
#input weights
Wxh = np.random.randn(hidden_size, vocab_size) * 0.01
#recurrent weight matrix (h to h)
Whh = np.random.randn(hidden_size, hidden_size) * 0.01
Why = np.random.randn(vocab_size, hidden_size) * 0.01
#print(Wxh, Whh, Why)
bh = np.zeros((hidden_size, 1))
by = np.zeros((vocab_size, 1))

def lossFun(inputs, targets, hprev):
  """
  inputs,targets are both list of integers.
  hprev is Hx1 array of initial hidden state
  returns the loss, gradients on model parameters, and last hidden state
  """
  #store our inputs, hidden states, outputs, and probability values
  xs, hs, ys, ps, = {}, {}, {}, {} #Empty dicts
    # Each of these are going to be SEQ_LENGTH(Here 25) long dicts i.e. 1 vector per time(seq) step
    # xs will store 1 hot encoded input characters for each of 25 time steps (26, 25 times)
    # hs will store hidden state outputs for 25 time steps (100, 25 times)) plus a -1 indexed initial state
    # to calculate the hidden state at t = 0
    # ys will store targets i.e. expected outputs for 25 times (26, 25 times), unnormalized probabs
    # ps will take the ys and convert them to normalized probab for chars
    # We could have used lists BUT we need an entry with -1 to calc the 0th hidden layer
    # -1 as  a list index would wrap around to the final element
  xs, hs, ys, ps = {}, {}, {}, {}
  #init with previous hidden state
    # Using "=" would create a reference, this creates a whole separate copy
    # We don't want hs[-1] to automatically change if hprev is changed
  hs[-1] = np.copy(hprev)
  #init loss as 0
  loss = 0
  # forward pass
  for t in range(len(inputs)):
    xs[t] = np.zeros((vocab_size,1)) # encode in 1-of-k representation (we place a 0 vector as the t-th input)
    xs[t][inputs[t]] = 1 # Inside that t-th input we use the integer in "inputs" list to  set the correct
    hs[t] = np.tanh(np.dot(Wxh, xs[t]) + np.dot(Whh, hs[t-1]) + bh) # hidden state
    ys[t] = np.dot(Why, hs[t]) + by # unnormalized log probabilities for next chars
    ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t])) # probabilities for next chars
    loss += -np.log(ps[t][targets[t],0]) # softmax (cross-entropy loss)
  # backward pass: compute gradients going backwards
  #initalize vectors for gradient values for each set of weights
  dWxh, dWhh, dWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
  dbh, dby = np.zeros_like(bh), np.zeros_like(by)
  dhnext = np.zeros_like(hs[0])
  for t in reversed(range(len(inputs))):
    #output probabilities
    dy = np.copy(ps[t])
    #derive our first gradient
    dy[targets[t]] -= 1 # backprop into y
    #compute output gradient -  output times hidden states transpose
    #When we apply the transpose weight matrix,
    #we can think intuitively of this as moving the error backward
    #through the network, giving us some sort of measure of the error
    #at the output of the lth layer.
    #output gradient, moving error backwards in back propagation
    dWhy += np.dot(dy, hs[t].T)
    #derivative of output bias
    dby += dy
    #backpropagate into h!
    dh = np.dot(Why.T, dy) + dhnext # backprop into h
    dhraw = (1 - hs[t] * hs[t]) * dh # backprop through tanh nonlinearity
    dbh += dhraw #derivative of hidden bias
    dWxh += np.dot(dhraw, xs[t].T) #derivative of input to hidden layer weight
    dWhh += np.dot(dhraw, hs[t-1].T) #derivative of hidden layer to hidden layer weight
    dhnext = np.dot(Whh.T, dhraw)
    #now we can return all our gradient / derivative values
  for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
    np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients
  return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(inputs)-1]

def sample(h, seed_ix, n):
  """
  sample a sequence of integers from the model
  h is memory state, seed_ix is seed letter for first time step
  n is how many characters to predict
  """
  #create vector
  x = np.zeros((vocab_size, 1))
  #customize it for our seed char
  x[seed_ix] = 1
  #list to store generated chars
  ixes = []
  #for as many characters as we want to generate
  for t in range(n):
    #a hidden state at a given time step is a function
    #of the input at the same time step modified by a weight matrix
    #added to the hidden state of the previous time step
    #multiplied by its own hidden state to hidden state matrix.
    h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h) + bh)
    #compute output (unnormalised)
    y = np.dot(Why, h) + by
    ## probabilities for next chars
    p = np.exp(y) / np.sum(np.exp(y))
    #pick one with the highest probability
    ix = np.random.choice(range(vocab_size), p=p.ravel())
    #create a vector
    x = np.zeros((vocab_size, 1))
    #customize it for the predicted char
    x[ix] = 1
    #add it to the list
    ixes.append(ix)

  txt = ''.join(ix_to_char[ix] for ix in ixes)
  print('----\n %s \n----' % (txt, ))
hprev = np.zeros((hidden_size,1)) # reset RNN memory
#predict the 200 next characters given 'a'
sample(hprev,char_to_ix['a'],30)
p=0
inputs = [char_to_ix[ch] for ch in data[p:p+seq_length]]
print("inputs", inputs)
targets = [char_to_ix[ch] for ch in data[p+1:p+seq_length+1]]
print("targets", targets)

n, p = 0, 0
mWxh, mWhh, mWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
mbh, mby = np.zeros_like(bh), np.zeros_like(by) # memory variables for Adagrad
smooth_loss = -np.log(1.0/vocab_size)*seq_length # loss at iteration 0
while n<=1000*3000:
  # prepare inputs (we're sweeping from left to right in steps seq_length long)
  # check "How to feed the loss function to see how this part works
  if p+seq_length+1 >= len(data) or n == 0:
    hprev = np.zeros((hidden_size,1)) # reset RNN memory
    p = 0 # go from start of data
  inputs = [char_to_ix[ch] for ch in data[p:p+seq_length]]
  targets = [char_to_ix[ch] for ch in data[p+1:p+seq_length+1]]

  # forward seq_length characters through the net and fetch gradient
  loss, dWxh, dWhh, dWhy, dbh, dby, hprev = lossFun(inputs, targets, hprev)
  smooth_loss = smooth_loss * 0.999 + loss * 0.001

  # sample from the model now and then
  if n % 3000 == 0:
    print('iter %d out of 1000000 ||, loss: %f' % (n, smooth_loss))# print progress
    print('progress: ', float((100*n)/1000000), ' % percent complete!')
    sample(hprev, inputs[0], 500)

  # perform parameter update with Adagrad
  for param, dparam, mem in zip([Wxh, Whh, Why, bh, by],
                                [dWxh, dWhh, dWhy, dbh, dby],
                                [mWxh, mWhh, mWhy, mbh, mby]):
    mem += dparam * dparam
    param += -learning_rate * dparam / np.sqrt(mem + 1e-8) # adagrad update

  p += seq_length # move data pointer
  n += 1 # iteration counter












