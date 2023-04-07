# This class will determine what action to take, and keep track of winrates/games

# Each node has a gamestate, number of games ran, and winrate from that node

from allmoves import ALLMOVES
import random
import copy
import math

class MCTS():
    def __init__(self, gameState):
        self.gameState = gameState
        self.moveArr = []
        self.totalSims = 0
        self.exploreParam = 0.14
        moves = gameState.generateLegalMoves()

        # each element of moveArr is [move, wins, gamesSimulated]
        for ele in moves:
            self.moveArr.append([ele, 0, 0])
        

    def initialScan(self):
        for ele in self.moveArr:
            for _ in range(15):
                gameWin = self.simulateRandomGameAfterAction(ele[0])
                if (gameWin == self.gameState.activePlayer.playerNum):
                    ele[1] += 1
                ele[2] += 1
                self.totalSims += 1

    def runSimulations(self, simulations):
        for _ in range(simulations):
            childToFollow = self.selectAction()
            gameWin = self.simulateRandomGameAfterAction(self.moveArr[childToFollow][0])
            if (gameWin == self.gameState.activePlayer.playerNum):
                self.moveArr[childToFollow][1] += 1
            self.moveArr[childToFollow][2] += 1

    def selectAction(self):
        currMaxIndex = 0
        currMax = -1
        currActionIndex = 0
        for ele in self.moveArr:
            currVal = (float(ele[1])/float(ele[2])) + self.exploreParam * math.sqrt(math.log(self.totalSims)/float(ele[2]))
            if currMax < currVal:
                currMax = currVal
                currMaxIndex = currActionIndex
            currActionIndex += 1
        return currMaxIndex

    def simulateRandomGameAfterAction(self, action):
        z = copy.deepcopy(self.gameState)
        z.initiateAction(action)
        gameWin = z.runToCompletion()
        return gameWin
        
    def printTree(self):
        for ele in self.moveArr:
            print(ele)
