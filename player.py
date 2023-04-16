from deck import Deck
from constants import MAX_HAND_SIZE, DEFAULT_MAX_HP, DEFAULT_MAX_PP
from leaderEffect import *

# A Player has an associated deck, that is a Deck type
# A Player has a hand, and that is simply an array of Cards, we can specify a starting hand if we wish
# A Player has a PlayerNum, and that is 1 or 2 depending on if the player is first or second respectively
# A Player has a max number of Evos, this is 2 when first or 3 when second, but this can change with certain cards
# A Player has a current number of usable Evos
# A Player has leader effects, that will be used in a later version
# A Player has a maximum and current HP
# A Player has a maximum and current PP
# A Player has a field to indicate if they are able to evolve yet

class Player:
    def __init__(self, deck, maxEvos, currEvos, playerNum):
        self.deck = deck
        self.maxEvos = maxEvos
        self.currEvos = currEvos
        self.playerNum = playerNum
        self.hand = []
        self.effects = []
        self.currHP = DEFAULT_MAX_HP
        self.maxHP = DEFAULT_MAX_HP
        self.currPP = DEFAULT_MAX_PP
        self.maxPP = DEFAULT_MAX_PP
        self.canEvolve = 0
        self.leaderEffects = LeaderEffectManager()

    def draw(self, count = 1):
        for _ in range(count):
            cardToAdd = self.deck.draw()
            # Hacky way to kill you when you draw reaper
            if (cardToAdd.name == "Reaper"):
                self.hand = []
                self.currHP = 0
                self.maxHP = 0
                self.maxPP = 0
                self.currPP = 0
            elif (len(self.hand) == MAX_HAND_SIZE):
                #print("Hand size full")
                return
            else:
                self.hand.append(cardToAdd)

    def randomHand(self):
        numCards = len(self.hand)
        for item in self.hand:
            self.deck.cards.append(item)
        self.hand = []
        self.deck.shuffle()
        self.draw(numCards)

    def printHand(self):
        count = 0
        printString = ""
        for item in self.hand:
            printString += str(item)
            printString += " [" + str(count) + "], "
            count += 1
        print(printString)

    def takeCombatDamage(self, gameState, val):
        self.currHP -= val
        if self.currHP <= 0:
            gameState.endgame((self.playerNum + 1) % 2)

    def takeEffectDamage(self, gameState, val):
        self.currHP -= val
        if self.currHP <= 0:
            gameState.endgame((self.playerNum + 1) % 2)
      
