from card import Card
from cardGeneric import *

class Spell(Card):
    def __init__(self, name, cost, allyFollowerTargets, enemyFollowerTargets):
        self.name = name
        self.cost = cost
        self.numAllyFollowerTargets = allyFollowerTargets
        self.numEnemyFollowerTargets = enemyFollowerTargets
        self.numTargets = self.numAllyFollowerTargets + self.numEnemyFollowerTargets

    def play(self, gameState, side, *args, **kwargs):
        # spells dont really have a default action, so just do nothing
        return
