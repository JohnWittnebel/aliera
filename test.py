from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game

def main():
  x = Game()
  x.player1.draw(3)
  x.player2.draw(3)

  #x.board.player1side.append(Fighter())
  #x.board.player2side.append(Fighter())
  #x.board.player2side.append(Fighter())
  
  x.printGameState()
  print("Input action:")
  uinput1 = int(raw_input(""))
  print("input first target:")
  uinput2 = int(raw_input(""))
  print("Select second target:")
  uinput3 = int(raw_input(""))
  x.initiateAction([uinput1,[uinput2,uinput3]])


  #x.initiateAttack(0,0)
  #x.board.player1side.append(Goblin())
  #x.board.player2side.append(Goblin())
  x.printGameState()
  #x.initiateAttack(0,1)
  #x.printGameState()
main()
