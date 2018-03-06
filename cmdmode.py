# CMD play for testing
from pprint import pprint as pp
import random
import sys
import traceback
from src import GAME
from src import turnController
from src.play import play

GAME.setTeam('raiders.json')
GAME.setEnemy('raiders.json')

GAME.turn = "dummy"
GAME.down = 1
GAME.callout = 'End Run'
GAME.into = "End Run"
GAME.rolls = {}
GAME.localstance = "Offense"
GAME.end = False
GAME.startingstance = "Offense"

GAME.validateState()

GAME.firstdown = 50

ALL_D = ["Standard", "Short Yardage", "Spread", "Pass Prevent Short", "Pass Prevent Long", "Blitz"]  # 6
ALL_A = ["Line Plunge", "Off Tackle", "End Run", "Draw", "Screen", "Short", "Medium", "Long", "Sideline"]  # 9

def fullGame():
    for i in range(0, 150):

        if GAME.localstance == "Offense":
            GAME.localstance = "Defense"
            GAME.defplay = ALL_D[random.randint(0, 5)]
            play.roll(GAME.defplay, offensePlay=GAME.into)

            GAME.callout = ALL_A[random.randint(0, 8)]
            GAME.offplay = GAME.callout
            GAME.localstance = "Offense"
            turnController.fullTurn()
        else:
            GAME.localstance = "Offense"
            GAME.offplay = ALL_A[random.randint(0, 8)]
            play.roll(GAME.offplay)

            GAME.callout = ALL_D[random.randint(0, 5)]
            GAME.defplay = GAME.callout
            GAME.localstance = "Defense"
            turnController.fullTurn()

        if GAME.TD:
            turnController.kickoff()

        if GAME.end:
            break

    print "Final yard: %s" % GAME.yard
    print "Final down: %s" % GAME.down


def heavyTest():
    errors = []
    for i in range(0, 100000):
        try:
            GAME.down = 1
            GAME.yard = 40
            GAME.firstdown = 50
            GAME.clock = ["1st", 720]
            GAME.end = False
            GAME.score = [0, 0]
            fullGame()
        except Exception as e:
            traceback.print_exc()
            sys.exit(0)
            errors.append(traceback.format_exc())

    pp(errors)


fullGame()
#heavyTest()