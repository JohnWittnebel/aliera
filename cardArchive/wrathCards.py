from monster import Monster
from spell import Spell
from cardGeneric import *
from constants import *

import sys
sys.path.insert(0, '..')

##### TOKENS

class ForestBat(Monster):
    def __init__(self):
        monsterName = "Forest Bat"
        cost = 1
        monsterAttack = 1
        monsterMaxHP = 1
        monsterCurrHP = 1
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = BatVal

##### EFFECT FUNCTIONS

def selfPing(val):
    return lambda gameState: gameState.activePlayer.takeEffectDamage(gameState, val)

def summonBat():
    x = ForestBat()
    return lambda gameState: genericSummon(x, gameState, gameState.activePlayer.playerNum-1)

def draw(val):
    return lambda gameState: gameState.activePlayer.draw(val)

def givePlus1Bats(gameState):
    if gameState.activePlayer.selfPings >= 7:
        for card in gameState.board.fullBoard[gameState.activePlayer.playerNum - 1]:
            if card.name == "Forest Bat":
                card.maxHP += 1
                card.currHP += 1
                card.currAttack += 1


def drawCondemn(gameState):
    index = 0
    for card in gameState.activePlayer.deck.cards:
        if len(card.traits) > 0 and card.traits[0] == "condemn":
            cardToDraw = gameState.activePlayer.deck.cards.pop(index)
            gameState.activePlayer.deck.shuffle()
            if (len(gameState.activePlayer.hand) < 9):
                gameState.activePlayer.hand.append(cardToDraw)
            break
        index += 1

def AoEEnemy(gameState):
    index = 0
    for card in gameState.board.fullBoard[gameState.activePlayer.playerNum % 2]:
        card.takeEffectDamage(gameState, 1, index, gameState.activePlayer.playerNum % 2)
        index += 1

##### MAIN DECK MONSTERS

class Veight(Monster):
    def __init__(self):
        monsterName = "Veight"
        cost = 4
        monsterAttack = 2
        monsterMaxHP = 2
        monsterCurrHP = 2
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = VeightVal

        self.evoEnemyFollowerTargets = 1
        self.fanfareEffects.append(selfPing(1))
        self.fanfareEffects.append(summonBat())
        self.fanfareEffects.append(draw(1))
        self.fanfareEffects.append(selfPing(1))
        self.fanfareEffects.append(summonBat())
        self.fanfareEffects.append(draw(1))
    
        self.turnEndEffects.append(givePlus1Bats)

    def evolve(self, gameState, target, targetSide, *args, **kwargs):
        genericEvolve(self, gameState)
            
        enemyPlayer = gameState.activePlayer.playerNum % 2
        if (len(gameState.board.fullBoard[enemyPlayer]) > target[0]):
            gameState.board.fullBoard[enemyPlayer][target[0]].takeEffectDamage(gameState, 4, target[0], targetSide)
        
        if (len(gameState.board.fullBoard[gameState.activePlayer.playerNum - 1]) == 5):
            return

        amuletSummoned = False
        deckIndex = 0
        for ele in gameState.activePlayer.deck.cards:
            if amuletSummoned:
                break
            if isinstance(ele, Amulet):
                cardToSummon = gameState.deck.cards.pop(deckIndex)
                genericSummon(cardToSummon, gameState, gameState.activePlayer.playerNum-1)
                amuletSummoned = True
                deckIndex += 1

class RagingCommander(Monster):
    def __init__(self):
        monsterName = "Raging Comm"
        cost = 3
        monsterAttack = 3
        monsterMaxHP = 1
        monsterCurrHP = 1
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = RCVal
        self.traits.append("condemn")

        self.selfPingEffects.append(AoEEnemy)
        self.fanfareEffects.append(selfPing(1))
        self.fanfareEffects.append(drawCondemn)
        
##### MAIN DECK AMULETS

