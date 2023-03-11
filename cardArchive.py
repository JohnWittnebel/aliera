from monster import Monster

class Goblin(Monster):
  def __init__(self):
    monsterName = "Goblin"
    monsterCost = 1
    monsterAttack = 1
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

  #TODO: make this a generic takeCombatDamage function
  def takeCombatDamage(self, damage):
    self.monsterCurrHP -= damage
    if (self.monsterCurrHP <= 0):
        self.initiateDestroy = 1
      

class Fighter(Monster):
  def __init__(self):
    monsterName = "Fighter"
    monsterCost = 2
    monsterAttack = 2
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
  
  def takeCombatDamage(self, damage):
    self.monsterCurrHP -= damage
    if (self.monsterCurrHP <= 0):
        self.initiateDestroy = 1

#class Monster(Card):
#  def __init__(self, monsterCost, monsterAttack, monsterDefense):
#    self.monsterAttack = monsterAttack
#    self.monsterDefense = monsterDefense
#    Card.__init__(self, monsterCost)
