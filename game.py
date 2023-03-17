import os
from board import Board
from player import Player
#from deckGen import generateDeckFromFile
from constants import PLAYER_1_MAX_EVOS
from constants import PLAYER_2_MAX_EVOS
from constants import MAX_BOARD_SIZE
from constants import ENEMY_FACE
from constants import MAX_EMPTY_PP
from deck2 import deck2
from deck1 import deck1
from deck import Deck

# A Game is the primary class that controls the flow of the game
# It has 2 players, a board, and keeps track of who is the current player and the current turn
# It has a winner field that will change to 1 or 2 depending on the winner of the game
# the winString returns the reason for winning (deckout, hp reached 0, etc.)

class Game:
    def __init__(self, player1, player2):
        self.activePlayer = player1
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.currTurn = 1

        # this will become 1 or 2 once the game is over
        self.winner = 0
        self.winString = ""
    
    def __init__(self):
        # If we are initializing a board state without players already generated,
        # we need to generate the players and the decks that they will be using

        # For this, we will take the cards listed in deck1.deck and deck2.deck local files
        #deck1File = "deck1.deck"
        #deck1 = generateDeckFromFile(deck1File)
        deck1.refresh()

        #deck2File = "deck2.deck"
        #deck2 = generateDeckFromFile(deck2File
        deck2.refresh()

        self.player1 = Player(deck1, PLAYER_1_MAX_EVOS, PLAYER_1_MAX_EVOS, 1)
        self.player2 = Player(deck2, PLAYER_2_MAX_EVOS, PLAYER_2_MAX_EVOS, 2)

        self.board = Board()
        self.activePlayer = self.player1
        self.currTurn = 1
        self.winner = 0
        self.winString = ""
        
    def reset(self):    
        deck1.shuffle()
        deck2.shuffle()

        self.player1 = Player(deck1, PLAYER_1_MAX_EVOS, PLAYER_1_MAX_EVOS, 1)
        self.player2 = Player(deck2, PLAYER_2_MAX_EVOS, PLAYER_2_MAX_EVOS, 2)

        self.board = Board()
        self.activePlayer = self.player1
        self.currTurn = 1
        self.winner = 0
        self.winString = ""

    def printGameState(self):
        os.system('clear')
        if (self.activePlayer == self.player1):
            print("HP: " + str(self.player2.currHP) + "/" + str(self.player2.maxHP))
            print("Cards: " + str(len(self.player2.hand)))
            print("PP: " + str(self.player2.currPP) + "/" + str(self.player2.maxPP))
            print("")
            self.board.printBoard()
            print("")
            print("HP: " + str(self.player1.currHP) + "/" + str(self.player1.maxHP))
            print("PP: " + str(self.player1.currPP) + "/" + str(self.player1.maxPP))
            print("Hand:")
            self.player1.printHand()
        else:
            print("HP: " + str(self.player1.currHP) + "/" + str(self.player1.maxHP))
            print("Cards: " + str(len(self.player1.hand)))
            print("PP: " + str(self.player1.currPP) + "/" + str(self.player1.maxPP))
            print("")
            self.board.printBoard()
            print("")
            print("HP: " + str(self.player2.currHP) + "/" + str(self.player2.maxHP))
            print("PP: " + str(self.player2.currPP) + "/" + str(self.player2.maxPP))
            print("Hand:")
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
            # TODO: this is really just here for training purposes
            self.activePlayer.currHP -= 1
            if (self.player2.currHP <= 0):
                self.endgame(self.player1)
            elif (self.player1.currHP <= 0):
                self.endgame(self.player2)
            return
        elif (allyMonster < 0):
            print("ERROR: attempt to use a non-existent monster to attack")
            self.activePlayer.currHP -= 1
            if (self.player2.currHP <= 0):
                self.endgame(self.player1)
            elif (self.player1.currHP <= 0):
                self.endgame(self.player2)
            return
        elif (enemyMonster > len(self.board.fullBoard[defendingPlayer]) - 1):
            print("ERROR: attempt to attack a non-existent target")
            self.activePlayer.currHP -= 1
            if (self.player2.currHP <= 0):
                self.endgame(self.player1)
            elif (self.player1.currHP <= 0):
                self.endgame(self.player2)
            return
        elif (enemyMonster < -1):
            print("ERROR: attempt to attack a non-existent target")
            self.activePlayer.currHP -= 1
            if (self.player2.currHP <= 0):
                self.endgame(self.player1)
            elif (self.player1.currHP <= 0):
                self.endgame(self.player2)
            return
        elif (not self.board.fullBoard[attackingPlayer][allyMonster].canAttack):
            print("ERROR: attempt to attack with a monster that cannot attack")
            self.activePlayer.currHP -= 1
            if (self.player2.currHP <= 0):
                self.endgame(self.player1)
            elif (self.player1.currHP <= 0):
                self.endgame(self.player2)
            return

        # Actual Fuction
        # We have to implement wards at some point, but for now this is fine as is

        # For when the face is targeted, simply do damage to face. At some point, this will become more complex...
        if (enemyMonster == ENEMY_FACE):
            if (attackingPlayer == 0):
                self.player2.currHP -= self.board.player1side[allyMonster].monsterCurrAttack
                # TODO: this check needs to be in a more universal place
                if (self.player2.currHP <= 0):
                    self.winString = "HP reduced to 0"
                    self.endgame(self.player1)
            else:
                self.player1.currHP -= self.board.player2side[allyMonster].monsterCurrAttack
                if (self.player1.currHP <= 0):
                    self.winString = "HP reduced to 0"
                    self.endgame(self.player2)

        # otherwise, we are attacking a monster, deal damage to each other
        else:
            monsterDamage1 = self.board.player1side[allyMonster].monsterCurrAttack
            monsterDamage2 = self.board.player2side[enemyMonster].monsterCurrAttack
            self.board.player2side[enemyMonster].takeCombatDamage(monsterDamage1)
            self.board.player1side[allyMonster].takeCombatDamage(monsterDamage2)
        
        # Give summoning sickness to the monster that just attacked
        self.board.fullBoard[attackingPlayer][allyMonster].canAttack = 0
  
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

    def endgame(self, winner):
        if winner == self.player1:
            #print("The winner is player 1")
            self.winner = 1
        else:
            #print("The winner is player 2")
            self.winner = 2
        #print("Cause of win: " + self.winString)

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
        if (len(self.board.fullBoard[currPlayer]) == MAX_BOARD_SIZE):
            print("Attempted to play a follower when the board is full")
            self.activePlayer.currHP -= 1
            if (self.player2.currHP <= 0):
                self.endgame(self.player1)
            elif (self.player1.currHP <= 0):
                self.endgame(self.player2)
            return

        # Make sure that we have the PP to play the follower
        if len(self.activePlayer.hand) == 0 or (self.activePlayer.currPP < self.activePlayer.hand[action[1][0]].monsterCost):
            print("Attempted to play a follower that costs more than our current PP")
            self.activePlayer.currHP -= 1
            if (self.player2.currHP <= 0):
                self.endgame(self.player1)
            elif (self.player1.currHP <= 0):
                self.endgame(self.player2)
            return

        # Here is where we would do battlecries/check targets, but for now this doesn't exist

        followerToPlay = self.activePlayer.hand.pop(action[1][0])
        self.board.fullBoard[currPlayer].append(followerToPlay)
        self.activePlayer.currPP -= followerToPlay.monsterCost

    # TODO
    def endTurn(self):
        # Allow all followers to attack again
        for mons in self.board.player1side:
            mons.canAttack = 1
        for mons in self.board.player2side:
            mons.canAttack = 1

        # Change the current active player
        if (self.activePlayer == self.player1):
            self.activePlayer = self.player2
        else:
            self.activePlayer = self.player1
        
        # Change the turn number
        if (self.activePlayer == self.player1):
            self.currTurn += 1

        self.startTurn()

    def startTurn(self):
        # Increase max PP of the current player
        if (self.activePlayer.maxPP < MAX_EMPTY_PP):
          self.activePlayer.maxPP += 1

        # Set active player current PP equal to their new max
        self.activePlayer.currPP = self.activePlayer.maxPP
 
        # Set if the player has the ability to evolve or not on this turn
        # TODO: make these constants
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

        # Current problem is that only the Game can signal to end itself but the player is the
        # class that draws cards. This means that the game will have to check with the player
        # after any draw instance. To fix this, we can create a draw method for the board that
        # draws for the active player and then checks for reaper, for now this is ok though.
        # TODO
        if self.activePlayer.hand == []:
            self.winString = "Decked out"
            if self.activePlayer == self.player1:
                self.endgame(self.player2)
            else:
                self.endgame(self.player1)


    # this function will have the initial drawing and mulligan phase
    def gameStart(self):
        self.winner = 0
        self.player1.draw(3)
        self.player2.draw(3)
       
        if (len(self.player1.deck.cards) == 0):
            raise Exception("no cards in deck at start")
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
