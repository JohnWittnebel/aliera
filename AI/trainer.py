import numpy as np
from random import uniform
import math
import pickle
from torch import nn
from torch.masked import masked_tensor
import torch
from bot import NeuralNetwork, inodes, onodes

class Trainer():
    def __init__(self):
        return

    def loss_fn():
        return

    def train_one_epoch():
        return

trainer = Trainer()

# Code to load NN parameters
model = NeuralNetwork().to("cpu")
model.load_state_dict(torch.load("./botModels/gen1.bot"))
model.eval()

# Code to load training data
data_file = open("./trainingData/pos1690.pickle", "rb")
posData = pickle.load(data_file)
data_file.close()

# Code to get the test run MCTS output, this should be done during the test runs for the future
indexes = posData[2].nonzero(as_tuple = False)
myOtherCoolTensor = []
nextToInsert = 0
for i in range(onodes - 1):
    if i in indexes:
        myOtherCoolTensor.append(posData[1][nextToInsert])
        nextToInsert += 1
    else:
        myOtherCoolTensor.append(0.)

actOutput = torch.tensor(myOtherCoolTensor)

# Code to get the normalized NN MCTS prediction
prediction = model(posData[0])
myCoolTensor = torch.where(posData[2], prediction[0], float('-inf'))
predictedOutput = nn.Softmax(dim=0)(myCoolTensor)

# Loss
print(nn.CrossEntropyLoss()(predictedOutput, actOutput))
