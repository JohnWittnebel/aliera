import pickle
from deck import Deck


def newDeckPool():
    for i in range(120):
        seedVal = i*12389 % 55554
        with open("./constantDecks/P1deck" + str(i) + ".seed", "wb") as f:
            pickle.dump(seedVal, f)

    for i in range(120):
        seedVal = i*14321 % 55554
        with open("./constantDecks/P2deck" + str(i) + ".seed", "wb") as f:
            pickle.dump(seedVal, f)
