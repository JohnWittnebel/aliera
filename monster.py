from card import Card

class Monster(Card):
  def __init__(self, monsterCost, monsterAttack, monsterDefense, monsterName):
    self.monsterAttack = monsterAttack
    self.monsterDefense = monsterDefense
    Card.__init__(self, monsterCost, monsterName)

