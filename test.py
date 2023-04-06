from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game
import numpy as np
import pickle
import copy
import torch

import sys
sys.path.insert(0, './AI/')

#from transformer import Transformer
from transformer2 import Transformer
from bot import Bot
from bot import NeuralNetwork
from tourData import TourData
from evolve import evolve
from allmoves import ALLMOVES

def singleGame(botGame, bot1, bot2):
  x = Game()
  x.gameStart()
  y = Transformer()

  model = NeuralNetwork().to("cpu")
  #X = torch.rand(5, 4, 25)
  #logits = model(torch.flatten(X))
  #print(logits)

  # This is the hidden layer weights
  #test1 = np.random.uniform(-1,1,(10,37))
  #test2 = np.random.uniform(-1,1,(6,10))
  #z = Bot(test1, test2)

  if (botGame == 1):
    botTurn = 1
  else:
    botTurn = 0
  
  #print(x.winner)
  #x.reset()
  while (x.winner == 0):

    x.printGameState()
    if (x.activePlayer == x.player1):
        inputArr = y.gameDataToNN(x.board.player1side, x.board.player2side, x.player1, x.player2)
    else:
        inputArr = y.gameDataToNN(x.board.player2side, x.board.player1side, x.player2, x.player1)
    
    if (botGame == 1) or (botTurn == 1):
        print(genRound)
        print(i)
        print(j)
        if (x.activePlayer == x.player1):
            botToMove = bot1
        else:
            botToMove = bot2
        botoutput = botToMove.getMove(inputArr)
        if (x.activePlayer == x.player1):
            botAction = y.NNtoGame(botoutput, x.player1.hand)
        else:
            botAction = y.NNtoGame(botoutput, x.player2.hand)
        print(str(botAction) + str(botoutput))

    print("Input action:")
    print("1 = play card")
    print("2 = attack")
    print("3 = evolve")
    print("4 = end turn")

    if (botTurn == 1):
        #nothing = input("")
        if (botAction[0] == 1):
            x.initiateAction([1, [botAction[1]]])
        if (botAction[0] == 2):
            x.initiateAttack(botAction[1][0], botAction[1][1])
        if (botAction[0] == 4):
            x.endTurn()
            if (botGame == 1):
                continue
            else:
                botTurn = 0
                continue
    else:
        mytest = model(torch.flatten(inputArr))
        mytest = y.normalizedVector(mytest[0], x)
        mymax = 0
        maxIndex = 0
        for currIndex in range(len(mytest)):
            if mytest[currIndex] > mymax:
                maxIndex = currIndex
                mymax = mytest[currIndex]
            currIndex += 1
        print(mytest)
        print(ALLMOVES[maxIndex])
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
            x.initiateAction([int(uinput1), [uinput2]])
        if (uinput1 == "4"):
            x.endTurn()
            #botTurn = 1
            continue
        if (uinput1 == "5"):
            wins1 = 0
            wins2 = 0
            for _ in range(100):
                z = copy.deepcopy(x)
                gameWin = z.runToCompletion()
                if (gameWin == 1):
                    wins1 += 1
                else:
                    wins2 += 1
            input("wins for p1: " + str(wins1) + ", wins for p2: " + str(wins2))

  #retVal = x.winner
  retVal = [x.player1.goodness, x.player2.goodness]
  del x
  return retVal


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
#    z2 = Bot(test3, test4)
singleGame(0,0,0)

