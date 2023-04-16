from card import Card
from cardGeneric import *

class Amulet(Card):
    def __init__(self, name, cost, allyFollowerTargets, enemyFollowerTargets, isCountdown, countdown):
        self.name = name
        self.cost = cost
        self.numAllyFollowerTargets = allyFollowerTargets
        self.numEnemyFollowerTargets = enemyFollowerTargets
        self.numTargets = self.numAllyFollowerTargets + self.numEnemyFollowerTargets
        self.isCountdown = isCountdown
        self.countdown = countdown

        # Effect Arrays
        self.fanfareEffects = []
        self.LWEffects = []
        self.strikeEffects = []
        self.clashEffects = []
        self.onAllyEvoEffects = []
        self.onPlayEffects = []  # for when an ally follower is played
        self.turnEndEffects = []
        self.turnStartEffects = []

    def play(self, gameState, side, *args, **kwargs):
        genericPlay(self, gameState, side)
