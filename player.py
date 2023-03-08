from deck import Deck
from constants import MAX_HAND_SIZE

# A Player has an associated deck, that is a Deck type
# A Player has a hand, and that is simply an array of Cards, we can specify a starting hand if we wish
# A Player has a PlayerNum, and that is 1 or 2 depending on if the player is first or second respectively
# A Player has a max number of Evos, this is 2 when first or 3 when second, but this can change with certain cards
# A Player has a current number of usable Evos
# A Player has leader effects, that will be used in a later version

class Player:
  def __init__(self, deck, maxEvos, currEvos, playerNum):
    self.deck = deck
    self.maxEvos = maxEvos
    self.currEvos = currEvos
    self.playerNum = playerNum
    self.hand = []
    self.effects = []

  def draw(self):
    cardToAdd = self.deck.draw()
    if (self.hand.count == MAX_HAND_SIZE):
      print("Hand size full")
    else:
      print(self.playerNum)
      print(self.hand)
      self.hand.append(cardToAdd)
