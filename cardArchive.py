from monster import Monster

class Goblin(Monster):
  def __init__(self):
    monsterName = "Goblin"
    monsterCost = 1
    monsterAttack = 1
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

class Fighter(Monster):
  def __init__(self):
    monsterName = "Fighter"
    monsterCost = 2
    monsterAttack = 2
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

#class Monster(Card):
#  def __init__(self, monsterCost, monsterAttack, monsterDefense):
#    self.monsterAttack = monsterAttack
#    self.monsterDefense = monsterDefense
#    Card.__init__(self, monsterCost)
