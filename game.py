import os
from board import Board
from player import Player
from spell import Spell
from monster import Monster
from amulet import Amulet
from constants import *
from deck import Deck
import copy
import random

# A Game is the primary class that controls the flow of the game
# It has 2 players, a board, and keeps track of who is the current player and the current turn
# It has a winner field that will change to 1 or 2 depending on the winner of the game
# the winString returns the reason for winning (deckout, hp reached 0, etc.)

# training variables
TRAINING = 1

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
    
    # This is meant to really only be used by the trueCopy function
    def update(self, player1, player2, activePlayer, gameBoard, currTurn, winner):
        self.activePlayer = activePlayer
        self.player1 = player1
        self.player2 = player2
        self.board = gameBoard
        self.currTurn = currTurn

        # this will become 1 or 2 once the game is over
        self.winner = winner
        self.winString = ""
    
    def __init__(self):
        # If we are initializing a board state without players already generated,
        # we need to generate the players and the decks that they will be using

        deck1 = Deck("deck1")
        deck2 = Deck("deck2")
        self.p1played = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.p2played = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.player1 = Player(deck1, PLAYER_1_MAX_EVOS, PLAYER_1_MAX_EVOS, 1)
        self.player2 = Player(deck2, PLAYER_2_MAX_EVOS, PLAYER_2_MAX_EVOS, 2)

        self.board = Board()
        self.activePlayer = self.player1
        self.currTurn = 1
        self.winner = 0
        self.winString = ""
        self.queue = []

    def printGameState(self):
        os.system('clear')
        if (self.activePlayer == self.player1):
            print("Active player: 1")
            print("HP: " + str(self.player2.currHP) + "/" + str(self.player2.maxHP))
            print("Cards: " + str(len(self.player2.hand)))
            print("PP: " + str(self.player2.currPP) + "/" + str(self.player2.maxPP))
            print("Evos: " + str(self.player2.currEvos))
            print("")
            self.board.printBoard()
            print("")
            print("HP: " + str(self.player1.currHP) + "/" + str(self.player1.maxHP))
            print("PP: " + str(self.player1.currPP) + "/" + str(self.player1.maxPP))
            print("Evos: " + str(self.player1.currEvos))
            print("Hand:")
            self.player1.printHand()
        else:
            print("Active player: 2")
            print("HP: " + str(self.player2.currHP) + "/" + str(self.player2.maxHP))
            print("Cards: " + str(len(self.player1.hand)))
            print("PP: " + str(self.player2.currPP) + "/" + str(self.player2.maxPP))
            print("Evos: " + str(self.player2.currEvos))
            print("")
            self.board.printBoard()
            print("")
            print("HP: " + str(self.player1.currHP) + "/" + str(self.player1.maxHP))
            print("PP: " + str(self.player1.currPP) + "/" + str(self.player1.maxPP))
            print("Evos: " + str(self.player1.currEvos))
            print("Hand:")
            self.player2.printHand()

    def initiateEvolve(self, allyMonsterIndex):
        if (not self.activePlayer.canEvolve): 
            input("ERROR: this player cannot evolve")
            return
        
        if self.activePlayer == self.player1:
            evolveTarget = self.board.fullBoard[0][allyMonsterIndex[0]]
        else:
            evolveTarget = self.board.fullBoard[1][allyMonsterIndex[0]]
            
        if ((self.activePlayer.currEvos == 0) and evolveTarget.freeEvolve == 0):
            input("ERROR: not enough evolves")
            return

        if evolveTarget.evoEnemyFollowerTargets > 0 and len(self.board.fullBoard[(self.activePlayer.playerNum+1) % 2]) > 0:
            evolveTarget.evolve(self, allyMonsterIndex[1:], self.activePlayer.playerNum % 2)
        else:
            evolveTarget.evolve(self)

    def initiateAttack(self, allyMonster, enemyMonster):
    
        # First, figure out what side is attacking
        attackingPlayer = self.activePlayer.playerNum - 1
        defendingPlayer = self.activePlayer.playerNum % 2

        # VALID TARGETS CHECKING
        # Make sure that the allyMonster attacking a valid target, and that the enemyMonster is a valid target
        if (allyMonster > len(self.board.fullBoard[attackingPlayer]) - 1):
            self.printGameState()
            print(allyMonster, enemyMonster)
            input("ERROR: attempt to use a non-existent monster to attack")
            return
        elif (allyMonster < 0):
            self.printGameState()
            print(allyMonster, enemyMonster)
            input("ERROR: attempt to use a non-existent monster to attack")
            return
        elif (enemyMonster > len(self.board.fullBoard[defendingPlayer]) - 1):
            self.printGameState()
            print(allyMonster, enemyMonster)
            input("ERROR: attempt to attack a non-existent target")
            return
        elif (enemyMonster < -1):
            self.printGameState()
            print(allyMonster, enemyMonster)
            input("ERROR: attempt to attack a non-existent target")
            return
        elif (not self.board.fullBoard[attackingPlayer][allyMonster].canAttack):
            self.printGameState()
            print(allyMonster, enemyMonster)
            input("ERROR: attempt to attack with a monster that cannot attack")
            return
        elif (enemyMonster == -1 and not self.board.fullBoard[attackingPlayer][allyMonster].canAttackFace):
            input("ERROR: this monster cannot attack face")
            return

        # VALID TARGETS CHECKING FOR WARDS, this might need to become more general
        wardExists = 0
        for enem in self.board.fullBoard[defendingPlayer]:
            if enem.hasWard:
                wardExists = 1
        if wardExists and (enemyMonster == ENEMY_FACE or not self.board.fullBoard[defendingPlayer][enemyMonster].hasWard):
            input("ERROR: attempt to attack through a ward")
            return

        # Actual Fuction

        # Give summoning sickness to the monster that just attacked, do this here
        # because the monster might stop existing after attacking, and then we would apply
        # summoning sickness to a different monster (or out of index error)
        # TODO: put these into the followerStrike/leaderStrike functions
        self.board.fullBoard[attackingPlayer][allyMonster].canAttack = 0
        self.board.fullBoard[attackingPlayer][allyMonster].hasAttacked = 1

        # Face is being attacked
        if (enemyMonster == ENEMY_FACE):
            if (attackingPlayer == 0):
                self.board.player1side[allyMonster].leaderStrike(self, allyMonster)
            else:
                self.board.player2side[allyMonster].leaderStrike(self, allyMonster)

        # otherwise, we are attacking a monster, deal damage to each other
        else:
            attackingMonster = self.board.fullBoard[attackingPlayer][allyMonster]
            defMonster = self.board.fullBoard[defendingPlayer][enemyMonster]
            attackingMonster.followerStrike(self, allyMonster, attackingPlayer, defMonster, enemyMonster)
        self.clearQueue()

    def endgame(self, winner):
        if winner == 1:
            #input("The winner is player 1")
            self.winner = 1
        else:
            #input("The winner is player 2")
            self.winner = 2
        #print("Cause of win: " + self.winString)

    # Note that function might also become bloated with time, be careful!
    # For now, nothing has a battlecry, so just place it on the field
    # Once spells are implemented, have this split into 2 separate functions
    def playCard(self, action):
        # First, figure out what side is playing cards
        currPlayer = self.activePlayer.playerNum - 1

        card = self.activePlayer.hand[action[1][0]]
        if (currPlayer == 0):
            self.p1played[card.encoding] += 1
        else:
            self.p2played[card.encoding] += 1

        # Check if we are acceling
        if (isinstance(card, Monster) and self.activePlayer.currPP < card.cost and card.canAccel and self.activePlayer.currPP >= card.accelCost):
            accelerating = True
        else:
            accelerating = False

        # Check that board is not full
        if (len(self.board.fullBoard[currPlayer]) == MAX_BOARD_SIZE and (not isinstance(card,Spell)) and (not accelerating)):
            print("Attempted to play a follower when the board is full")
            return

        # Make sure that we have the PP to play the follower/spell
        if self.activePlayer.currPP < self.activePlayer.hand[action[1][0]].cost and not accelerating:
            print("Attempted to play a card that costs more than our current PP")
            return
        
        cardToPlay = self.activePlayer.hand.pop(action[1][0])
        if accelerating:
            cardToPlay = cardToPlay.accelCard

        if (cardToPlay.numTargets == 0):
            cardToPlay.play(self, currPlayer)
        else:
            cardToPlay.play(self, currPlayer, action[1][1:])

    def endTurn(self):
        self.activateTurnEndEffects(None)
        self.clearQueue()

        # Allow all followers to attack again
        for mons in self.board.player1side:
            mons.effActivations = 0
            if (mons.isAmulet) and (mons.isCountdown) and (self.activePlayer.playerNum == 1):
                mons.countdown -= 1
                if mons.countdown == 0:
                    mons.destroy(self)
            elif (not mons.isAmulet):
                mons.canAttack = 1
                mons.canAttackFace = 1
        for mons in self.board.player2side:
            mons.effActivations = 0
            if (mons.isAmulet) and (mons.isCountdown) and (self.activePlayer.playerNum == 2):
                mons.countdown -= 1
                if mons.countdown == 0:
                    mons.destroy(self)
            elif (not mons.isAmulet):
                mons.canAttack = 1
                mons.canAttackFace = 1

        #self.clearQueue()

        # Change the current active player
        if (self.activePlayer == self.player1):
            self.activePlayer.selfPingsTurn = 0
            self.activePlayer = self.player2
        else:
            self.activePlayer.selfPingsTurn = 0
            self.activePlayer = self.player1
        
        # Change the turn number
        if (self.activePlayer == self.player1):
            self.currTurn += 1
        
        self.startTurn()

    def startTurn(self):
        self.activateTurnStartEffects(None)
        self.clearQueue()
        # Increase max PP of the current player
        if (self.activePlayer.maxPP < MAX_EMPTY_PP):
          self.activePlayer.maxPP += 1

        # Set active player current PP equal to their new max
        self.activePlayer.currPP = self.activePlayer.maxPP
 
        # Set if the player has the ability to evolve or not on this turn
        if (self.activePlayer == self.player1 and self.currTurn >= PLAYER_1_EVO_TURN):
            self.activePlayer.canEvolve = 1
        elif (self.activePlayer == self.player2 and self.currTurn >= PLAYER_2_EVO_TURN):
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
                self.endgame(2)
            else:
                self.endgame(1)


    #def mulligan(self, player):
    #    mull = player.mulliganSample(1,1,0)
    #    player.returnMulliganSample(mull)

    # this function will have the initial drawing and mulligan phase
    def gameStart(self):
        self.winner = 0
        self.player1.draw(3)
        self.player2.draw(3)
       
        if (len(self.player1.deck.cards) == 0):
            raise Exception("no cards in deck at start")
        
        #self.mulligan(self.player1)
        #self.mulligan(self.player2)

        #self.startTurn()

    # this function is mostly to deal with ward, but can be expanded to include other specific cards
    def attackableTargets(self):
        targets = []
        if self.activePlayer == self.player1:
            targetPlayer = 1
        else:
            targetPlayer = 0

        tempTargets = []
        # Ward check
        wards = []
        wardIndex = 0
        for follower in self.board.fullBoard[targetPlayer]:
            if follower.hasWard:
                wards.append(wardIndex)
            if follower.isAttackable:
                tempTargets.append(wardIndex)
            wardIndex += 1
  
        if wards == []:
            targets.append(-1)
            targets += tempTargets
        else:
            targets = wards

        return targets

    # Helper function for generating legal moves for playing cards
    def addLegalMovesForCard(self, card, moves, currIndex):
        allyBoard = self.activePlayer.playerNum - 1
        if (card.numTargets == 0):
            moves.append([PLAY_ACTION, [currIndex]])
            # For now we only support battlecries that have a single target
        if (card.fanfareTargetFace):
            moves.append([PLAY_ACTION, [currIndex, -1]])
        if (card.numEnemyFollowerTargets == 1):
            for targetIndex in range(len(self.board.fullBoard[(allyBoard+1) % 2])):
                if isinstance(self.board.fullBoard[(allyBoard+1) % 2][targetIndex], Monster):
                    moves.append([PLAY_ACTION, [currIndex, targetIndex]])
        elif (card.numAllyFollowerTargets == 1):
            for targetIndex in range(len(self.board.fullBoard[allyBoard])):
                if isinstance(self.board.fullBoard[allyBoard][targetIndex], Monster):
                    moves.append([PLAY_ACTION, [currIndex, targetIndex]])

    def generateLegalMoves(self):
        self.clearQueue()
        moves = []

        allyBoard = self.activePlayer.playerNum - 1
        
        # Playing card from hand moves available
        currIndex = 0
        for card in self.activePlayer.hand:
            # Check for accel
            if (isinstance(card, Monster) and self.activePlayer.currPP < card.cost and card.canAccel and self.activePlayer.currPP >= card.accelCost):
                accelerating = True
            else:
                accelerating = False
             
            # We are accelerating
            if (accelerating):
                self.addLegalMovesForCard(card.accelCard, moves, currIndex)

            # Not acceling, but there is either room for the card, or it is a spell
            if self.activePlayer.currPP >= card.cost and (len(self.board.fullBoard[allyBoard]) < 5 or isinstance(card,Spell)):
                self.addLegalMovesForCard(card, moves, currIndex)

            currIndex += 1

        # Attacking moves available
        currIndex = 0
        possibleTargets = self.attackableTargets()
        for card in self.board.fullBoard[allyBoard]:
            if (card.canAttack):
                for attackable in possibleTargets:
                    if (attackable == -1) and not card.canAttackFace:
                        continue
                    moves.append([ATTACK_ACTION, [currIndex, attackable]])
            currIndex += 1

        # If we cant evolve, we are done
        if not self.activePlayer.canEvolve:
            moves.append([PASS_ACTION])
            return moves

        # Otherwise, Evolving follower moves available, find them
        currIndex = 0
        for card in self.board.fullBoard[allyBoard]:
            if card.canEvolve and ((self.activePlayer.currEvos > 0) or (card.freeEvolve)):
                # TODO: ally targeting at some point
                if card.evoEnemyFollowerTargets == 0:
                    moves.append([EVO_ACTION, [currIndex]])
                elif card.evoEnemyFace == 0 and len(self.board.fullBoard[(allyBoard+1) % 2]) == 0:
                    moves.append([EVO_ACTION, [currIndex]])
                else:
                    if card.evoEnemyFace == True:
                        moves.append([EVO_ACTION, [currIndex, -1]])
                    for targetIndex in range(len(self.board.fullBoard[(allyBoard+1) % 2])):
                        moves.append([EVO_ACTION, [currIndex, targetIndex]])
            currIndex += 1

        moves.append([PASS_ACTION])

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
            self.initiateEvolve(action[1])
        else:
            print("ERROR: Invalid action:")
            input(action)

    # This is used for rollouts on a MCTS, but we dont actually do this with our AZ implementation
    def runToCompletion(self):
        while (self.winner == 0):
            moves = self.generateLegalMoves()
            selection = random.randrange(len(moves))
            #print(moves[selection])
            self.initiateAction(moves[selection])
        return self.winner

    def removeFollowerLambda(self, mons):
        for side in self.board.fullBoard:
            for item in side:
                if item == mons:
                    side.remove(mons)

    def removeFollower(self, mons):
        return lambda gameState: gameState.removeFollowerLambda(mons) 

    def activateOnPlayEffects(self, card):
        self.activePlayer.leaderEffects.activateOnPlayEffects(self, card)

    def activateOnSummonEffects(self, card):
        if card.side == 1:
            self.player1.leaderEffects.activateOnSummonEffects(self, card)
        else:
            self.player2.leaderEffects.activateOnSummonEffects(self, card)
        for item in self.board.fullBoard[card.side]:
            for eff in item.onSummonEffects:
                eff(self, card)

    def activateSelfPingEffects(self, nothing):
        self.activePlayer.leaderEffects.activateSelfPingEffects(self)
        for card in self.board.fullBoard[self.activePlayer.playerNum - 1]:
            for eff in card.selfPingEffects:
                eff(card, self)

    def activateHealEffects(self, nothing):
        self.activePlayer.leaderEffects.activateHealEffects(self)
        for card in self.board.fullBoard[self.activePlayer.playerNum - 1]:
            for eff in card.selfHealEffects:
                eff(self)
    
    def activateTurnEndEffects(self, placholder):
        self.activePlayer.leaderEffects.activateTurnEndEffects(self)
        for card in self.board.fullBoard[self.activePlayer.playerNum - 1]:
            for eff in card.turnEndEffects:
                eff(self)
    
    def activateTurnStartEffects(self, placholder):
        self.activePlayer.leaderEffects.activateTurnStartEffects(self)
        for card in self.board.fullBoard[self.activePlayer.playerNum - 1]:
            for eff in card.turnStartEffects:
                eff(self)

    def clearQueue(self):
        queueIndex = 0
        while queueIndex < len(self.queue):
            if self.queue[queueIndex] != None:
                self.queue[queueIndex](self)
            queueIndex += 1
        self.queue = []
