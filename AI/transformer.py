# The transformer is a liason between the NN and the Game class
# it takes the output of the NN and interprets it for the Game,
# and takes the game state and condenses it into a digestible form
# for the NN

class Transformer:
    def __init__(self):
        #TODO: this needs access to the array of possible cards that the deck can contain
        #      for now we will just do it like this, but this REALLY needs to be done better
        self.mapping = ["Goblin", "Fighter"]
        return

    #For our Fighter+Goblin toy game, we will have:
    #30 board inputs (15 each side) (attack/defense/attackable status)
    #2 hand inputs (number of goblins, number of fighters)
    #2 hp inputs (ours + enemy)
    #1 handsize input (opp hand size)
    #2 PP inputs (our current, our max)

    def gameDataToNN(self, allyBoard, enemyBoard, hand, currPlayerHP, enemyPlayerHP, enemyCardNum, currPP, maxPP):
        generatedData = []

        # First we generate the board state and add it to the array
        for mons in allyBoard:
            generatedData.append(mons.monsterCurrAttack)
            generatedData.append(mons.monsterCurrHP)
            generatedData.append(mons.canAttack)
        # we need to generate 0's for the rest of ally board
        for _ in range(5 - len(allyBoard)):
            generatedData.append(0)
            generatedData.append(0)
            generatedData.append(0)

        # repeat for enemy side
        for mons in enemyBoard:
            generatedData.append(mons.monsterCurrAttack)
            generatedData.append(mons.monsterCurrHP)
            generatedData.append(mons.canAttack)
        # we need to generate 0's for the rest of P2 board side
        for _ in range(5 - len(enemyBoard)):
            generatedData.append(0)
            generatedData.append(0)
            generatedData.append(0)

        # TODO: need a more generalizable method to do this
        numGobs = 0
        numFighters = 0
        for item in hand:
            if item.name == "Fighter":
                numFighters += 1
            else:
                numGobs += 1
        generatedData.append(numGobs)
        generatedData.append(numFighters)

        generatedData.append(currPlayerHP)
        generatedData.append(enemyPlayerHP)
        generatedData.append(enemyCardNum)
        generatedData.append(currPP)
        generatedData.append(maxPP)
            
        return generatedData

    def NNtoGame(self, NNoutput, hand):
        # NOTE: Right now all NN outputs are normalized to [0,1], so we need to find the associated value for thing like
        #       card to play
        if NNoutput[0] == 1:
            cardIndex = -1
            currIndex = 0
            for item in hand:
                if item.name == self.mapping[NNoutput[1]]:
                    cardIndex = currIndex
                    return [1, currIndex]
            # If we reached here the AI requested an illegal action, so just send it as one
            return [1, -1]
        else:
            return NNoutput

# testing
