import numpy as np
from random import uniform
import math

hiddennodes = 10
onodes = 6

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
        af = lambda x: sig(x)               # activation function
        # TODO: figure out a better activation function
        h1 = af(np.dot(self.wih, currGameState))  # hidden layer
        out = af(np.dot(self.who, h1))          # output layer
      
        # fix the outputs to be readable
        # TODO: put this in a better spot
        out[1] = int(math.floor(out[1]*2))
        out[3] = int(math.floor(out[3]*5))
        out[4] = int(math.floor(out[4]*6)) - 1
        return out





#test1 = np.random.uniform(-1,1,(hiddennodes,37))
#test2 = np.random.uniform(-1,1,(onodes,hiddennodes))
#x = bot(test1, test2)
#testinput = np.random.uniform(-1,1, (37, 1))
#print(x.think(testinput))
#print(np.random.uniform(-1, 1, (4, 3))) # This is code to generate a 4x3 matrix with random values from -1 to 1
                                        # represents one hidden layer
#print(np.dot(100, np.random.uniform(-1,1,(4,3))))

#testinput = np.random.uniform(-1,1, (37, 1))
#hiddennodes = 10
#onodes = 6

#af = lambda x: sig(x)               # activation function

#middle = af(np.dot(test1, testinput))
#out = af(np.dot(test2, middle))
#print(test1)
#print(out)
