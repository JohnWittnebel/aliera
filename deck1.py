import sys
sys.path.insert(0, './cardArchive/')


import pickle
from deck import Deck
from cardsSimple import *
from wrathCards import *

deck1 = [[HarmonicWolf, 3],
         [Maestro, 3],
         [HowlingScream, 3],
         [Tank, 3],
         [Flautist, 3],
         [Garodeth, 3],
         [RagingCommander, 3],
         [Veight, 3],
         [Drummer, 3],
         [HowlingDemon, 3],
         [VampireQueenCastle, 3],
         [Vampy, 3]]

with open("deck1.deck", "wb") as f:
    pickle.dump(deck1, f)
