from card import Card
from cardGeneric import *

class Spell(Card):
    def __init__(self, name, cost, allyFollowerTargets, enemyFollowerTargets):
        self.name = name
        self.cost = cost
        self.allyFollowerTargets = allyFollowerTargets
        self.enemyFollowerTargets = enemyFollowerTargets

    def play(self, gameState, side):
        # spells dont really have a default action, so just do nothing
        return
