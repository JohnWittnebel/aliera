from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game
import numpy as np
import pickle

import sys
sys.path.insert(0, './AI/')

from transformer import Transformer
from bot import Bot
from tourData import TourData

def singleGame(botGame, bot1, bot2):
  x = Game()
  x.gameStart()
  y = Transformer()

  # This is the hidden layer weights
  #test1 = np.random.uniform(-1,1,(10,37))
  #test2 = np.random.uniform(-1,1,(6,10))
  #z = Bot(test1, test2)

  if (botGame == 1):
    botTurn = 1
  else:
    botTurn = 0
  
  #print(x.winner)
  #lmao = raw_input("")
  #x.reset()
  while (x.winner == 0): 
    x.printGameState()
    if (x.activePlayer == x.player1):
        inputArr = y.gameDataToNN(x.board.player1side, x.board.player2side, x.player1.hand, x.player1.currHP, x.player2.currHP, len(x.player2.hand), x.player1.currPP, x.player1.maxPP)
    else:
        inputArr = y.gameDataToNN(x.board.player2side, x.board.player1side, x.player2.hand, x.player2.currHP, x.player1.currHP, len(x.player1.hand), x.player2.currPP, x.player2.maxPP)
    
    if (botGame == 1) or (botTurn == 1):
        if (x.activePlayer == x.player1):
            botToMove = bot1
        else:
            botToMove = bot2
        botoutput = botToMove.getMove(inputArr)
        if (x.activePlayer == x.player1):
            botAction = y.NNtoGame(botoutput, x.player1.hand)
        else:
            botAction = y.NNtoGame(botoutput, x.player2.hand)

    print("Input action:")
    print("1 = play card")
    print("2 = attack")
    print("4 = end turn")


    if (botTurn == 1):
        #nothing = raw_input("")
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
        uinput1 = raw_input("")
        if (uinput1 == "1"):
            print("input card:")
            uinput2 = int(raw_input(""))
            x.initiateAction([int(uinput1),[uinput2]])
        if (uinput1 == "2"):
            print("Select attacker:")
            uinput2 = int(raw_input(""))
            print("Select defender:")
            uinput3 = int(raw_input(""))
            x.initiateAttack(uinput2, uinput3)
        if (uinput1 == "4"):
            x.endTurn()
            botTurn = 1
            continue

  retVal = x.winner
  del x
  return retVal

#    x.initiateAction([uinput1,[uinput2,uinput3]])

  #x.initiateAttack(0,-1)
  #x.initiateAttack(0,0)

  #x.board.player1side.append(Goblin())
  #x.board.player2side.append(Goblin())
  #x.printGameState()
  #x.initiateAttack(0,1)
  #x.printGameState()
#main()
#This is the hidden layer weights

#for i in range(2):
#    singleGame(0,0,0)

#with open ("AI/bots/P2BOT6.bot", 'rb') as fp:
#    test3 = pickle.load(fp)
#    test4 = pickle.load(fp)
#    z2 = Bot(test3, test4)
#singleGame(0,0,z2)

tourdata = TourData(10)

for i in range(10):
    for j in range(10):
        with open ("AI/bots/P1BOT" + str(i) + ".bot", 'rb') as fp:
            test1 = pickle.load(fp)
            test2 = pickle.load(fp)
            z = Bot(test1, test2)
        with open ("AI/bots/P2BOT" + str(j) + ".bot", 'rb') as fp:
            test3 = pickle.load(fp)
            test4 = pickle.load(fp)
            z2 = Bot(test3, test4)
        winningPlayer = singleGame(1, z, z2)
        if (winningPlayer == 2):
            tourdata.p2Wins[j] += 1
        else:
            tourdata.p1Wins[i] += 1
print(tourdata.p1Wins)
print(tourdata.p2Wins)
