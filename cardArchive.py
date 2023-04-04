from monster import Monster
from cardGeneric import *

class Reaper(Monster):
  def __init__(self):
    monsterName = "Reaper"
    monsterCost = 0
    monsterAttack = 0
    monsterMaxHP = 0
    monsterCurrHP = 0
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

class DeathDragon(Monster):
  def __init__(self):
    monsterName = "Death Dragon"
    monsterCost = 4
    monsterAttack = 4
    monsterMaxHP = 4
    monsterCurrHP = 4
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

class Goliath(Monster):
  def __init__(self):
    monsterName = "Goliath"
    monsterCost = 4
    monsterAttack = 3
    monsterMaxHP = 4
    monsterCurrHP = 4
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

class Mercenary(Monster):
  def __init__(self):
    monsterName = "Mercenary"
    monsterCost = 3
    monsterAttack = 3
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

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
  
