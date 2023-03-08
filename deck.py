import random

class Deck:
  def __init__(self, cards):
    self.cards = cards

  def shuffle(self):
    for i in range(len(self.cards)-1, 0, -1):
     
      # Pick a random index from 0 to i
      j = random.randint(0, i)
   
      # Swap arr[i] with the element at random index
      self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

  # This actually draws from the end of the deck, important to note
  def draw(self):
    cardDrawn = self.cards.pop()
    return cardDrawn

  # This is pretty dumb, but will work for now
  def __str__(self):
    for item in self.cards:
        print(item)
    return ""
