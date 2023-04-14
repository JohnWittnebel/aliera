from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game
import numpy as np
import pickle
import copy
import torch
import cProfile

import sys
sys.path.insert(0, './AI/')

from transformer import Transformer
from bot import Bot
from bot import NeuralNetwork
from allmoves import ALLMOVES
from AZMCTS import AZMCTS

def singleGame(botGame, currPosSave):
  x = Game(1)
  x.gameStart()
  y = Transformer()

  if (botGame == 1):
    botTurn = 1
  else:
    botTurn = 0
  
  myTree = AZMCTS(x)
  myTree.rootInit()
  while (x.winner == 0):

    x.printGameState()
    
    print("Input action:")
    print("1 = play card")
    print("2 = attack")
    print("3 = evolve")
    print("4 = end turn")

    if (botGame == 1):
        myTree.runSimulations(50)
        myTree.printTree()
        
        maxSims = -1
        bestMove = [4]
        for ele in myTree.moveArr:
            if ele[2] > maxSims:
                maxSims = ele[2]
                bestMove = ele[0]
                bestChild = myTree.children[ele[1]]
        if (bestMove == [4] and botGame == 0):
            botTurn = 0

        myTree.cleanTreeExceptAction(bestMove)
        myTree = bestChild
        x.initiateAction(bestMove)
    
    elif (botTurn == 1):
        model1 = NeuralNetwork().to("cpu")
        model1.load_state_dict(torch.load("./AI/botModels/gen4.bot"))
        model1.eval()
        pos = y.gameDataToNN(x)
        z = pos.unsqueeze(dim=0)
        moves = x.generateLegalMoves()
        pred = model1(z)

        moveProbs = y.normalizedVector(pred[0][0],x)[0]
        currIndex = 0
        maxIndex = 0
        maxProb = 0
        for _ in range(len(moves)):
            if maxProb < moveProbs[currIndex]:
                maxIndex = currIndex
                maxProb = moveProbs[currIndex]
            currIndex += 1
        x.initiateAction(moves[maxIndex])

        if (moves[maxIndex] == [4]):
            botTurn = 0

    else:
        #mytest = model(torch.flatten(inputArr))
        #mytest = y.normalizedVector(mytest[0], x)
        #mymax = 0
        #maxIndex = 0
        #for currIndex in range(len(mytest)):
        #    if mytest[currIndex] > mymax:
        #        maxIndex = currIndex
        #        mymax = mytest[currIndex]
        #    currIndex += 1
        #print(mytest)
        #print(ALLMOVES[maxIndex])
        print(x.generateLegalMoves())
        uinput1 = input("")

        if (uinput1 == "1"):
            print("input card:")
            uinput2 = int(input(""))
            x.initiateAction([int(uinput1),[uinput2]])
        if (uinput1 == "2"):
            print("Select attacker:")
            uinput2 = int(input(""))
            print("Select defender:")
            uinput3 = int(input(""))
            x.initiateAttack(uinput2, uinput3)
        if (uinput1 == "3"):
            print("Select target")
            uinput2 = int(input(""))
            uinput3 = int(input("target:\n"))
            x.initiateAction([int(uinput1), [uinput2, uinput3]])
        if (uinput1 == "4"):
            x.endTurn()
            botTurn = 1
            continue
        if (uinput1 == "5"):
            myTree = AZMCTS(x)
            #myTree.initialScan()
            myTree.runSimulations(50)
            myTree.printTree()
            input("")

  return
  #currPosSave = myTree.recordResults(x.winner, currPosSave)
  #return currPosSave


def botGenerationTest(bot1, bot2):  
    x = Game(1)
    x.gameStart()
    y = Transformer()

    while (x.winner == 0):

        x.printGameState()
    
        print("Input action:")
        print("1 = play card")
        print("2 = attack")
        print("3 = evolve")
        print("4 = end turn")

        pos = y.gameDataToNN(x)
        z = pos.unsqueeze(dim=0)
        moves = x.generateLegalMoves()
        if (x.activePlayer.playerNum == 1):    
            pred = bot1(z)
        else:
            pred = bot2(z) 

        moveProbs = y.normalizedVector(pred[0][0],x)[0]
        print(moveProbs)
        currIndex = 0
        maxIndex = 0
        maxProb = 0
        for _ in range(len(moves)):
            if maxProb < moveProbs[currIndex]:
                maxIndex = currIndex
                maxProb = moveProbs[currIndex]
            currIndex += 1
        x.initiateAction(moves[maxIndex])

    return x.winner


# FOR GENERATING TRAINING DATA
currPosSave = 8089
#for _ in range(100):
currPosSave = singleGame(0,currPosSave)

# FOR testing bot vs new gen
"""
model1 = NeuralNetwork().to("cpu")
model1.load_state_dict(torch.load("./AI/botModels/gen3.bot"))
model1.eval()

model2 = NeuralNetwork().to("cpu")
model2.load_state_dict(torch.load("./AI/botModels/gen4.bot"))
model2.eval()

result = [0,0]
player1wins = 0
for _ in range(100):
    winner = botGenerationTest(model1, model2)
    if winner == 1:
        result[0] += 1
        player1wins += 1
    else:
        result[1] += 1

for _ in range(100):
    winner = botGenerationTest(model2, model1)
    if winner == 1:
        result[1] += 1
        player1wins += 1
    else:
        result[0] += 1

print(result)
print(player1wins)
"""
