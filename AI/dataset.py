import random
import os
import torch
import pickle
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from bot import onodes
import fnmatch

class PositionDataset(Dataset):
    def __init__(self, positionDir):
        self.positionDir = positionDir
        self.numPos = len(fnmatch.filter(os.listdir("./AI/trainingData/"), '*.pickle'))

    def __len__(self):
        return self.numPos

    def __getitem__(self, idx):
        # Code to load training data
        data_file = open(self.positionDir + "/pos" + str(idx) + ".pickle", "rb")
        posData = pickle.load(data_file)
        data_file.close()
  
        # TODO positions where the opponent is already dead are currently not returning a mask because the game is over
        #      fix this
        if type(posData[2]) == int:
            print(idx)
            x = torch.zeros(onodes-1, dtype=bool)
            for i in range(onodes-1):
                if i==onodes-2:
                    x[i] = True
                else:
                    x[i] = False
            return posData[0], torch.zeros(onodes-1), x, posData[3]

        # Code to get the test run MCTS output, this should be done during the test runs for the future
        indexes = posData[2].nonzero(as_tuple = False)
        bufferedMCTS = []
        nextToInsert = 0
        for i in range(onodes - 1):
            if i in indexes:
                bufferedMCTS.append(posData[1][nextToInsert])
                nextToInsert += 1
            else:
                bufferedMCTS.append(0.)

        actualMCTSOutput = torch.tensor(bufferedMCTS) 
        actualResult = posData[3]
        gamePosition = posData[0]
        mask = posData[2]
        return gamePosition, actualMCTSOutput, mask, actualResult


#training_data = PositionDataset("./trainingData")
#train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)
#gamePos, train_MCTS, mask, train_result = next(iter(train_dataloader))
#print(gamePos)

