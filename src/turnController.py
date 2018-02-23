import random
from gui.liaison import notify
import src
from src import GAME
from src.play import play

def graphicDispatch():
    notify()

def downChange():
    GAME.down += 1


def turnOver():
    print "Switched sides!"
    GAME.down = 1
    GAME.toggleStance()
    print "Offense is now on the %s yard line." % GAME.yard


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
    print "%sth and %s on the %s" % (GAME.down, GAME.firstdown-GAME.yard, GAME.yard)
    play.roll(GAME.callout)
    play.processPlay()
    print GAME.rolls
    if GAME.yard >= GAME.firstdown:
        print "First Down!"
        GAME.down = 1
        GAME.firstdown = GAME.yard + 10
    else:
        downChange()
    if GAME.down == 5:
        turnOver()
    clock(GAME.boob)
