# For generic card functions

def genericTakeDamage(mons, gameState, damage):
    mons.currHP -= damage
    if (mons.currHP <= 0):
        mons.destroy(gameState)
    return damage

def genericDestroy(mons, gameState):
    gameState.queue.append(gameState.removeFollower(mons))

    #gameState.removeFollower(mons)(gameState)
    #TODO: queueify, necessary for disco dragon LW/ward/heal
    # for wrath mirror, I think theres nothing where this matters (only LW are drummer)
    # with this implementation, card LWs activate before the follower is removed, and basically before anything else, so
    # the 0/1/1 ward might heal before infiniflame deals face damage
    for func in mons.LWEffects:
        # TODO: 0 doesnt work here
        func(gameState, mons.side)

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
    if (mons.freeEvolve != 1):
        gameState.activePlayer.currEvos -= 1

def genericPlay(mons, gameState, currPlayer):
    mons.turnPlayed = gameState.currTurn
    mons.side = gameState.activePlayer.playerNum - 1
    gameState.board.fullBoard[currPlayer].append(mons)
    gameState.activePlayer.currPP -= mons.cost
    for ele in mons.fanfareEffects:
        ele(gameState)
    gameState.queue.append(gameState.activateOnSummonEffects(mons))

def genericSummon(mons, gameState, side):
    if (len(gameState.board.fullBoard[side]) < 5):
        mons.turnPlayed = gameState.currTurn
        mons.side = side + 1
        gameState.board.fullBoard[side].append(mons)
        gameState.queue.append(gameState.activateOnSummonEffects(mons))

