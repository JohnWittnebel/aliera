import numpy as np
from random import uniform
import math
import pickle
from torch import nn
from torch.masked import masked_tensor
import torch
from bot import NeuralNetwork, inodes, onodes
from dataset import PositionDataset
from torch.utils.data import DataLoader

class Trainer():
    def __init__(self):
        return

    def loss_fn():
        return

    def train_one_epoch():
        return
"""
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
print(actOutput)

# Code to get the normalized NN MCTS prediction
prediction = model(posData[0])
myCoolTensor = torch.where(posData[2], prediction[0], float('-inf'))
predictedOutput = nn.Softmax(dim=0)(myCoolTensor)

# Loss
print(nn.CrossEntropyLoss()(predictedOutput, actOutput))
"""

#mybatch = []
#for i in range(5):
#    data_file = open("./trainingData/pos" + str(i) + ".pickle", "rb")
#    posData = pickle.load(data_file)
#    data_file.close()
#    mybatch.append(posData[0])

#def AZLossFcn(predMTCS, actMTCS, predRes, actRes):
#    return nn.CrossEntropyLoss()(predMTCS, actMCTS)
training_data = PositionDataset("./trainingData")
loader = DataLoader(training_data, batch_size=7, shuffle=True)
model = NeuralNetwork().to("cpu")

#model(torch.as_tensor(mybatch))
#input("")

#model.load_state_dict(torch.load("./botModels/gen1.bot"))
model.eval()

#a,b,c,d = next(iter(loader))

#gamePos, train_MCTS, mask, train_result = list(next(iter(loader)))[0]
#print(gamePos)
n_epochs = 2
for epoch in range(n_epochs):
    x,y,a,b = next(iter(loader))
        #print(f"Feature batch shape: {X_batch.size()}"
    print(x)
    print(y)
    y_pred2 = model(x)
    y_pred2.cutUp()
    #print(nn.CrossEntropyLoss()(y_pred2[0],y[0]))
        #loss = loss_fn(y_pred, y_batch)
        #optimizer.zero_grad()
        #loss.backward()
        #optimizer.step()
