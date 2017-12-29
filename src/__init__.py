from libs.namespace import Namespace
from libs import json_reader
from src.play import play
from gui.sub.coinflip import CoinFlip
from gui.sub.stateerror import StateError


STANCES = ['Offense', 'Defense', 'Kick']
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
    except AssertionError:
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
    numProbTable = json_reader.readJSON("NumProb.json")
    for sheetRoll in numProbTable[stance]:
        if numProbTable[stance][numProbTable[stance].index(sheetRoll)+1][0] > perc:
            return sheetRoll[0]


def setTeam(team):
    GAME.team = team

def setEnemy(team):
    GAME.enemy = team

def setState(state):
    GAME.state = state

def switchYardSide():
    GAME.yard = 100 - GAME.yard

def toggleStance():
    if GAME.localstance == "Attack" or GAME.localstance == "Kick":
        GAME.localstance = "Defense"
    else:
        GAME.localstance = "Attack"
    GAME.switchYardSide()


GAME.clock = ['1st', 720]
GAME.simplePriorityLow = ['+', '-']
GAME.score = (0, 0) # (Me, Them)
GAME.state = CoinFlip # QWidget object
GAME.conn = None # IP address or connection object for the second player
GAME.localstance = ''
GAME.yard = 40

GAME.playmap = {
    '+': play.soft,
    '-': play.soft,
    ':+': play.hard,
    ':-': play.hard,
    'OP': lambda f, t='OP': play.penalty(towards=t, fromStance=f),
    'DF': lambda f, t='DF': play.penalty(towards=t, fromStance=f),
    'PI': lambda f, t='PI': play.penalty(towards=t, fromStance=f),
    '0': play.incomplete,
    ':TD': play.hard,
    'QT': play.qtrouble,
    'INT': play.intercept
}

GAME.setTeam = setTeam
GAME.setEnemy = setEnemy
GAME.setState = setState
GAME.weightedRoll = weightedRoll
GAME.switchYardSide = switchYardSide
GAME.toggleStance = toggleStance
