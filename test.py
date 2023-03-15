from monster import Monster
from cardArchive import Goblin
from cardArchive import Fighter
from deck import Deck
from game import Game

def main():
  x = Game()
  x.gameStart()

  #x.board.player1side.append(Fighter())
  #x.board.player2side.append(Fighter())
  #x.board.player2side.append(Fighter())

  while (x.winner == 0): 
    x.printGameState()
    print("Input action:")
    print("1 = play card")
    print("2 = attack")
    print("4 = end turn")
    uinput1 = raw_input("")
    if (uinput1 == "1"):
      print("input card:")
      uinput2 = int(raw_input(""))
      x.initiateAction([int(uinput1),[uinput2]])
    if (uinput1 == "2"):
      print("Select attacker:")
      uinput2 = int(raw_input(""))
      print("Select defender:")
      uinput3 = int(raw_input(""))
      x.initiateAttack(uinput2, uinput3)
    if (uinput1 == "4"):
        x.endTurn()
        continue
#    x.initiateAction([uinput1,[uinput2,uinput3]])

  #x.initiateAttack(0,-1)
  #x.initiateAttack(0,0)

  #x.board.player1side.append(Goblin())
  #x.board.player2side.append(Goblin())
  #x.printGameState()
  #x.initiateAttack(0,1)
  #x.printGameState()
main()
