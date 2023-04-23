import pickle
from deck import Deck
import time
import random
import math

def newDeckPool():
    for i in range(120):
        seedVal = random.randint(0, math.floor(time.time()))
        with open("./constantDecks/P1deck" + str(i) + ".seed", "wb") as f:
            pickle.dump(seedVal, f)
            f.close()

    for i in range(120):
        seedVal = random.randint(0, math.floor(time.time()))
        with open("./constantDecks/P2deck" + str(i) + ".seed", "wb") as f:
            pickle.dump(seedVal, f)
            f.close()
