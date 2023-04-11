# The transformer is a liason between the NN and the Game class
# it takes the output of the NN and interprets it for the Game,
# and takes the game state and condenses it into a digestible form
# for the NN

# This is where a lot of the modification is going to have to be between matchups

#TODO, get this from constants file
MAX_HAND_SIZE = 9
MAX_BOARD_SIZE = 5

import torch
from torch.masked import masked_tensor
from torch import nn
import numpy as np
from allmoves import ALLMOVES

def int_to_bits(x, bits=None, dtype=torch.int8):
    assert not(x.is_floating_point() or x.is_complex()), "x isn't an integer type"
    if bits is None: bits = x.element_size()
    mask = 2**torch.arange(bits-1,-1,-1).to(x.device, x.dtype)
    return x.unsqueeze(-1).bitwise_and(mask).ne(0).to(dtype=dtype)

#a = torch.tensor([[20,20,8,8],[3,4,8,3],[16,pow(2,4)+3,0,0]])
#print(int_to_bits(a, bits=5, dtype=torch.float))

class Transformer:
    def __init__(self):
        return

    # Current stack, see input.txt for details
    
    # From the game state, create an input to the NN
    def gameDataToNN(self, gameState):

        # TODO: maybe make this less bad
        if (gameState.activePlayer.playerNum == 1):
            currPlayer = gameState.player1
            enemyPlayer = gameState.player2
            allyBoard = gameState.board.fullBoard[0]
            enemyBoard = gameState.board.fullBoard[1]
        else:
            currPlayer = gameState.player2
            enemyPlayer = gameState.player1
            allyBoard = gameState.board.fullBoard[1]
            enemyBoard = gameState.board.fullBoard[0]

        generatedData = []

        # Layer 1, basic data
        currLayer = []
        currLayer.append(currPlayer.currHP)
        currLayer.append(enemyPlayer.currHP)
        currLayer.append(currPlayer.currPP)
        currLayer.append(currPlayer.maxPP)
        #currLayer.append(0) #turn number, implement later
        currLayer.append(currPlayer.canEvolve)
        generatedData.append(currLayer)

        # Layer 2, basic data
        currLayer = []
        currLayer.append(enemyPlayer.maxPP)
        currLayer.append(len(enemyPlayer.hand))
        currLayer.append(currPlayer.currEvos)
        currLayer.append(enemyPlayer.currEvos)
        #currLayer.append(0)
        currLayer.append(0)
        generatedData.append(currLayer)
        
        # Layers 3-11, hand contents
        for loopIndex in range(MAX_HAND_SIZE):
            currLayer = [0,0,0,0,0]
            if loopIndex < len(currPlayer.hand):
                currLayer[0] = pow(2, currPlayer.hand[loopIndex].encoding)
            generatedData.append(currLayer)

        # Layers 12-22, board contents
        for loopIndex in range(MAX_BOARD_SIZE):
            currLayer = [0,0,0,0,0]
            if loopIndex < len(allyBoard):
                currMon = allyBoard[loopIndex]
                currLayer[0] = pow(2, currMon.encoding)
                currLayer[1] = currMon.monsterCurrAttack
                currLayer[2] = currMon.monsterCurrHP
                currLayer[3] = 8*currMon.canAttackFace + 4*currMon.isEvolved + 2*currMon.hasWard + currMon.canAttack
            generatedData.append(currLayer)
        
        for loopIndex in range(MAX_BOARD_SIZE):
            currLayer = [0,0,0,0,0]
            if loopIndex < len(enemyBoard):
                currMon = enemyBoard[loopIndex]
                currLayer[0] = pow(2, currMon.encoding)
                currLayer[1] = currMon.monsterCurrAttack
                currLayer[2] = currMon.monsterCurrHP
                currLayer[3] = 8*currMon.canAttackFace + 4*currMon.isEvolved + 2*currMon.hasWard + currMon.canAttack
            generatedData.append(currLayer)

        # Layer 23, player turn
        if currPlayer.playerNum == 1:
            currLayer = [63,63,63,63,63]
        else:
            currLayer = [0,0,0,0,0]
        generatedData.append(currLayer)
       
        #return generatedData
        return int_to_bits(torch.tensor(generatedData), bits=6, dtype=torch.float32)

    # The NN output is defined by 46 outputs, 45 being move probabilities and the last being the valuation.
    # first 9: play associated card
    # then next 30: attack
    # then next 30: evolve
    # then last 1: pass
    # We need to determine which moves are legal, and normalize the probabilities of the legal moves
    # Plan: get the game to generate all legal moves, create a binary tensor representing legal/illegal, element-wise product
    #       with NNoutput tensor, then normalize
    def normalizedVector(self, NNoutput, gameState):
        legalBinaryMask = torch.zeros(70, dtype=bool)
        legalMoves = gameState.generateLegalMoves()
        for move in legalMoves:
            if move[0] == 4:
                legalBinaryMask[69] = 1
            elif move[0] == 1:
                legalBinaryMask[move[1][0]] = 1
            elif move[0] == 2:
                legalBinaryMask[10 + 6*move[1][0] + move[1][1]] = 1
            elif move[0] == 3:
                if (len(move[1]) == 1):                    
                    legalBinaryMask[39 + 6*move[1][0]] = 1
                else:
                    legalBinaryMask[39 + 6*move[1][0] + move[1][1] + 1] = 1

        legalMasked = masked_tensor(NNoutput, legalBinaryMask)
        legalMoveProbs = nn.Softmax(dim=0)(legalMasked)
        #print(legalMoveProbs)
        #binaryTensor = torch.Tensor(legalBinaryArray)
        #legalMoveProbs = legalBinaryArray * NNoutput
        
        #totalWeight = 0
        #for ele in legalMoveProbs:
        #    totalWeight += ele
        #for ind in range(len(legalMoveProbs)):
        #    legalMoveProbs[ind] /= totalWeight
        return legalMoveProbs, legalBinaryMask

