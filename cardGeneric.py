# For generic card functions

def genericTakeCombatDamage(mons, damage):
    mons.monsterCurrHP -= damage
    if (mons.monsterCurrHP <= 0):
        mons.initiateDestroy = 1
  
def genericEvolve(mons, gameState):
    if (mons.isEvolved):
        print("ERROR: monster is already evolved")
        return
        
    mons.monsterCurrAttack += 2
    mons.monsterMaxAttack += 2
    mons.monsterMaxHP += 2
    mons.monsterCurrHP += 2
    mons.name += "(E)"

    mons.canEvolve = 0
    mons.isEvolved = 1
    if (mons.hasAttacked == 0):
        mons.canAttack = 1

    gameState.activePlayer.canEvolve = 0
    gameState.activePlayer.currEvos -= 1

def genericPlay(mons, gameState, currPlayer):
    mons.turnPlayed = gameState.currTurn
    gameState.board.fullBoard[currPlayer].append(mons)
    gameState.activePlayer.currPP -= mons.monsterCost
