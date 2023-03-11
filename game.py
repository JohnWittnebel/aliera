from board import Board
from player import Player
#from deckGen import generateDeckFromFile
from constants import PLAYER_1_MAX_EVOS
from constants import PLAYER_2_MAX_EVOS
from constants import ENEMY_FACE

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

  #def requestAction(self):
  #TODO

  # TODO: this might become very bloated in the future when we start implementing clash, on-attack effects, LW, etc.
  #       try to make this function as decoupled and fragmentable as possible
  def initiateAttack(self, allyMonster, enemyMonster):
    
    # First, figure out what side is attacking
    attackingPlayer = 0
    defendingPlayer = 1
    if self.activePlayer == self.player1:
        attackingPlayer = 0
        defendingPlayer = 1
    else:
        attackingPlayer = 1
        defendingPlayer = 0

    # VALID TARGETS CHECKING
    # Make sure that the allyMonster attacking a valid target, and that the enemyMonster is a valid target
    if (allyMonster > len(self.board.fullBoard[attackingPlayer]) - 1):
        print("ERROR: attempt to use a non-existent monster to attack")
        return
    elif (allyMonster < 0):
        print("ERROR: attempt to use a non-existent monster to attack")
        return
    elif (enemyMonster > len(self.board.fullBoard[defendingPlayer]) - 1):
        print("ERROR: attempt to attack a non-existent target")
        return
    elif (enemyMonster < -1):
        print("ERROR: attempt to attack a non-existent target")
        return

    # Actual Fuction
    # We have to implement wards at some point, but for now this is fine as is

    # For when the face is targeted, simply do damage to face. At some point, this will become more complex...
    if (enemyMonster == ENEMY_FACE):
        if (attackingPlayer == 0):
            self.player2.currHP -= self.board.player1side[allyMonster].monsterAttack
        else:
            self.player1.currHP -= self.board.player2side[allyMonster].monsterAttack

    # otherwise, we are attacking a monster, deal damage to each other
    else:
        monsterDamage1 = self.board.player1side[allyMonster].monsterAttack
        monsterDamage2 = self.board.player2side[allyMonster].monsterAttack
        self.board.player2side[enemyMonster].takeCombatDamage(monsterDamage1)
        self.board.player1side[allyMonster].takeCombatDamage(monsterDamage2)
  
    # TODO: this checks if any monsters are dead from the combat, could maybe be done in a better location
    for mons in self.board.player1side:
      if mons.initiateDestroy:
        print("yay")
    for mons in self.board.player2side:
      if mons.initiateDestroy:
        print("double yay")

  # TODO
  def initiateEvolve(self, evolveTarget, evolveEffTargets):
    return

  # TODO
  def playCard(self, action):
    return

  # TODO
  def endTurn(self):
    return

  # Remove magic numbers from this, maybe implement action as a class. Find some better
  # implementation in any case
  def initiateAction(self, action):
    if action[0] == 4:
      self.endTurn()
    elif action[0] == 1:
      self.playCard(action)
    elif action[0] == 2:
      self.initiateAttack(action[1], action[2][0])
    elif action[0] == 3:
      self.initiateEvolve(action[1], action[2])
    else:
      print("ERROR: Invalid action")
