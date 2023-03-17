from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game
import numpy as np

import sys
sys.path.insert(0, './AI/')

from transformer import Transformer
from bot import Bot

def main():
  x = Game()
  x.gameStart()
  y = Transformer()

  # This is the hidden layer weights
  test1 = np.random.uniform(-1,1,(10,37))
  test2 = np.random.uniform(-1,1,(6,10))
  z = Bot(test1, test2)

  #x.board.player1side.append(Fighter())
  #x.board.player2side.append(Fighter())
  #x.board.player2side.append(Fighter())

  while (x.winner == 0): 
    x.printGameState()
    if (x.activePlayer == x.player1):
        inputArr = y.gameDataToNN(x.board.player1side, x.board.player2side, x.player1.hand, x.player1.currHP, x.player2.currHP, len(x.player2.hand), x.player1.currPP, x.player1.maxPP)
    else:
        inputArr = y.gameDataToNN(x.board.player2side, x.board.player1side, x.player2.hand, x.player2.currHP, x.player1.currHP, len(x.player1.hand), x.player2.currPP, x.player2.maxPP)
    print(z.think(inputArr))
    print("Input action:")
    print("1 = play card")
    print("2 = attack")
    print("4 = end turn")
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
        continue


#    x.initiateAction([uinput1,[uinput2,uinput3]])

  #x.initiateAttack(0,-1)
  #x.initiateAttack(0,0)

  #x.board.player1side.append(Goblin())
  #x.board.player2side.append(Goblin())
  #x.printGameState()
  #x.initiateAttack(0,1)
  #x.printGameState()
main()
