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

from transformer2 import Transformer
from bot import Bot
from bot import NeuralNetwork
from tourData import TourData
from evolve import evolve
from allmoves import ALLMOVES
from mcts import MCTS
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
    #inputArr = y.gameDataToNN(x)
    
    print("Input action:")
    print("1 = play card")
    print("2 = attack")
    print("3 = evolve")
    print("4 = end turn")

    if (botTurn == 1):
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
        #    botTurn = 1
            continue
        if (uinput1 == "5"):
            myTree = AZMCTS(x)
            #myTree.initialScan()
            myTree.runSimulations(400)
            myTree.printTree()
            input("")

  currPosSave = myTree.recordResults(x.winner, currPosSave)
  #retVal = x.winner
  return currPosSave


#with open ("AI/bots/P2BOT6.bot", 'rb') as fp:
#    test3 = pickle.load(fp)
#    test4 = pickle.load(fp)
#    z2 = Bot(test3, test4)
#singleGame(0,0,z2)

# Lets do 3 generations for now, might take some time
"""
for genRound in range(30):
    tourdata = TourData(30)
    tourdata.reset()

    for i in range(30):
        for j in range(30):
            with open ("AI/bots/P1BOT" + str(i) + ".bot", 'rb') as fp:
                test1 = pickle.load(fp)
                test2 = pickle.load(fp)
                z = Bot(test1, test2)
            with open ("AI/bots/P2BOT" + str(j) + ".bot", 'rb') as fp:
                test3 = pickle.load(fp)
                test4 = pickle.load(fp)
                z2 = Bot(test3, test4)
            goodnessAchieved = singleGame(1, z, z2)
            tourdata.p1Wins[i] += goodnessAchieved[0]
            tourdata.p2Wins[j] += goodnessAchieved[1]

            #if (winningPlayer == 2):
            #    tourdata.p2Wins[j] += 1
            #else:
            #    tourdata.p1Wins[i] += 1

    f = open("stats.txt", "a")
    f.write(str(tourdata.p1Wins))
    f.write("\n")
    f.write(str(tourdata.p2Wins))
    f.write("\n")
    f.close()

    evolve(10, 30, 1, tourdata.p1Wins)
    evolve(10, 30, 2, tourdata.p2Wins)

"""
#with open ("AI/bots/P1BOT0.bot", 'rb') as fp:
#    test1 = pickle.load(fp)
#    test2 = pickle.load(fp)
#    z = Bot(test1, test2)
#with open ("AI/bots/P2BOT0.bot", 'rb') as fp:
#    test3 = pickle.load(fp)
#    test4 = pickle.load(fp)
#    z2 = Bot(test3, test4

currPosSave = 45
for _ in range(199):
    currPosSave = singleGame(1,currPosSave)

