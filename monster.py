from card import Card

class Monster(Card):
  def __init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName):
    self.monsterAttack = monsterAttack
    self.monsterMaxHP = monsterMaxHP
    self.monsterCurrHP = monsterCurrHP

    # These are various properties that a monster can have, maybe make this a bit more elegant
    self.canEvolve = 1
    self.isEvolved = 0
    self.hasStorm = 0
    self.hasRush = 0
    Card.__init__(self, monsterCost, monsterName)

