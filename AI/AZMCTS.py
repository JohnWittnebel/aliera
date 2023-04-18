# This class will determine what action to take, and keep track of winrates/games

# Each node has a gamestate, number of games ran, and winrate from that node

from allmoves import ALLMOVES
import random
import copy
import math
import pickle
import torch
from transformer import Transformer
from bot import NeuralNetwork
from mycopy import trueCopy

import sys
sys.path.insert(0, './botModels/')
sys.path.insert(0, './..')

#TODO: the training file should handle this
currNN = NeuralNetwork()
#currNN.load_state_dict(torch.load("./AI/botModels/test.bot"))
#currNN.eval()
GAMENUM = 1
POSNUM = 1
#gamePath = []
transformer = Transformer()


class AZMCTS():
    def __init__(self, gameState, parent=None):
        self.gameState = gameState
        self.moveArr = []
        self.totalSims = 0
        self.exploreParam = 1.4
        self.parent = parent
        self.mask = 0
        moves = gameState.generateLegalMoves()

        self.children = []

        rollIndex = 0
        # each element of moveArr is [move, childIndex, timesTaken, totalValue, meanValue, moveProb (according to NN),
        #                             move indices (for training)]
        for ele in moves:
            self.moveArr.append([ele, rollIndex, 0, 0., 0., 0.])
            self.children.append(0)
            rollIndex += 1
    
    # the moveProbs are generated when the node is created during tree descent, but this doesnt occur for the root
    # so we do it manually here
    def rootInit(self):
        nnInput = transformer.gameDataToNN(self.gameState)
        nnInput = nnInput.unsqueeze(dim=0)
            
        logits = currNN(nnInput)[0]
        val = currNN(nnInput)[1]
        #print(logits)
        probabilitiesNN, mask = transformer.normalizedVector(logits[0], self.gameState)
        #print(mask)
        #print(probabilitiesNN)
        self.mask = mask
        self.setProbabilities(probabilitiesNN)
        return val

    def runSimulations(self, simulations):
        for _ in range(simulations):
            self.descendTree()
        #    self.totalSims += 1

    def descendTree(self):
        self.totalSims += 1
        actionIndex = self.selectAction()
        #input(self.printTree())
        updateValue = self.takeAction(actionIndex, self.moveArr[actionIndex][1])
        # if the previous action was a pass, then we invert the valuation
        if self.moveArr[actionIndex][0][0] == 4:
            updateValue = 1 - updateValue

        # update the action info
        self.moveArr[actionIndex][2] += 1
        self.moveArr[actionIndex][3] += updateValue
        self.moveArr[actionIndex][4] = self.moveArr[actionIndex][3] / self.moveArr[actionIndex][2]
        return updateValue

    def selectAction(self):
        if (len(self.moveArr) == 1): #or (self.totalSims == 0):
            return 0
        currMaxIndex = 0
        currMax = -1
        currActionIndex = 0
        for ele in self.moveArr:
            currVal = ele[4] + (self.exploreParam * ele[5] * (math.sqrt(1 + float(self.totalSims)) / (1 + float(ele[2]))))
            if currMax < currVal:
                currMax = currVal
                currMaxIndex = currActionIndex
            currActionIndex += 1
            #input("")
        return currMaxIndex

    def takeAction(self, actionIndex, childIndex):
        # We are at a leaf node, time to create a new leaf then climb, unless we are already at a game end state
        if self.gameState.winner != 0:
            if self.gameState.winner == self.gameState.activePlayer.playerNum:
                return 1
            else:
                return 0

        if (self.children[childIndex] == 0):
            z = copy.deepcopy(self.gameState)
            z.initiateAction(self.moveArr[actionIndex][0])
            self.children[childIndex] = AZMCTS(z, self)
            #self.children[childIndex].gameState.printGameState()
  
            # game has ended
            if self.children[childIndex].gameState.winner != 0:
                if self.children[childIndex].gameState.winner == self.children[childIndex].gameState.activePlayer.playerNum:
                    return 1
                else:
                    return 0
            # game is still in progress, return NN eval
            nnInput = transformer.gameDataToNN(self.gameState)
            nnInput = nnInput.unsqueeze(dim=0)
            
            logits = currNN(nnInput)
            logitsProb = logits[0][0]
            logitsValuation = logits[1][0]

            probabilitiesNN, mask = transformer.normalizedVector(logitsProb, self.children[childIndex].gameState)
            self.children[childIndex].mask = mask
            self.children[childIndex].setProbabilities(probabilitiesNN)
            return logitsValuation

        return self.children[actionIndex].descendTree()
      
    def printTree(self):
        for ele in self.moveArr:
            currVal = ele[4] + (self.exploreParam * ele[5] * (math.sqrt(1 + float(self.totalSims)) / (1 + float(ele[2]))))
            print(ele)
            print(currVal)
            print(self.totalSims)

    def setProbabilities(self, probabilities):
        currIndex = 0
        for ele in self.moveArr:
            ele[5] = probabilities[currIndex]
            currIndex += 1
        #moveInd = 0
        #allMoveInd = 0
        #while (moveInd < len(self.moveArr)):
        #    if ALLMOVES[allMoveInd] == self.moveArr[moveInd][0]:
        #        self.moveArr[moveInd][5] = probabilities[allMoveInd]
        #        moveInd += 1
        #    allMoveInd += 1

        if (self.moveArr[len(self.moveArr) - 1] == 0):
            print("ERROR")
            self.printTree()
            input(probabilities)

    def recordResults(self, result, posnum):
        MCTSRes = []
        for ele in self.moveArr:
            MCTSRes.append(float(ele[2]) / float(self.totalSims))

        if (result == self.gameState.activePlayer.playerNum):
            gameResult = 1
        else:
            gameResult = 0
        condensedResult = [transformer.gameDataToNN(self.gameState), MCTSRes, self.mask, gameResult]
        with open("./AI/trainingData/pos" + str(posnum) + ".pickle", "wb") as f:
            pickle.dump(condensedResult, f)

        if (self.parent != None):
            return self.parent.recordResults(result, posnum+1)
        else:
            return posnum+1

    def cleanTreeExceptAction(self, action):
        for move in self.moveArr:
            if move[0] != action:
                if (self.children[move[1]] != 0):
                    self.children[move[1]].cleanTree()
                    self.children[move[1]] = None

    def cleanTree(self):
        for child in self.children:
            if child != 0:
                child.cleanTree()
                child = None
