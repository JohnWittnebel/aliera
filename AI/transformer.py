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

    def gameDataToNN(self, board, hand):
        

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
