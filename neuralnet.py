#   June 17th, 2022, 12:10PM Friday
#   Mohamad Chahadeh, ©2022
#   https://MoChahadeh.github.io/
#   https://twitter.com/MoChahadeh

# Libraries and classes
import numpy as np


# ReLU Activation function for layers
def ReLU(Z):

    return np.maximum(0, Z )

# Sigmoid Activation function for layers
def sigmoid(Z):

    return 1/(1+np.exp(-Z))


# Neural Network Class
class NeuralNet():

    # class constructor
    def __init__(self, i:int, h:int, o:int):

        # Initalizing Weights and biases with random numbers between -0.5 and +0.5
        self.W1:np.ndarray = np.random.rand(h, i) - 0.5
        self.b1:np.ndarray = np.random.rand(h, 1) - 0.5
        self.W2:np.ndarray = np.random.rand(o, h) -0.5
        self.b2:np.ndarray = np.random.rand(o,1) -0.5
    
    # forward propogation
    def forward(self, inputs: np.ndarray):

        Z1 = np.dot(self.W1,np.transpose(inputs)) + self.b1     # first hidden layer, takes the transpose input array as inputs
        A1 = sigmoid(Z1)    # sigmoid activation for hidden layer

        Z2 = np.dot(self.W2, A1) + self.b2  # output layer, takes activation function of previous layer as input.
        A2 = sigmoid(Z2)    # sigmoid activation for output layer

        return A2   # Activation for output layer, having dimensions of "o" rows and one column
    
    # mutation of network
    def mutate(self, rate):

        # getting the number rows and columns of each variable
        # making a random matrix of the same shape with values between -rate and +rate, multipling it by the previous values then adding it
        # Effectively changing each value in the matrix by a random rate between -+rate of its previous value..

        W1r, W1c = self.W1.shape 
        self.W1 = self.W1 + (self.W1 * (np.random.rand(W1r, W1c) - 0.5) / (0.5/rate))
        b1r, b1c = self.b1.shape
        self.b1 = self.b1 + (self.b1 * (np.random.rand(b1r, b1c) - 0.5) / (0.5/rate))
        W2r, W2c = self.W2.shape
        self.W2 = self.W2 + (self.W2 * (np.random.rand(W2r, W2c) - 0.5) / (0.5/rate))
        b2r, b2c = self.b2.shape
        self.b2 = self.b2 + (self.b2 * (np.random.rand(b2r, b2c) - 0.5) / (0.5/rate))
