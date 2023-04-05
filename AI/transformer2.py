# The transformer is a liason between the NN and the Game class
# it takes the output of the NN and interprets it for the Game,
# and takes the game state and condenses it into a digestible form
# for the NN

# This is where a lot of the modification is going to have to be between matchups

#TODO, get this from constants file
MAX_HAND_SIZE = 9
MAX_BOARD_SIZE = 5

import torch

def int_to_bits(x, bits=None, dtype=torch.int8):
    assert not(x.is_floating_point() or x.is_complex()), "x isn't an integer type"
    if bits is None: bits = x.element_size()
    mask = 2**torch.arange(bits-1,-1,-1).to(x.device, x.dtype)
    return x.unsqueeze(-1).bitwise_and(mask).ne(0).to(dtype=dtype)

a = torch.tensor([[20,20,8,8],[3,4,8,3],[16,pow(2,4)+3,0,0]])
print(int_to_bits(a, bits=5, dtype=torch.float))

class Transformer:
    def __init__(self):
        return

    # Current stack, see input.txt for details
    
    # TODO: change this to take in a Game
    # From the game state, create an input to the NN
    def gameDataToNN(self, allyBoard, enemyBoard, currPlayer, enemyPlayer):
        generatedData = []

        # Layer 1, basic data
        currLayer = []
        currLayer.append(currPlayer.currHP)
        currLayer.append(enemyPlayer.currHP)
        currLayer.append(currPlayer.currPP)
        currLayer.append(currPlayer.maxPP)
        currLayer.append(0) #turn number, implement later
        currLayer.append(currPlayer.canEvolve)
        generatedData.append(currLayer)

        # Layer 2, basic data
        currLayer = []
        currLayer.append(enemyPlayer.maxPP)
        currLayer.append(len(enemyPlayer.hand))
        currLayer.append(currPlayer.currEvos)
        currLayer.append(enemyPlayer.currEvos)
        currLayer.append(0)
        currLayer.append(0)
        generatedData.append(currLayer)
        
        # Layers 3-11, hand contents
        for loopIndex in range(MAX_HAND_SIZE):
            currLayer = [0,0,0,0,0,0]
            if loopIndex < len(currPlayer.hand):
                currLayer[0] = pow(2, currPlayer.hand[loopIndex].encoding)
            generatedData.append(currLayer)

        # Layers 12-22, board contents
        for loopIndex in range(MAX_BOARD_SIZE):
            currLayer = [0,0,0,0,0,0]
            if loopIndex < len(allyBoard):
                currMon = allyBoard[loopIndex]
                currLayer[0] = pow(2, currMon.encoding)
                currLayer[1] = currMon.monsterCurrAttack
                currLayer[2] = currMon.monsterCurrHP
                currLayer[3] = 8*currMon.canAttackFace + 4*currMon.isEvolved + 2*currMon.hasWard + currMon.canAttack
            generatedData.append(currLayer)
        
        for loopIndex in range(MAX_BOARD_SIZE):
            currLayer = [0,0,0,0,0,0]
            if loopIndex < len(enemyBoard):
                currMon = enemyBoard[loopIndex]
                currLayer[0] = pow(2, currMon.encoding)
                currLayer[1] = currMon.monsterCurrAttack
                currLayer[2] = currMon.monsterCurrHP
                currLayer[3] = 8*currMon.canAttackFace + 4*currMon.isEvolved + 2*currMon.hasWard + currMon.canAttack
            generatedData.append(currLayer)
        
        if currPlayer.playerNum == 1:
            currLayer = [32,32,32,32,32,32]
        else:
            currLayer = [0,0,0,0,0,0]
        generatedData.append(currLayer)
        
        return generatedData
        #return int_to_bits(torch.tensor(generatedData), bits=6)

    def NNtoGame(self, NNoutput, hand):
        # NOTE: Right now all NN outputs are normalized to [0,1], so we need to find the associated value for thing like
        #       card to play
        if NNoutput[0] == 1:
            currIndex = 0
            for item in hand:
                if item.name == self.mapping[NNoutput[1]]:
                    return [1, currIndex]
                currIndex += 1
            # If we reached here the AI requested an illegal action, so just send it as one
            return [1, -5]
        else:
            return NNoutput

