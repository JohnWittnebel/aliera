from monster import Monster
from cardGeneric import *
from constants import *

class Reaper(Monster):
    def __init__(self):
        monsterName = "Reaper"
        monsterCost = 0
        monsterAttack = 0
        monsterMaxHP = 0
        monsterCurrHP = 0
        Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

class DragonWarrior(Monster):
    def __init__(self):
        monsterName = "Dragon Warrior"
        monsterCost = 4
        monsterAttack = 3
        monsterMaxHP = 4
        monsterCurrHP = 4
        Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = MaidenVal

        self.evoEnemyTargets = 1

        def evolve(self, gameState, targets):
            self.genericEvolve(gameState)
            self.monsterMaxHP -= 1
            self.monsterCurrHP -= 1
            self.monsterCurrAttack -= 1
            
            enemyPlayer = (gameState.activePlayer.playerNum + 1) % 2
            gameState.fullBoard[enemyPlayer][targets[0]].takeEffectDamage(3)


class DeathDragon(Monster):
    def __init__(self):
        monsterName = "Death Dragon"
        monsterCost = 4
        monsterAttack = 4
        monsterMaxHP = 4
        monsterCurrHP = 4
        Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
        self.encoding = DeathDragonVal

class Maiden(Monster):
    def __init__(self):  
        monsterName = "Maiden (W)"
        monsterCost = 1
        monsterAttack = 1
        monsterMaxHP = 1
        monsterCurrHP = 1
        Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)

        self.hasWard = 1
        self.evoEnemyFollowerTargets = 1
        self.encoding = MaidenVal
        
    def evolve(self, gameState, target, targetSide, *args, **kwargs):
        genericEvolve(self, gameState)
        self.monsterMaxHP -= 1
        self.monsterCurrHP -= 1
        self.monsterCurrAttack -= 1
            
        enemyPlayer = gameState.activePlayer.playerNum % 2
        if (len(gameState.board.fullBoard[enemyPlayer]) > target[0]):
            gameState.board.fullBoard[enemyPlayer][target[0]].takeEffectDamage(gameState, 3, target[0], targetSide)
    
class Goliath(Monster):
  def __init__(self):
    monsterName = "Goliath"
    monsterCost = 4
    monsterAttack = 3
    monsterMaxHP = 4
    monsterCurrHP = 4
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
    self.encoding = GoliathVal

class Mercenary(Monster):
  def __init__(self):
    monsterName = "Mercenary"
    monsterCost = 3
    monsterAttack = 3
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
    self.encoding = MercVal

class Goblin(Monster):
  def __init__(self):
    monsterName = "Goblin"
    monsterCost = 1
    monsterAttack = 1
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
    self.encoding = GoblinVal

class Fighter(Monster):
  def __init__(self):
    monsterName = "Fighter"
    monsterCost = 2
    monsterAttack = 2
    monsterMaxHP = 2
    monsterCurrHP = 2
    Monster.__init__(self, monsterCost, monsterAttack, monsterMaxHP, monsterCurrHP, monsterName)
    self.encoding = FighterVal
  
