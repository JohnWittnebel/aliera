from game

class MCTS():
    def __init__(self):
        x=1

    def runToCompletion(self, game):
        while (game.winner == 0):
            moves = game.generateLegalMoves()


