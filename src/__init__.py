"""
The GAME state. Who knows why I thought organizing it like this would be a good idea.
"""
from libs.namespace import Namespace
from libs import json_reader

STANCES = ['Offense', 'Defense', 'Kick']
QNAMES = ['1st', '2nd', '3rd', '4th', 'END']
GAME = Namespace()

def validateState():
    """
    *Why isn't this just a bool?
    Validate that the state of the GAME contains what we need in order to start playing.
    :returns: 1 for yes, 0 for no
    :rtype: int
    """
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
        assert not GAME.TD
    except (AssertionError, AttributeError):
        GAME.state = "Error"
        return 0
    return 1


def weightedRoll(stance, perc):
    """
    Roll the dice, based on the probability weight table found in dice.json
    JSON structur resembles:
        A = [
                (10,    ),
                (20,    ),
                (30,    ),
                (40,    ),
                ...
        ]
    :param str stance: stance being rolled
    :param int perc: 1d100 rolled
    :returns: the dice number rolled, per fuhbuh rules
    :rtype: int
    """
    numProbTable = json_reader.readJson("dice")
    for sheetRoll in numProbTable[stance]:
        if numProbTable[stance][numProbTable[stance].index(sheetRoll)+1] > perc:
            #print (sheetRoll, numProbTable[stance].index(sheetRoll))
            return numProbTable[stance].index(sheetRoll)

#pylint: disable=missing-function-docstring
# Setters
def setTeam(team):
    GAME.team = team


def setEnemy(team):
    GAME.enemy = team


def setState(state):
    GAME.state = state


def switchYardSide():
    GAME.yard = 100 - GAME.yard
#pylint: enable=missing-function-docstring

def toggleStance():
    """
    Toggles the localstance value, and everything that entails (switching the yards and setting the downs).
    """
    if GAME.localstance == "Offense" or GAME.localstance == "Kick":
        GAME.localstance = "Defense"
    else:
        GAME.localstance = "Offense"
    GAME.switchYardSide()
    GAME.down = 1
    GAME.firstdown = GAME.yard+10


GAME.clock = ['1st', 720]
GAME.simplePriorityLow = ['+', '-']
GAME.score = [0, 0] # (Me, Them)
GAME.state = "CoinFlip" # QWidget object
GAME.conn = None # IP address or connection object for the second player
GAME.localstance = ''
GAME.yard = 40
GAME.boob = False
GAME.TD = False
GAME.offplay = None
GAME.defplay = None
GAME.team = None
GAME.enemy = None

GAME.setTeam = setTeam
GAME.setEnemy = setEnemy
GAME.setState = setState
GAME.weightedRoll = weightedRoll
GAME.switchYardSide = switchYardSide
GAME.toggleStance = toggleStance
GAME.validateState = validateState

GAME.printables = []