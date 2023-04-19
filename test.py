from monster import Monster
from deck import Deck
from game import Game
import numpy as np
import pickle
import copy
import torch
import cProfile

import sys
sys.path.insert(0, './AI/')
sys.path.insert(0, './cardArchive')
from transformer import Transformer
from bot import NeuralNetwork
from allmoves import ALLMOVES
from AZMCTS import AZMCTS
from AZMCTS import setCurrNN
from trainer import training

def singleGame(botGame, currPosSave):
  x = Game()
  y = Transformer()
  x.gameStart()

  # mulligan phase
  if botGame == 0:
      index = 0
      for item in x.player1.hand:
          print(str(index) + ": " + str(item))
          index += 1
      mull1 = int(input("mulligan card 0? "))
      mull2 = int(input("mulligan card 1? "))
      mull3 = int(input("mulligan card 2? "))
      x.player1.mulligan(mull1,mull2,mull3)
      
      index = 0
      for item in x.player2.hand:
          print(str(index) + ": " + str(item))
          index += 1
      mull1 = int(input("mulligan card 0? "))
      mull2 = int(input("mulligan card 1? "))
      mull3 = int(input("mulligan card 2? "))
      x.player2.mulligan(mull1,mull2,mull3)
  else:
      totals = [[[0,0],[0,0]],[[0,0],[0,0]]]
      currMax = 0
      currMaxIndices = [0,0,0]
      for _ in range(10):
          for i in range(2):
              for j in range(2):
                  for k in range(2):
                      mull = x.player1.mulliganSample(i,j,k)
                      myTree = AZMCTS(x)
                      val = myTree.rootInit()
                      totals[i][j][k] += val
                      if totals[i][j][k] > currMax:
                          currMax = totals[i][j][k]
                          currMaxIndices = [i,j,k]
                      x.player1.returnMulliganSample(mull)

      x.player1.mulligan(currMaxIndices[0], currMaxIndices[1], currMaxIndices[2])
      x.activePlayer = x.player2
      totals = [[[0,0],[0,0]],[[0,0],[0,0]]]
      currMax = 0
      currMaxIndices = [0,0,0]
      for _ in range(10):
          for i in range(2):
              for j in range(2):
                  for k in range(2):
                      mull = x.player2.mulliganSample(i,j,k)
                      myTree = AZMCTS(x)
                      val = myTree.rootInit()
                      totals[i][j][k] += val
                      if totals[i][j][k] > currMax:
                          currMax = totals[i][j][k]
                          currMaxIndices = [i,j,k]
                      x.player2.returnMulliganSample(mull)
      x.player2.mulligan(currMaxIndices[0], currMaxIndices[1], currMaxIndices[2])
      x.activePlayer = x.player1

  # Turn 1 start
  x.startTurn()

  if (botGame == 1):
    botTurn = 1
  else:
    botTurn = 0

  myTree = AZMCTS(x)
  myTree.rootInit()
  while (x.winner == 0):
    if (x.queue != []):
        x.clearQueue()

    x.queue = []
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
            uinput2 = input("")
            uinput3 = input("target?\n")
            if (len(uinput2) > 0):
                uinput2 = int(uinput2)
                if (len(uinput3) > 0):
                    uinput3 = int(uinput3)
                    x.initiateAction([int(uinput1),[uinput2, uinput3]])
                else:
                    x.initiateAction([int(uinput1),[uinput2]])
        if (uinput1 == "2"):
            print("Select attacker:")
            uinput2 = input("")
            print("Select defender:")
            uinput3 = input("")
            if (len(uinput2) > 0) and (len(uinput3) > 0):
                x.initiateAttack(int(uinput2), int(uinput3))
        if (uinput1 == "3"):
            print("Select target")
            uinput2 = input("")
            uinput3 = input("target:\n")
            if (len(uinput2) > 0):
                if (len(uinput3) > 0):
                    x.initiateAction([int(uinput1), [int(uinput2), int(uinput3)]])
                else:
                    x.initiateAction([int(uinput1), [int(uinput2)]])
        if (uinput1 == "4"):
            x.endTurn()
            #botTurn = 1
            continue
        if (uinput1 == "5"):
            myTree = AZMCTS(x, generation)
            myTree.rootInit()
            myTree.runSimulations(50)
            myTree.printTree()
            input("")
        if (uinput1 == "6"):
            myTree.rootInit()
        if (uinput1 == "8"):
            print("Rig RNG for card")
            uinput2 = input("select card: ")
            uinput3 = input("rigged RNG: ")
            if (len(uinput2) > 0) and (len(uinput3) > 0):
                x.activePlayer.hand[int(uinput2)].rigRNG = True
                x.activePlayer.hand[int(uinput2)].riggedVal = int(uinput3)
        if (uinput1 == "9"):
            input2 = input("cheat how many cards? ")
            if (len(input2) > 0):
                for i in range(int(input2)):
                    print("Card at position " + str(i) + ":")
                    deckIndex = 0
                    for card in x.activePlayer.deck.cards:
                        print(str(deckIndex) + ": " + str(card))
                        deckIndex += 1
                    cheatedCard = input("")
                    if (len(cheatedCard) > 0):
                        swap = x.activePlayer.hand[i]
                        x.activePlayer.hand[i] = x.activePlayer.deck.cards[int(cheatedCard)]
                        x.activePlayer.deck.cards[int(cheatedCard)] = swap
        if (uinput1 == "sb"):
            input2 = input("spellboost what card index?")
            input3 = input("spellboost how many times?")


  currPosSave = myTree.recordResults(x.winner, currPosSave)
  return currPosSave, x.winner
  #return x.winner


def botGenerationTest(bot1, bot2):  
    x = Game()
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

#currPosSave=0
#winner = singleGame(0,currPosSave)
#print(winner)

learningRate = 2
generation = 1
currPosSave = 0
for pepega in range(1):
    # FOR GENERATING TRAINING DATA
    currNN = NeuralNetwork()
    setCurrNN(generation)
    thisRound = 0
    startingPoint = currPosSave
    while thisRound < 10000:
        currPosSave, recentWinner = singleGame(1,currPosSave)
        print(recentWinner)
        thisRound = currPosSave - startingPoint
    learningRate = 1 / pow(2,pepega)
    training(generation, learningRate)
    generation += 1

    # FOR testing bot vs new gen
    model1 = NeuralNetwork().to("cpu")
    model1.load_state_dict(torch.load("./AI/botModels/gen" + str(generation-1) + ".bot"))
    model1.eval()

    model2 = NeuralNetwork().to("cpu")
    model2.load_state_dict(torch.load("./AI/botModels/gen" + str(generation) + ".bot"))
    model2.eval()

    result = [0,0]
    player1wins = 0
    for _ in range(120):
        winner = botGenerationTest(model1, model2)
        if winner == 1:
            result[0] += 1
            player1wins += 1
        else:
            result[1] += 1

    for _ in range(120):
        winner = botGenerationTest(model2, model1)
        if winner == 1:
            result[1] += 1
            player1wins += 1
        else:
            result[0] += 1

    print(result)
    f = open("resultFile.txt", "a")
    f.write(str(result[0]) + " v " + str(result[1]) + "\n")
    f.close()
    
    if result[1] < 123:
        generation -= 1


