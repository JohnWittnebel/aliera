from card import Card
from cardGeneric import *

class Monster(Card):
    def __init__(self, cost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName):
        self.cost = cost
        self.monsterCurrAttack = monsterAttack
        self.monsterMaxAttack = monsterAttack
        self.monsterMaxHP = monsterMaxHP
        self.monsterCurrHP = monsterCurrHP

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

        # Effect Arrays
        self.fanfareEffects = []
        self.LWEffects = []
        self.strikeEffects = []
        self.clashEffects = []
        self.onAllyEvoEffects = []
        self.onPlayEffects = []  # for when an ally follower is played

        self.traits = []
        
        # Battlecry targets
        self.numTargets = 0

        # Evo targets
        self.evoEnemyFollowerTargets = 0
        self.evoAllyFollowerTargets = 0

        # This is set to true when a monster take damage or effect that will cause it to be destroyed
        # The Game will check this after every move and remove it from play if needed
        self.initiateDestroy = 0
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
