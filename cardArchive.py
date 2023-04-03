from monster import Monster

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

  #TODO: make this a generic takeCombatDamage function
  def takeCombatDamage(self, damage):
    self.monsterCurrHP -= damage
    if (self.monsterCurrHP <= 0):
        self.initiateDestroy = 1
  
  #TODO: make this a generic takeCombatDamage function
  def evolve(self, gameState):
      self.monsterCurrAttack += 2
      self.monsterMaxAttack += 2
      self.monsterMaxHP += 2
      self.monsterCurrHP += 2
      self.monsterName += "(E)"

      self.canEvolve = 0
      self.isEvolved = 1
      if (self.hasAttacked == 0):
          self.canAttack = 1

class Goliath(Monster):
  def __init__(self):
    monsterName = "Goliath"
    monsterCost = 4
    monsterAttack = 3
    monsterMaxHP = 4
    monsterCurrHP = 4
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

  #TODO: make this a generic takeCombatDamage function
  def takeCombatDamage(self, damage):
    self.monsterCurrHP -= damage
    if (self.monsterCurrHP <= 0):
        self.initiateDestroy = 1
  
  #TODO: make this a generic takeCombatDamage function
  def evolve(self, gameState):
      self.monsterCurrAttack += 2
      self.monsterMaxAttack += 2
      self.monsterMaxHP += 2
      self.monsterCurrHP += 2
      self.monsterName += "(E)"

      self.canEvolve = 0
      self.isEvolved = 1
      if (self.hasAttacked == 0):
          self.canAttack = 1

class Mercenary(Monster):
  def __init__(self):
    monsterName = "Mercenary"
    monsterCost = 3
    monsterAttack = 3
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

  #TODO: make this a generic takeCombatDamage function
  def takeCombatDamage(self, damage):
    self.monsterCurrHP -= damage
    if (self.monsterCurrHP <= 0):
        self.initiateDestroy = 1
  
  #TODO: make this a generic takeCombatDamage function
  def evolve(self, gameState):
      self.monsterCurrAttack += 2
      self.monsterMaxAttack += 2
      self.monsterMaxHP += 2
      self.monsterCurrHP += 2
      self.monsterName += "(E)"

      self.canEvolve = 0
      self.isEvolved = 1
      if (self.hasAttacked == 0):
          self.canAttack = 1

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
  
  #TODO: make this a generic takeCombatDamage function
  def evolve(self, gameState):
      self.monsterCurrAttack += 2
      self.monsterMaxAttack += 2
      self.monsterMaxHP += 2
      self.monsterCurrHP += 2
      self.monsterName += "(E)"

      self.canEvolve = 0
      self.isEvolved = 1
      if (self.hasAttacked == 0):
          self.canAttack = 1
      

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

  #TODO: make this a generic takeCombatDamage function
  def evolve(self, gameState):
      self.monsterCurrAttack += 2
      self.monsterMaxAttack += 2
      self.monsterMaxHP += 2
      self.monsterCurrHP += 2
      self.monsterName += "(E)"

      self.canEvolve = 0
      self.isEvolved = 1
      if (self.hasAttacked == 0):
          self.canAttack = 1

#class Monster(Card):
#  def __init__(self, monsterCost, monsterAttack, monsterDefense):
#    self.monsterAttack = monsterAttack
#    self.monsterDefense = monsterDefense
#    Card.__init__(self, monsterCost)
