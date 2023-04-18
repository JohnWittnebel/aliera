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

class GiftForBloodKin(Spell):
    def __init__(self):
        spellName = "Gift"
        spellCost = 0
        allyFollowerTargets = 0
        enemyFollowerTargets = 0
        Spell.__init__(self, spellName, spellCost, allyFollowerTargets, enemyFollowerTargets)
        self.encoding = GiftVal
        
    def play(self, gameState, currSide):
        selfPing(1)(gameState)
        enemyPing(1)(gameState, currSide)
        genericSummon(ForestBat(), gameState, currSide)
        genericSummon(ForestBat(), gameState, (currSide + 1) % 2)

class SummonBloodKin(Spell):
    def __init__(self):
        spellName = "Summon BK"
        spellCost = 2
        allyFollowerTargets = 0
        enemyFollowerTargets = 0
        Spell.__init__(self, spellName, spellCost, allyFollowerTargets, enemyFollowerTargets)
        self.encoding = BloodkinVal
        
    def play(self, gameState, currSide):
        genericSummon(ForestBat(), gameState, currSide)
        genericSummon(ForestBat(), gameState, currSide)

##### EFFECT FUNCTIONS

def healFace(val):
    return lambda gameState, side: gameState.player1.restoreHP(gameState, val) if side == 0 \
    else gameState.player2.restoreHP(gameState, val)

def selfPing(val):
    return lambda gameState: gameState.activePlayer.takeEffectDamage(gameState, val)

def enemyPing(val):
    return lambda gameState, side: gameState.player2.takeEffectDamage(gameState, val) if side == 0 \
    else gameState.player1.takeEffectDamage(gameState, val)

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
    for card in gameState.board.fullBoard[gameState.activePlayer.playerNum % 2]:
        card.takeEffectDamage(gameState, 1)

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

class DrummerAccel(Spell):
    def __init__(self):
        spellName = "Drummer Accel"
        spellCost = 2
        allyFollowerTargets = 0
        enemyFollowerTargets = 0
        Spell.__init__(self, spellName, spellCost, allyFollowerTargets, enemyFollowerTargets)
        self.encoding = DrummerVal
        
    def play(self, gameState, currSide):
        genericSummon(Drummer(), gameState, currSide)
        selfPing(1)(gameState)
        selfPing(1)(gameState)
        selfPing(1)(gameState)
        selfPing(1)(gameState)
        selfPing(1)(gameState)
        selfPing(1)(gameState)
        selfPing(1)(gameState)
        genericSummon(Drummer(), gameState, currSide)
        selfPing(1)(gameState)
        gameState.activePlayer.currPP -= self.cost
        return

class Drummer(Monster):
    def __init__(self):
        monsterName = "Drummer (W)"
        cost = 5
        monsterAttack = 1
        monsterMaxHP = 1
        monsterCurrHP = 1
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = DrummerVal

        self.hasWard = 1
        self.canAccel = True
        self.accelCost = 2
        self.accelCard = DrummerAccel()
        self.LWEffects.append(healFace(1))

    # TODO: should probably move this to fanfare effects
    def play(self, gameState, currSide):
        genericPlay(self, gameState, currSide)
        for _ in range(4):
            genericSummon(Drummer(), gameState, currSide)
        if gameState.activePlayer.selfPings >= 7:
            self.evolve(gameState)

    
    # TODO: this is a bit scuffed and doesnt work with silence and probably work work with other protections
    def takeCombatDamage(self, gameState, damage):
        if self.isEvolved and damage > 2:
            return genericTakeDamage(self, gameState, 2)
        else:
            return genericTakeDamage(self, gameState, damage)

    def takeEffectDamage(self, gameState, damage):
        if self.isEvolved and damage > 2:
            return genericTakeDamage(self, gameState, 2)
        else:
            return genericTakeDamage(self, gameState, damage)
    
    def evolve(self, gameState):
        self.LWEffects = [healFace(2)]
        self.freeEvolve = 1
        genericEvolve(self, gameState)

def vampyEffect(gameState, card):
    if card.name == "Forest Bat":
        card.hasBane = 1
        card.hasStorm = 1
        card.canAttack = 1
        if (card.side == 1):
            gameState.player2.takeEffectDamage(gameState, 1)
        else:
            gameState.player1.takeEffectDamage(gameState, 1)

class Vampy(Monster):
    def __init__(self):
        monsterName = "Vampy"
        cost = 2
        monsterAttack = 2
        monsterMaxHP = 2
        monsterCurrHP = 2
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = VampyVal

    # TODO: fanfareify + special venge
    def play(self, gameState, currSide):
        genericPlay(self, gameState, currSide)
        if (len(gameState.activePlayer.hand) < 9):
            gameState.activePlayer.hand.append(GiftForBloodKin())
        if (gameState.activePlayer.selfPings >= 7) or (gameState.activePlayer.currHP <= 10):
            self.freeEvolve = 1
            if (len(gameState.activePlayer.hand) < 9):
                gameState.activePlayer.hand.append(SummonBloodKin())
    
    def evolve(self, gameState):
        self.onSummonEffects.append(vampyEffect)
        genericEvolve(self, gameState)
        
class HowlingDemon(Monster):
    def __init__(self):
        monsterName = "Drummer"
        cost = 5
        monsterAttack = 1
        monsterMaxHP = 1
        monsterCurrHP = 1
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = DrummerVal
        


##### MAIN DECK AMULETS

