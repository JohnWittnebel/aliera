from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck

def main():
  y = Goblin()
  x = Fighter()
  myDeck = Deck([x,y])
  myDeck.shuffle()
  print(myDeck)
  
main()
