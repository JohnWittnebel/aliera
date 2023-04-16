import random
import copy
import sys
import pickle
sys.path.insert(0, './cardArchive/')
from cardsSimple import *

class Deck:
    def __init__(self, deckname):
        self.deckName = deckname
        self.cards = []
        self.deckFromFile()

    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
     
            # Pick a random index from 0 to i
            j = random.randint(0, i)
   
            # Swap arr[i] with the element at random index
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    # This actually draws from the end of the deck, important to note
    def draw(self):
        if len(self.cards) > 0:
            cardDrawn = self.cards.pop()
            return cardDrawn
        else:
            return Reaper()

    # This is pretty dumb, but will work for now
    def __str__(self):
        for item in self.cards:
            print(item)
        return ""
    
    # For when the deck needs to be reset in between games
    # This is deprecated and no longer used probably, delete soon
    def refresh(self):
        self.deckFromFile()

    def deckFromFile(self):
        self.cards = []
        deck_file = open("./" + self.deckName + ".deck", "rb")
        deckData = pickle.load(deck_file)
        deck_file.close()

        for ele in deckData:
            for _ in range(ele[1]):
                self.cards.append(ele[0]())
        self.shuffle()

