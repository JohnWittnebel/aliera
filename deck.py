import random
from cardArchive import Reaper
from cardArchive import Goblin, Fighter, Goliath, DeathDragon, Mercenary

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

  # This really is only for Fighter/Gob testing
  def refresh(self):
      self.cards = []
      for _ in range(8):
          self.cards.append(Goblin())
          self.cards.append(Fighter())
          self.cards.append(Mercenary())
          self.cards.append(Goliath())
          self.cards.append(DeathDragon())
      self.shuffle()
