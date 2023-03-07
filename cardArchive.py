from monster import Monster

class Goblin(Monster):
  def __init__(self):
    monsterName = "Goblin"
    monsterCost = 1
    monsterAttack = 1
    monsterHealth = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterHealth, monsterName)

class Fighter(Monster):
  def __init__(self):
    monsterName = "Fighter"
    monsterCost = 2
    monsterAttack = 2
    monsterHealth = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterHealth, monsterName)

#class Monster(Card):
#  def __init__(self, monsterCost, monsterAttack, monsterDefense):
#    self.monsterAttack = monsterAttack
#    self.monsterDefense = monsterDefense
#    Card.__init__(self, monsterCost)
