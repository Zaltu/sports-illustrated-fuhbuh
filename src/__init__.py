from libs.namespace import Namespace
from libs import json_reader
from gui.sub.coinflip import CoinFlip
from gui.sub.stateerror import StateError


STANCES = ['Offense', 'Defense', 'Kick']
QNAMES = ['1st', '2nd', '3rd', '4th', 'END']
GAME = Namespace()

def validateState():
    try:
        assert GAME.team
        assert GAME.enemy
        assert GAME.state
        assert GAME.turn
        assert GAME.clock
        assert GAME.score
        assert GAME.conn
        assert GAME.localstance
        assert GAME.down
    except (AssertionError, AttributeError):
        GAME.state = StateError
        return 0
    return 1


"""
A = [
        (10,    ),
        (20,    ),
        (30,    ),
        (40,    ),
        ...
    ]
"""
def weightedRoll(stance, perc):
    numProbTable = json_reader.readJson("data/dice.json")
    for sheetRoll in numProbTable[stance]:
        if numProbTable[stance][numProbTable[stance].index(sheetRoll)+1] > perc:
            print (sheetRoll, numProbTable[stance].index(sheetRoll))
            return numProbTable[stance].index(sheetRoll)


def setTeam(team):
    GAME.team = team


def setEnemy(team):
    GAME.enemy = team


def setState(state):
    GAME.state = state


def switchYardSide():
    GAME.yard = 100 - GAME.yard


def toggleStance():
    if GAME.localstance == "Offense" or GAME.localstance == "Kick":
        GAME.localstance = "Defense"
    else:
        GAME.localstance = "Offense"
    GAME.switchYardSide()
    GAME.down = 1


GAME.clock = ['1st', 720]
GAME.simplePriorityLow = ['+', '-']
GAME.score = (0, 0) # (Me, Them)
GAME.state = CoinFlip # QWidget object
GAME.conn = None # IP address or connection object for the second player
GAME.localstance = ''
GAME.yard = 40
GAME.boob = False

GAME.setTeam = setTeam
GAME.setEnemy = setEnemy
GAME.setState = setState
GAME.weightedRoll = weightedRoll
GAME.switchYardSide = switchYardSide
GAME.toggleStance = toggleStance
GAME.validateState = validateState
