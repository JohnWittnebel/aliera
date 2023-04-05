import os
from board import Board
from player import Player
#from deckGen import generateDeckFromFile
from constants import *
from deck2 import deck2
from deck1 import deck1
from deck import Deck
import random

from cardArchive import Goblin, Fighter

# A Game is the primary class that controls the flow of the game
# It has 2 players, a board, and keeps track of who is the current player and the current turn
# It has a winner field that will change to 1 or 2 depending on the winner of the game
# the winString returns the reason for winning (deckout, hp reached 0, etc.)

# training variables
TRAINING = 1
PLAY_CARD_GOODNESS = 2
ATTACK_GOODNESS = 30
VALUE_TRADE_GOODNESS = 0
ANTI_VALUE_TRADE_GOODNESS = 0
WIN_ATTACK_GOODNESS = 1000
PASS_GOODNESS = 0

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

        #TODO
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
            print("Active player: 1")
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
            print("Active player: 2")
            print("HP: " + str(self.player2.currHP) + "/" + str(self.player2.maxHP))
            print("Cards: " + str(len(self.player1.hand)))
            print("PP: " + str(self.player2.currPP) + "/" + str(self.player2.maxPP))
            print("")
            self.board.printBoard()
            print("")
            print("HP: " + str(self.player1.currHP) + "/" + str(self.player1.maxHP))
            print("PP: " + str(self.player1.currPP) + "/" + str(self.player1.maxPP))
            print("Hand:")
            self.player2.printHand()

    def initiateEvolve(self, allyMonsterIndex):
        if (not self.activePlayer.canEvolve) or (self.activePlayer.currEvos == 0):
            print("ERROR: this player cannot evolve")
            return

        if self.activePlayer == self.player1:
            evolveTarget = self.board.fullBoard[0][allyMonsterIndex].evolve(self)
        else:
            evolveTarget = self.board.fullBoard[1][allyMonsterIndex].evolve(self)

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
        elif (not self.board.fullBoard[attackingPlayer][allyMonster].canAttack):
            print("ERROR: attempt to attack with a monster that cannot attack")
            return
        elif (enemyMonster == -1 and not self.board.fullBoard[attackingPlayer][allyMonster].canAttackFace):
            print("ERROR: this monster cannot attack face")
            return

        # VALID TARGETS CHECKING FOR WARDS, this might need to become more general
        wardExists = 0
        for enem in self.board.fullBoard[defendingPlayer]:
            if enem.hasWard:
                wardExists = 1
        if wardExists and (enemyMonster == ENEMY_FACE or not self.board.fullBoard[defendingPlayer][enemyMonster].hasWard):
            print("ERROR: attempt to attack through a ward")
            return

        # Actual Fuction
        # We have to implement wards at some point, but for now this is fine as is

        # For when the face is targeted, simply do damage to face. At some point, this will become more complex...
        if (enemyMonster == ENEMY_FACE):
            if (attackingPlayer == 0):
                self.player2.currHP -= self.board.player1side[allyMonster].monsterCurrAttack
                if (self.player2.currHP <= 0):
                    self.winString = "HP reduced to 0"
                    self.endgame(self.player1)
            else:
                self.player1.currHP -= self.board.player2side[allyMonster].monsterCurrAttack
                if (self.player1.currHP <= 0):
                    self.winString = "HP reduced to 0"
                    self.endgame(self.player2)

        # otherwise, we are attacking a monster, deal damage to each other
        # TODO make this less bad/redundant
        else:
            if (attackingPlayer == 0):
                monsterDamage1 = self.board.player1side[allyMonster].monsterCurrAttack
                monsterDamage2 = self.board.player2side[enemyMonster].monsterCurrAttack
                self.board.player2side[enemyMonster].takeCombatDamage(monsterDamage1)
                self.board.player1side[allyMonster].takeCombatDamage(monsterDamage2)
                
            else:
                monsterDamage1 = self.board.player2side[allyMonster].monsterCurrAttack
                monsterDamage2 = self.board.player1side[enemyMonster].monsterCurrAttack
                self.board.player1side[enemyMonster].takeCombatDamage(monsterDamage1)
                self.board.player2side[allyMonster].takeCombatDamage(monsterDamage2)
        
        # Give summoning sickness to the monster that just attacked
        self.board.fullBoard[attackingPlayer][allyMonster].canAttack = 0
        self.board.fullBoard[attackingPlayer][allyMonster].hasAttacked = 1
  
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
            return

        # Make sure that we have the PP to play the follower
        if len(self.activePlayer.hand) == 0 or (self.activePlayer.currPP < self.activePlayer.hand[action[1][0]].monsterCost):
            print("Attempted to play a follower that costs more than our current PP")
            return

        # Here is where we would do battlecries/check targets, but for now this doesn't exist

        followerToPlay = self.activePlayer.hand.pop(action[1][0])
        followerToPlay.play(self, currPlayer)
        #self.board.fullBoard[currPlayer].append(followerToPlay)
        #self.activePlayer.currPP -= followerToPlay.monsterCost

    # TODO
    def endTurn(self):
        # Allow all followers to attack again
        for mons in self.board.player1side:
            mons.canAttack = 1
            mons.canAttackFace = 1
        for mons in self.board.player2side:
            mons.canAttack = 1
            mons.canAttackFace = 1

        # Change the current active player
        if (self.activePlayer == self.player1):
            self.activePlayer = self.player2
        else:
            self.activePlayer = self.player1
        
        # Change the turn number
        if (self.activePlayer == self.player1):
            self.currTurn += 1
        
        # Allow evolving if currently late in game
        if (self.activePlayer == self.player2 and self.currTurn >= 4):
            self.activePlayer.canEvolve = 1
        if (self.activePlayer == self.player1 and self.currTurn >= 5):
            self.activePlayer.canEvolve = 1

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

    # this function is mostly to deal with ward, but can be expanded to include other specific cards
    def attackableTargets(self):
        targets = []
        if self.activePlayer == self.player1:
            targetPlayer = 1
        else:
            targetPlayer = 0

        # Ward check
        wards = []
        wardIndex = 0
        for follower in self.board.fullBoard[targetPlayer]:
            if follower.hasWard:
                wards.append(wardIndex)
            wardIndex += 1
        
        if wards == []:
            targets.append(-1)
            targets += range(len(self.board.fullBoard[targetPlayer]))
        else:
            targets = wards

        return targets

    def generateLegalMoves(self):
        moves = [[PASS_ACTION]]

        if self.activePlayer == self.player1:
            allyBoard = 0
        else:
            allyBoard = 1

        currIndex = 0
        # Attacking moves available
        possibleTargets = self.attackableTargets()
        for card in self.board.fullBoard[allyBoard]:
            if (card.canAttack):
                for attackable in possibleTargets:
                    if (attackable == -1) and not card.canAttackFace:
                        continue
                    moves.append([ATTACK_ACTION, [currIndex, attackable]])
            currIndex += 1

        # Playing card from hand moves available
        currIndex = 0
        for card in self.activePlayer.hand:
            if self.activePlayer.currPP >= card.monsterCost and len(self.board.fullBoard[allyBoard]) < 5:
                moves.append([PLAY_ACTION, [currIndex]])
            currIndex += 1

        # If we cant evolve, we are done
        if not self.activePlayer.canEvolve:
            return moves

        # Otherwise, Evolving follower moves available, find them
        currIndex = 0
        for card in self.board.fullBoard[allyBoard]:
            if card.canEvolve:
                moves.append([EVO_ACTION, [currIndex]])
            currIndex += 1

        return moves

    # Remove magic numbers from this, maybe implement action as a class. Find some better
    # implementation in any case
    def initiateAction(self, action):
        if action[0] == PASS_ACTION:
            self.endTurn()
        elif action[0] == PLAY_ACTION:
            self.playCard(action)
        elif action[0] == ATTACK_ACTION:
            self.initiateAttack(action[1][0], action[1][1])
        elif action[0] == EVO_ACTION:
            self.initiateEvolve(action[1][0])
        else:
            print("ERROR: Invalid action")

    # This will be used with our MCTS algorithm
    def runToCompletion(self):
        while (self.winner == 0):
            moves = self.generateLegalMoves()
            selection = random.randrange(len(moves))
            print(moves[selection])
            self.initiateAction(moves[selection])
        return self.winner

