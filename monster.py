from card import Card

class Monster(Card):
  def __init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName):
    self.monsterCost = monsterCost
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

    # This is set to true when a monster take damage or effect that will cause it to be destroyed
    # The Game will check this after every move and remove it from play if needed
    self.initiateDestroy = 0
    Card.__init__(self, monsterCost, monsterName)
  
    #@abstractmethod
    def takeCombatDamage(self, damage):
        pass

