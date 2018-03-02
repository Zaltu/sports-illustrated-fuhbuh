import random
import sys as system
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
        print "Changing quarters"
        changeQuarters()
    GAME.boob = False

def changeQuarters():
    GAME.clock[0] = src.QNAMES[src.QNAMES.index(GAME.clock[0])+1]
    if GAME.clock[0] == 'END':
        gameOver()
    GAME.clock[1] = 720


def gameOver():
    print "Game over"
    print "Final score: %s to %s" % (GAME.score[0], GAME.score[1])
    GAME.end = True


def handleFluff():
    if GAME.firstdown >= 100:
        print "%sth and goal on the %s" % (GAME.down, GAME.yard)
    else:
        print "%sth and %s on the %s" % (GAME.down, GAME.firstdown-GAME.yard, GAME.yard)

    print "Game time: %s" % GAME.clock


def handleTD():
    if GAME.yard >= 100:
        print "TOUCHDOWN!"
        handleScore()
        GAME.TD = True


def handleScore():
    if GAME.localstance == "Offense":
        GAME.score[0] += 7
    else:
        GAME.score[1] += 7


def handleDowns():
    if GAME.yard >= 100:  # TD
        return
    if GAME.yard >= GAME.firstdown:
        print "First Down!"
        GAME.down = 1
        GAME.firstdown = GAME.yard + 10
    else:
        downChange()
    if GAME.down == 5:
        turnOver()


def fullTurn():
    handleFluff()
    play.roll(GAME.callout, offensePlay=GAME.into if GAME.localstance == "Defense" else None)
    play.processPlay()
    print GAME.rolls
    handleDowns()
    handleTD()
    clock(GAME.boob)


def kickoff():
    GAME.TD = False
    GAME.yard = 40
    play.customKey('Kickoff', 'Kickoff')
    GAME.toggleStance()
    play.customKey('Kickoff Return', 'Kickoff Return')
    GAME.firstdown = GAME.yard + 10
    handleFluff()
