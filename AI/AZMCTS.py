# This class will determine what action to take, and keep track of winrates/games

# Each node has a gamestate, number of games ran, and winrate from that node

from allmoves import ALLMOVES
import random
import copy
import math

class AZMCTS():
    def __init__(self, gameState):
        self.gameState = gameState
        self.moveArr = []
        self.totalSims = 0
        self.exploreParam = 0.14
        moves = gameState.generateLegalMoves()

        self.children = []

        childIndex = 0
        # each element of moveArr is [move, childIndex, timesTaken, totalValue, meanValue, moveProb (according to NN)]
        for ele in moves:
            self.moveArr.append([ele, childIndex, 0, 0., 0., 0.])
            self.children.append(0)
            childIndex += 1
    
    def runSimulations(self, simulations):
        for _ in range(simulations):
            self.descendTree()
            self.totalSims += 1

    def descendTree(self):
        actionIndex = self.selectAction()
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
        if (len(self.moveArr) == 1) or (self.totalSims == 0):
            return 0
        currMaxIndex = 0
        currMax = -1
        currActionIndex = 0
        for ele in self.moveArr:
            #print(ele)
            currVal = ele[4] + self.exploreParam * math.sqrt(math.log(self.totalSims)/max(0.00001,float(ele[2])))
            if currMax < currVal:
                currMax = currVal
                currMaxIndex = currActionIndex
            currActionIndex += 1
            #input("")
        return currMaxIndex

    def takeAction(self, actionIndex, childIndex):
        # We are at a leaf node, time to create a new leaf then climb
        if (self.children[childIndex] == 0):
            #TODO: bug here, we are continuing to expand when the game is over
            z = copy.deepcopy(self.gameState)
            z.initiateAction(self.moveArr[actionIndex][0])
            self.children[childIndex] = AZMCTS(z)
            self.children[childIndex].gameState.printGameState()
  
            # game has ended
            if self.children[childIndex].gameState.winner != 0:
                if self.children[childIndex].gameState.winner == self.children[childIndex].gameState.activePlayer.playerNum:
                    return 1
                else:
                    return 0
            # game is still in progress, return NN eval
            # TODO
            return 0.2

        return self.children[actionIndex].descendTree()
      
    def printTree(self):
        for ele in self.moveArr:
            print(ele)
