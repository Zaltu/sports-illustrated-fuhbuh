from gui.liaison import notify
import src
from src import GAME
from src.play import play

def graphicDispatch():
    notify()

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
    GAME.boob = False

def changeQuarters():
    GAME.clock[0] = src.QNAMES[src.QNAMES.index(GAME.clock[0])+1]
    if GAME.clock[0] == 'END':
        gameOver()


def gameOver():
    pass


def fullTurn():
    play.processPlay()
    downChange()
    if GAME.down == 5:
        turnOver()
    clock(GAME.boob)
