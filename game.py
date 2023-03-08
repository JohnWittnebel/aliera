from board import Board
from player import Player
#from deckGen import generateDeckFromFile
from constants import PLAYER_1_MAX_EVOS
from constants import PLAYER_2_MAX_EVOS

from deck import Deck
from cardArchive import Goblin
from cardArchive import Fighter

# A Game is the primary class that controls the flow of the game
# It has 2 players, a board, and keeps track of who is the current player and the current turn

class Game:
  def __init__(self, player1, player2):
    self.activePlayer = player1
    self.player1 = player1
    self.player2 = player2
    self.board = Board()
    self.currTurn = 1
    
  def __init__(self):
    # If we are initializing a board state without players already generated,
    # we need to generate the players and the decks that they will be using

    # For this, we will take the cards listed in deck1.deck and deck2.deck local files
    #deck1File = "deck1.deck"
    #deck1 = generateDeckFromFile(deck1File)
    deck1 = Deck([Goblin(), Goblin(), Goblin(), Fighter(), Fighter(), Fighter()])
    deck1.shuffle()

    #deck2File = "deck2.deck"
    #deck2 = generateDeckFromFile(deck2File
    deck2 = Deck([Fighter(), Fighter(), Fighter(), Goblin(), Goblin(), Goblin()])
    deck2.shuffle()

    self.player1 = Player(deck1, PLAYER_1_MAX_EVOS, PLAYER_1_MAX_EVOS, 1)
    self.player2 = Player(deck2, PLAYER_2_MAX_EVOS, PLAYER_2_MAX_EVOS, 2)

    self.board = Board()
    self.activePlayer = self.player1
    self.currTurn = 1

  def printGameState(self):
    if (self.activePlayer == self.player1):
      print(str(self.player2.currHP) + "/" + str(self.player2.maxHP))
      self.board.printBoard()
      print(str(self.player1.currHP) + "/" + str(self.player1.maxHP))
      print(self.player1.hand)
    else:
      print(self.player1.currHP + "/" + self.player1.maxHP)
     # self.board.printReverseBoard()
      print(str(self.player2.currHP) + "/" + str(self.player2.maxHP))
      print(self.player2.hand)

 # def requestAction(self):
    #TODO

  # The way that we will parse a requested action
 # def parseAction(self):
    #TODO

 # def executeAction(self):
    #TODO
