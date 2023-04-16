from monster import Monster
from spell import Spell
from cardGeneric import *
from constants import *

import sys
sys.path.insert(0, '..')

class Reaper(Monster):
    def __init__(self):
        monsterName = "Reaper"
        cost = 0
        monsterAttack = 0
        monsterMaxHP = 0
        monsterCurrHP = 0
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

class DeathDragon(Monster):
    def __init__(self):
        monsterName = "Death Dragon"
        cost = 4
        monsterAttack = 4
        monsterMaxHP = 4
        monsterCurrHP = 4
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = DeathDragonVal

def dealFaceDamage(val):
    return lambda gameState, side: gameState.player1.takeEffectDamage(gameState, val) if side == 0 \
    else gameState.player2.takeEffectDamage(gameState, val)

class Maiden(Monster):
    def __init__(self):  
        monsterName = "Maiden (W)"
        cost = 1
        monsterAttack = 1
        monsterMaxHP = 1
        monsterCurrHP = 1
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

        self.hasWard = 1
        self.evoEnemyFollowerTargets = 1
        self.encoding = MaidenVal
        self.LWEffects.append(dealFaceDamage(2))
        
    def evolve(self, gameState, target, targetSide, *args, **kwargs):
        genericEvolve(self, gameState)
        self.monsterMaxHP -= 1
        self.currHP -= 1
        self.currAttack -= 1
            
        enemyPlayer = gameState.activePlayer.playerNum % 2
        if (len(gameState.board.fullBoard[enemyPlayer]) > target[0]):
            gameState.board.fullBoard[enemyPlayer][target[0]].takeEffectDamage(gameState, 3, target[0], targetSide)

class Goliath(Monster):
  def __init__(self):
    monsterName = "Goliath"
    cost = 4
    monsterAttack = 3
    monsterMaxHP = 4
    monsterCurrHP = 4
    Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
    self.encoding = GoliathVal

class Mercenary(Monster):
  def __init__(self):
    monsterName = "Mercenary"
    cost = 3
    monsterAttack = 3
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
    self.encoding = MercVal

class Goblin(Monster):
  def __init__(self):
    monsterName = "Goblin"
    cost = 1
    monsterAttack = 1
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
    self.encoding = GoblinVal

def givePlusOne(gameState, card):
    if (isinstance(card, Monster)):
        card.currAttack += 1
        card.currHP += 1
        card.monsterMaxHP += 1

class Fighter(Monster):
    def __init__(self):
        monsterName = "Fighter"
        cost = 2
        monsterAttack = 2
        monsterMaxHP = 2
        monsterCurrHP = 2
        Monster.__init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = FighterVal

    # Giving leader effect
    def play(self, gameState, currSide):
        genericPlay(self, gameState, currSide)
        if (givePlusOne not in gameState.activePlayer.leaderEffects.onPlayEffects):
            gameState.activePlayer.leaderEffects.onPlayEffects.append(givePlusOne)

    # Remove leader effect when this follower leaves play
    def destroy(self, gameState, index, currSide):
        if currSide:
            currPlayer = gameState.player2
        else:
            currPlayer = gameState.player1
        currPlayer.leaderEffects.onPlayEffects = filter(lambda a: a != givePlusOne, currPlayer.leaderEffects.onPlayEffects)
        genericDestroy(gameState, index, currSide) 

class DragonBreath(Spell):
    def __init__(self):
        spellName = "Dragon's breath"
        spellCost = 2
        allyFollowerTargets = 0
        enemyFollowerTargets = 1
        Spell.__init__(self, spellName, spellCost, allyFollowerTargets, enemyFollowerTargets)
        self.encoding = GoliathVal
        
    def play(self, gameState, currSide, targets):
        damage = 2
        enemySide = (currSide + 1) % 2
        targetIndex = targets[0]
        gameState.board.fullBoard[enemySide][targetIndex].takeEffectDamage(gameState, damage, targetIndex, enemySide)
        gameState.activePlayer.draw(2)
        gameState.activePlayer.currPP -= self.cost
        return
