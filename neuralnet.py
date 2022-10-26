#   June 17th, 2022, 12:10PM Friday
#   Mohamad Chahadeh, ©2022
#   https://MoChahadeh.github.io/
#   https://twitter.com/MoChahadeh

# Libraries and classes
import numpy as np
import json
import datetime


# ReLU Activation function for layers
def ReLU(Z):

    return np.maximum(0, Z )

# Sigmoid Activation function for layers
def sigmoid(Z):

    return 1/(1+np.exp(-Z))


# Neural Network Class
class NeuralNet():

    # class constructor
    def __init__(self, i:int, h1:int, h2, o:int):

        # Initalizing Weights and biases with random numbers between -0.5 and +0.5
        self.W1:np.ndarray = (np.random.rand(h1, i) - 0.5)*3
        self.b1:np.ndarray = (np.random.rand(h1, 1) - 0.5)*3
        # self.W2:np.ndarray = (np.random.rand(h2, h1) -0.5)*5
        # self.b2:np.ndarray = (np.random.rand(h2,1) -0.5)*5
        self.W3:np.ndarray = (np.random.rand(o, h1) -0.5)*3
        self.b3:np.ndarray = (np.random.rand(o,1) -0.5)*3
    
    # forward propogation
    def forward(self, inputs: np.ndarray):

        Z1 = np.dot(self.W1,np.transpose(inputs)) + self.b1     # first hidden layer, takes the transpose input array as inputs
        A1 = ReLU(Z1)    # sigmoid activation for hidden layer

        # Z2 = np.dot(self.W2, A1) + self.b2  # output layer, takes activation function of previous layer as input.
        # A2 = ReLU(Z2)    # sigmoid activation for output layer

        Z3 = np.dot(self.W3, A1) + self.b3  # output layer, takes activation function of previous layer as input.
        A3 = sigmoid(Z3)    # sigmoid activation for output layer

        return A3   # Activation for output layer, having dimensions of "o" rows and one column
    
    # mutation of network
    def mutate(self, rate):

        # getting the number rows and columns of each variable
        # making a random matrix of the same shape with values between -rate and +rate, multipling it by the previous values then adding it
        # Effectively changing each value in the matrix by a random rate between -+rate of its previous value..

        W1r, W1c = self.W1.shape 
        self.W1 = self.W1 + (self.W1 * (np.random.rand(W1r, W1c) - 0.5) / (0.5/rate))
        b1r, b1c = self.b1.shape
        self.b1 = self.b1 + (self.b1 * (np.random.rand(b1r, b1c) - 0.5) / (0.5/rate))
        # W2r, W2c = self.W2.shape
        # self.W2 = self.W2 + (self.W2 * (np.random.rand(W2r, W2c) - 0.5) / (0.5/rate))
        # b2r, b2c = self.b2.shape
        # self.b2 = self.b2 + (self.b2 * (np.random.rand(b2r, b2c) - 0.5) / (0.5/rate))
        W3r, W3c = self.W3.shape
        self.W3 = self.W3 + (self.W3 * (np.random.rand(W3r, W3c) - 0.5) / (0.5/rate))
        b3r, b3c = self.b3.shape
        self.b3 = self.b3 + (self.b3 * (np.random.rand(b3r, b3c) - 0.5) / (0.5/rate))

    def save(self):

        date = datetime.datetime.now()
        self.dict = {
            "W1" : self.W1.tolist(),
            "b1" : self.b1.tolist(),
            # "W2" : self.W2.tolist(),
            # "b2" : self.b2.tolist(),
            "W3" : self.W3.tolist(),
            "b3" : self.b3.tolist()
        }

        json_object = json.dumps(self.dict, indent = None)
        with open(f"model-{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}-{date.second}.json", "w") as outfile:
            outfile.write(json_object)
    
    def load(self, filepath):

        with open(filepath) as json_file:
            data = json.load(json_file)
            self.W1 = np.array(data["W1"])
            self.b1 = np.array(data["b1"])
            # self.W2 = np.array(data["W2"])
            # self.b2 = np.array(data["b2"])
            self.W3 = np.array(data["W3"])
            self.b3 = np.array(data["b3"])

