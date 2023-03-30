import numpy as np
from random import uniform
import math
from torch import nn
import torch

hiddennodes = 10
onodes = 6

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(6, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork().to("cpu")
print(model)
X = torch.rand(1, 3, 2)
print(X)
logits = model(X)
print(logits)
pred_probab = nn.Softmax(dim=1)(logits)
y_pred = pred_probab.argmax(1)
print(f"Predicted class: {y_pred}")

def sig(x):
 return 1 / (1 + np.exp(-x))

class Bot():
    def __init__(self, wih=None, who=None, name=None):
        self.wih = wih
        self.who = who

        self.name = name

    def getMove(self, currGameState):
        # Run the NN
        out = self.think(currGameState)
        print(out)
        
        # Determine what the highest valued action is, make this have fewer magic numbers in the future
        if out[0] >= out[2] and out[0] >= out[5]:
            return [1, int(out[1])]
        elif out[2] >= out[5]:
            return [2, [int(out[3]), int(out[4])]]
        else:
            return [4]
        
    # NEURAL NETWORK
    def think(self, currGameState):

        # SIMPLE MLP
        af = lambda x: np.maximum(0,x)               # activation function
        af2 = lambda x: sig(x)
        # TODO: figure out a better activation function
        h1 = af(np.dot(self.wih, currGameState))  # hidden layer
        out = af2(np.dot(self.who, h1))          # output layer
      
        # fix the outputs to be readable
        # TODO: put this in a better spot
        out[1] = min(int(math.floor(out[1]*5)), 4) # This is dumb because it is dependent on number of distinct cards
        out[3] = min(int(math.floor(out[3]*5)), 4)
        out[4] = min(int(math.floor(out[4]*6)) - 1, 4)
        return out






#test1 = np.random.uniform(-1,1,(hiddennodes,37))
#test2 = np.random.uniform(-1,1,(onodes,hiddennodes))
#x = bot(test1, test2)
#testinput = np.random.uniform(-1,1, (37, 1))
#print(x.think(testinput))
#print(np.random.uniform(-1, 1, (4, 3))) # This is code to generate a 4x3 matrix with random values from -1 to 1
                                        # represents one hidden layer
#print(np.dot(100, np.random.uniform(-1,1,(4,3))))

#testinput = np.random.uniform(0, 1, (37, 1))
#hiddennodes = 10
#onodes = 6

#af = lambda x: np.maximum(0,x)               # activation function
#af2 = lambda x: sig(x)

#middle = af(np.dot(test1, testinput))
#out = af2(np.dot(test2, middle))
#print(test1)
#print(middle)
#print(out)
