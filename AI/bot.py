import numpy as np
from random import uniform

def sig(x):
 return 1 / (1 + np.exp(-x))

class bot():
    def __init__(self, wih=None, who=None, name=None):
        # Right now the bot itself keeps track of the wins and losses it receives,
        # maybe this is not ideal, we should have a separate AI for going first and going second
        self.winsFirst = 0
        self.winsSecond = 0
        self.lossesFirst = 0
        self.lossesSecond = 0

        self.wih = wih
        self.who = who

        self.name = name

    def getMove(self, currGameState):
        # Run the NN
        actionArray = think(currGameState)
        
        # Determine what the highest valued action is, make this have fewer magic numbers in the future
        if out[0] >= out[2] and out[0] >= out[5]:
            return [1, out[1]]
        elif out[2] >= out[5]:
            return [2, [out[3], out[4]]]
        else:
            return [4]
        
    # NEURAL NETWORK
    def think(self, currGameState):

        # SIMPLE MLP
        af = lambda x: sig(x)               # activation function
        # TODO: figure out a better activation function
        h1 = af(np.dot(self.wih, currGameState))  # hidden layer
        out = af(np.dot(self.who, h1))          # output layer
        return out



x = bot()
#print(np.random.uniform(-1, 1, (4, 3))) # This is code to generate a 4x3 matrix with random values from -1 to 1
                                        # represents one hidden layer
#print(np.dot(100, np.random.uniform(-1,1,(4,3))))

testinput = np.random.uniform(-1,1, (37, 1))
hiddennodes = 10
onodes = 6

af = lambda x: sig(x)               # activation function
test1 = np.random.uniform(-1,1,(hiddennodes,37))
test2 = np.random.uniform(-1,1,(onodes,hiddennodes))
middle = af(np.dot(test1, testinput))
out = af(np.dot(test2, middle))
print(test1)
print(out)
