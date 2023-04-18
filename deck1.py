import sys
sys.path.insert(0, './cardArchive/')


import pickle
from deck import Deck
from cardsSimple import *
from wrathCards import *

deck1 = [[Fighter, 3],
         [Maiden, 3],
         [Goblin, 3], 
         [Mercenary, 3],
         [DeathDragon, 3],
         [DragonBreath, 2],
         [RagingCommander, 3],
         [Veight, 3],
         [Drummer, 3],
         [Vampy, 3]]

with open("deck1.deck", "wb") as f:
    pickle.dump(deck1, f)
