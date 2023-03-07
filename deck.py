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

  def draw(self):
    return 1

  def __str__(self):
    for item in self.cards:
        print(item.monsterName)
