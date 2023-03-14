from board import Board
from player import Player
#from deckGen import generateDeckFromFile
from constants import PLAYER_1_MAX_EVOS
from constants import PLAYER_2_MAX_EVOS
from constants import MAX_BOARD_SIZE
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
        deck1 = Deck([Goblin(), Goblin(), Goblin(), Fighter(), Fighter(), Fighter(), Goblin(), Goblin(), Goblin()])
        deck1.shuffle()

        #deck2File = "deck2.deck"
        #deck2 = generateDeckFromFile(deck2File
        deck2 = Deck([Fighter(), Fighter(), Fighter(), Goblin(), Goblin(), Goblin(), Fighter(), Fighter(), Fighter()])
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
            self.player1.printHand()
        else:
            print(self.player1.currHP + "/" + self.player1.maxHP)
            # self.board.printReverseBoard()
            print(str(self.player2.currHP) + "/" + str(self.player2.maxHP))
            self.player2.printHand()

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
                self.player2.currHP -= self.board.player1side[allyMonster].monsterCurrAttack
            else:
                self.player1.currHP -= self.board.player2side[allyMonster].monsterCurrAttack

        # otherwise, we are attacking a monster, deal damage to each other
        else:
            monsterDamage1 = self.board.player1side[allyMonster].monsterCurrAttack
            monsterDamage2 = self.board.player2side[enemyMonster].monsterCurrAttack
            self.board.player2side[enemyMonster].takeCombatDamage(monsterDamage1)
            self.board.player1side[allyMonster].takeCombatDamage(monsterDamage2)
  
        # This checks if any monsters are dead from the combat, could maybe be done in a better location
        newside1 = []
        newside2 = []
        for mons in self.board.player1side:
            if not mons.initiateDestroy:
                newside1.append(mons)
        for mons in self.board.player2side:
            if not mons.initiateDestroy:
                newside2.append(mons)

        # Now we update the board
        self.board.player1side = newside1
        self.board.player2side = newside2
        self.board.updateFullBoard()

    # TODO
    def initiateEvolve(self, evolveTarget, evolveEffTargets):
        return

    # Note that function might also become bloated with time, be careful!
    # For now, nothing has a battlecry, so just place it on the field
    # Once spells are implemented, have this split into 2 separate functions
    def playCard(self, action):
        # First, figure out what side is playing cards
        currPlayer = 0
        if self.activePlayer == self.player2:
            currPlayer = 1

        # Check that board is not full
        if (self.board.fullBoard[currPlayer].count == MAX_BOARD_SIZE):
            print("Attempted to play a follower when the board is full")

        # Here is where we would do battlecries/check targets, but for now this doesn't exist

        followerToPlay = self.activePlayer.hand.pop(action[1][0])
        self.board.fullBoard[currPlayer].append(followerToPlay)

    # TODO
    def endTurn(self):
        # Change the current active player
        if (self.activePlayer == player1):
            self.activePlayer = player2
        else:
            self.activePlayer = player1
        
        # Change the turn number
        if (self.activePlayer == player1):
            self.currTurn += 1

        self.startTurn()

    def startTurn(self):
        # Increase max PP of the current player
        self.activePlayer.maxPP += 1

        # Set active player current PP equal to their new max
        self.activePlayer.currPP = self.activePlayer.maxPP
 
        # Set if the player has the ability to evolve or not on this turn
        if (self.activePlayer == self.player1 and self.currTurn >= 5 and self.activePlayer.currEvos > 0):
            self.activePlayer.canEvolve = 1
        elif (self.activePlayer == self.player2 and self.currTurn >= 4 and self.activePlayer.currEvos > 0):
            self.activePlayer.canEvolve = 1
        else:
            self.activePlayer.canEvolve = 0

        # The second player gets to draw 2 cards on their first draw
        if (self.activePlayer == self.player2 and self.currTurn == 1):
            self.activePlayer.draw(2)
        else:
            self.activePlayer.draw()

    # this function will have the initial drawing and mulligan phase
    def gameStart(self):
        self.player1.draw(3)
        self.player2.draw(3)

        #TODO
        #mulligan

        self.startTurn()

    # Remove magic numbers from this, maybe implement action as a class. Find some better
    # implementation in any case
    def initiateAction(self, action):
        if action[0] == 4:
            self.endTurn()
        elif action[0] == 1:
            self.playCard(action)
        elif action[0] == 2:
            self.initiateAttack(action[1][0], action[1][1])
        elif action[0] == 3:
            self.initiateEvolve(action[1], action[2])
        else:
            print("ERROR: Invalid action")
