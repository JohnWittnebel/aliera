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
loader = DataLoader(training_data, batch_size=16, shuffle=True)
model = NeuralNetwork().to("cpu")
model.load_state_dict(torch.load("./botModels/gen1.bot"))
model.eval()

#a,b,c,d = next(iter(loader))

#gamePos, train_MCTS, mask, train_result = list(next(iter(loader)))[0]
#print(gamePos)

def AZLossFcn(predMCTS, actMCTS, predRes, actRes):
    loss1 = nn.CrossEntropyLoss(reduction='mean')(predMCTS, actMCTS)
    loss2 = nn.MSELoss()(predRes, actRes.unsqueeze(dim=1))
    return (loss1 + loss2).sum()

n_epochs = 1
for epoch in range(n_epochs):
    #for name, param in model.named_parameters():
    #    if param.requires_grad:
    #        print(name, param.data)
    gamePos, train_MCTS, mask, train_result = next(iter(loader))
    gamePos.requires_grad = True
    NNpred, NNvaluation = model(gamePos)
    myCoolTensor = torch.where(mask, NNpred, float('-inf'))
    predictedOutput = nn.Softmax(dim=1)(myCoolTensor)
    #loss = nn.MSELoss()(NNvaluation, train_result.to(dtype = torch.float32).unsqueeze(dim=1))
    #loss = nn.CrossEntropyLoss()(NNpred, train_MCTS)
    loss = AZLossFcn(predictedOutput, train_MCTS, NNvaluation, train_result.float())
    loss.backward()
    optimizer = torch.optim.SGD(model.parameters(), lr=2.0, momentum=0.9)
    optimizer.step()

    for name, param in model.named_parameters():
        if param.requires_grad:
            print(name, param.data)
    #print(model.weight.grad)
    #print(y_pred2)
    

    #print(nn.CrossEntropyLoss()(y_pred2[0],y[0]))
        #loss = loss_fn(y_pred, y_batch)
        #optimizer.zero_grad()
        #loss.backward()
        #optimizer.step()
