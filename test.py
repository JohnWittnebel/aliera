from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game

def main():
  x = Game()
  x.player1.draw()
  x.player2.draw()
  x.printGameState()

main()
