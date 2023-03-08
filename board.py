# A Board has 2 sides, one for each player
# On a side there is an ordered array of cards
# the maximum number of cards on each side is 5

class Board:
  def __init__(self):
    self.player1side = []
    self.player2side = []
    self.maxSize = 5
