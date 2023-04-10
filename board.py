from constants import MAX_BOARD_SIZE

# A Board has 2 sides, one for each player
# On a side there is an ordered array of cards
# the maximum number of cards on each side is 5

class Board:
  def __init__(self):
    self.player1side = []
    self.player2side = []
    self.maxSize = MAX_BOARD_SIZE
    self.fullBoard = [self.player1side, self.player2side]

  def printBoard(self):
    playerSideString = ""
    count = 0

    # TODO: change this so that each monster/amulet has its own print function at some point
    for item in self.player2side:
      if item.canAttack:
          attackStr = "[X]"
      else:
          attackStr = "[ ]"
      playerSideString += item.name + " (" + str(item.monsterCurrAttack) + "/" + str(item.monsterCurrHP) + ") " + attackStr + " [" + str(count) + "], " 
      count += 1
    print(playerSideString)
    playerSideString = ""
    count = 0
    for item in self.player1side:
      if item.canAttack:
          attackStr = "[X]"
      else:
          attackStr = "[ ]"
      playerSideString += item.name + " (" + str(item.monsterCurrAttack) + "/" + str(item.monsterCurrHP) + ") " + attackStr + " [" + str(count) + "], "
      count += 1
    print(playerSideString)
 
  def updateFullBoard(self):
    self.fullBoard = [self.player1side, self.player2side]
