class Card:
  def __init__(self, cost, name):
    self.cost = cost
    self.name = name

  def __str__(self):
    return self.name
