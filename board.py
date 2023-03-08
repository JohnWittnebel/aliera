from constants import MAX_BOARD_SIZE

# A Board has 2 sides, one for each player
# On a side there is an ordered array of cards
# the maximum number of cards on each side is 5

class Board:
  def __init__(self):
    self.player1side = []
    self.player2side = []
    self.maxSize = MAX_BOARD_SIZE

  def printBoard(self):
    playerSideString = ""
    count = 1
    for item in self.player2side:
      playerSideString += item.name + " (" + str(item.monsterAttack) + "/" + str(item.monsterCurrHP) + ") [" + str(count) + "], " 
      count += 1
    print(playerSideString)
    playerSideString = ""
    for item in self.player1side:
      playerSideString += item.name + " (" + str(item.monsterAttack) + "/" + str(item.monsterCurrHP) + ") [" + str(count) + "], "
      count += 1
    print(playerSideString)
