import random
import sys as system
from gui.liaison import notify
import src
from src import GAME, QNAMES
from src.play import play


def graphicDispatch():
    notify()


def turnOver():
    print "Switched sides!"  # Only for CMD mode
    GAME.down = 1
    GAME.toggleStance()
    print "Offense is now on the %s yard line." % GAME.yard  # Only for CMD mode


def clock(star):
    GAME.clock[1] -= 30 if not star else 10
    if GAME.clock[1] <= 0:
        print "Changing quarters"  # Only for CMD mode
        changeQuarters()
    GAME.boob = False

def changeQuarters():
    GAME.clock[0] = src.QNAMES[src.QNAMES.index(GAME.clock[0])+1]
    if GAME.clock[0] == 'END':
        gameOver()
    GAME.clock[1] = 720
    if GAME.clock[0] == src.QNAMES[2]:
        print "Halftime!"
        if GAME.startingstance == "Offense" and GAME.localstance == "Offense":
            GAME.toggleStance()
        kickoff()


def gameOver():
    print "Game over"  # Only for CMD mode
    print "Final score: %s to %s" % (GAME.score[0], GAME.score[1])  # Only for CMD mode
    GAME.end = True


def handleFluff():
    print ""
    if GAME.firstdown >= 100:
        print "%s and goal on the %s" % (QNAMES[GAME.down-1], GAME.yard)
    else:
        print "%s and %s on the %s" % (QNAMES[GAME.down-1], GAME.firstdown-GAME.yard, GAME.yard)

    print "Game time: %s" % GAME.clock

def handleFluffCall():
    print "Offense callout: %s -> %s" % (GAME.offplay, GAME.rolls['Offense'])
    print "Defense callout: %s -> %s" % (GAME.defplay, GAME.rolls['Defense'])


def handleTD():
    if GAME.yard >= 100:
        print "TOUCHDOWN!"  # Only for CMD mode
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
        print "First Down!"  # Only for CMD mode
        GAME.down = 1
        GAME.firstdown = GAME.yard + 10
    else:
        GAME.down += 1
    if GAME.down == 5:
        turnOver()


def fullTurn():
    handleFluff()  # Only for CMD mode
    play.roll(GAME.callout, offensePlay=GAME.into if GAME.localstance == "Defense" else None)
    handleFluffCall()  # Only for CMD mode
    play.processPlay()
    handleDowns()
    handleTD()
    clock(GAME.boob)
    graphicDispatch()


def kickoff():
    print ""  # Only for CMD mode
    GAME.TD = False
    GAME.yard = 40
    play.customKey('Kickoff', 'Kickoff')
    GAME.toggleStance()
    play.customKey('Kickoff Return', 'Kickoff Return')
    GAME.firstdown = GAME.yard + 10
    GAME.down = 1


def punt():
    play.customKey('Punt', 'Punt')
    GAME.toggleStance()
    play.customKey('Punt Return', 'Punt Return')
    GAME.firstdown = GAME.yard + 10
    GAME.down = 1
    handleFluff()
