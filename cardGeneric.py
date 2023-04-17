# For generic card functions

def genericTakeDamage(mons, gameState, damage, index, side):
    mons.currHP -= damage
    if (mons.currHP <= 0):
        mons.destroy(gameState, index, side)

def genericDestroy(gameState, index, side):
    cardDestroyed = gameState.board.fullBoard[side].pop(index)
    #TODO: QUEUEIFY
    for func in cardDestroyed.LWEffects:
        func(gameState, side)

def genericEvolve(mons, gameState):
    if (mons.isEvolved):
        print("ERROR: monster is already evolved")
        return
        
    mons.currAttack += 2
    mons.maxAttack += 2
    mons.maxHP += 2
    mons.currHP += 2
    mons.name += "(E)"

    mons.canEvolve = 0
    mons.isEvolved = 1
    if (mons.hasAttacked == 0):
        mons.canAttack = 1
    if (mons.turnPlayed == gameState.currTurn):
        mons.canAttackFace = 0

    gameState.activePlayer.canEvolve = 0
    gameState.activePlayer.currEvos -= 1

def genericPlay(mons, gameState, currPlayer):
    mons.turnPlayed = gameState.currTurn
    gameState.board.fullBoard[currPlayer].append(mons)
    gameState.activePlayer.currPP -= mons.cost
    for ele in mons.fanfareEffects:
        ele(gameState)
    gameState.queue.append(gameState.activateOnPlayEffects(mons))

def genericSummon(mons, gameState, side):
    if (len(gameState.board.fullBoard[side]) < 5):
        mons.turnPlayed = gameState.currTurn
        gameState.board.fullBoard[gameState.activePlayer.playerNum - 1].append(mons)

