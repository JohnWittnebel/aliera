from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game

def main():
  x = Game()
  x.player1.draw()
  x.player2.draw()

  x.board.player1side.append(Fighter())
  x.board.player2side.append(Fighter())
  x.board.player2side.append(Fighter())
  x.printGameState()
  x.initiateAttack(0,1)
  x.printGameState()
main()
