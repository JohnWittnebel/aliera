from card import Card
from cardGeneric import *

class Monster(Card):
    def __init__(self, cost, monsterAttack, monsterMaxHP, currHP, monsterName):
        self.cost = cost
        self.currAttack = monsterAttack
        self.monsterMaxAttack = monsterAttack
        self.monsterMaxHP = monsterMaxHP
        self.currHP = currHP

        # These are various properties that a monster can have, maybe make this a bit more elegant
        self.canEvolve = 1
        self.isEvolved = 0
        self.hasStorm = 0
        self.hasRush = 0
        self.canAttack = 0
        self.hasWard = 0
        self.hasDrain = 0
        self.hasAttacked = 0
        self.turnPlayed = 0
        self.canAttackFace = 1
        self.isAttackable = True

        #Enhance/accel
        self.canEnhance = False
        self.canAccel = False
        self.accelCost = 0

        # Effect Arrays
        self.fanfareEffects = []
        self.LWEffects = []
        self.followerStrikeEffects = []
        self.strikeEffects = []
        self.clashEffects = []
        self.onAllyEvoEffects = []
        self.onPlayEffects = []  # for when an ally follower is played
        self.turnEndEffects = []
        self.turnStartEffects = []

        self.traits = []
        
        # Battlecry targets
        self.numTargets = 0

        # Evo targets
        self.evoEnemyFollowerTargets = 0
        self.evoAllyFollowerTargets = 0

        Card.__init__(self, cost, monsterName)

    #@abstractmethod
    def play(self, board, currPlayer, *args, **kwargs):
        genericPlay(self, board, currPlayer)
  
    #@abstractmethod
    def takeCombatDamage(self, gameState, damage, index, side):
        genericTakeDamage(self, gameState, damage, index, side)

    def takeEffectDamage(self, gameState, damage, index, side):
        genericTakeDamage(self, gameState, damage, index, side)
    
    #@classmethod
    def evolve(self, gameState, *args, **kwargs):
        genericEvolve(self, gameState)
    
    # called to actually destroy, activate LW, etc.
    def destroy(self, gameState, index, side, *args, **kwargs):
        genericDestroy(gameState, index, side)

    # called when an effect attempts to destroy (bane, destroy follower, etc.). Might not actually
    # destroy if the target has protection
    def effectDestroy(self, gameState, index, side, *args, **kwargs):
        genericDestroy(gameState, index, side)

    def followerStrike(self, gameState, allyIndex, activeSide, enemyMonster, enemyIndex, *args, **kwargs):
        for func in self.strikeEffects:
            func(gameState, activeSide)
        for func in self.clashEffects:
            func(gameState, activeSide, enemyMonster)
        for func in self.followerStrikeEffects:
            func(gameState, activeSide, enemyMonster)
        for func in enemyMonster.clashEffects:
            func(gameState, (activeSide+1)%2, self)
        combatDamageToTake = enemyMonster.currAttack
        enemyMonster.takeCombatDamage(gameState, self.currAttack, enemyIndex, (activeSide+1)%2)
        self.takeCombatDamage(gameState, combatDamageToTake, allyIndex, activeSide)
