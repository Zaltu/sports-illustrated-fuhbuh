from gui.liaison import notify
import src
from src import GAME

def graphicDispatch(play):
    playToGame(play)
    notify()


def playToGame(play):
    GAME.play = play


def downChange():
    GAME.down += 1


def turnOver():
    GAME.down = 1
    GAME.switchYardSide()
    GAME.toggleStance()


def clock(star):
    GAME.clock[1] -= 30 if not star else 10
    if GAME.clock[1] <= 0:
        changeQuarters()

def changeQuarters():
    GAME.clock[0] = src.QNAMES[src.QNAMES.index(GAME.clock[0])+1]
    if GAME.clock[0] == 'END':
        gameOver()


def gameOver():
    pass
