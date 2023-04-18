import sys
sys.path.insert(0, './cardArchive/')


import pickle
from deck import Deck
from cardsSimple import *
from wrathCards import *

deck1 = [[Goblin, 3],
         [RagingCommander, 3],
         [Garodeth, 3],
         [Drummer, 3],
         [Vampy, 3],
         [HowlingDemon, 3],
         [Veight, 3]]

with open("deck2.deck", "wb") as f:
    pickle.dump(deck1, f)
