import random
from pprint import pprint as pp
from libs import json_reader
from src import GAME




def roll(callout, offensePlay=None): # eg roll('Line Plunge')
    stats = json_reader.readJson("data/teams/"+GAME.team, attribute=GAME.localstance)
    numRoll = random.random()*100
    if not offensePlay:
        GAME.rolls[GAME.localstance] = stats[callout][GAME.weightedRoll(GAME.localstance, numRoll)]
    else:
        GAME.rolls[GAME.localstance] = stats[callout][offensePlay][GAME.weightedRoll(GAME.localstance, numRoll)]

def processPlay():
    finalStance = determinePriority()
    if finalStance:
        PLAYMAP[_rolltype(GAME.rolls[finalStance])](GAME.rolls[finalStance])#call resolve
        GAME.boob = GAME.rolls[finalStance].split(" ")[-1] == "*" or GAME.boob
    else:
        soft()


def determinePriority():
    defType = _rolltype(GAME.rolls['Defense'])
    attType = _rolltype(GAME.rolls['Offense'])
    if defType not in GAME.simplePriorityLow:
        return 'Defense'
    elif attType not in GAME.simplePriorityLow:
        return 'Offense'
    else:
        return None
    # TODO Resolve down
    # TODO Resolve clock


def _rolltype(rollRes, position=0):
    return rollRes.split(" ")[position]


"""
These represent all the different play types that can occur and their resolves.
"""
def soft():
    mod1 = (int)(''.join(GAME.rolls["Defense"].split(" ")[:2]))
    mod2 = (int)(''.join(GAME.rolls["Offense"].split(" ")[:2]))
    if mod2 == 100:
        # Soft TD
        pass
    GAME.yard += mod1+mod2
    if _rolltype(GAME.rolls['Offense'], position=-1) == "*" or _rolltype(GAME.rolls['Defense'], position=-1) == "*":
        GAME.boob = True


def hard(gain, result):
    mod = (int)(result.split(" ")[1])
    if mod == 100:
        # Force TD
        pass
    if gain:
        GAME.yard += mod
    else:
        GAME.yard -= mod


def incomplete(result):
    pass


def interception(result):
    GAME.yard += (int)(result.split(" ")[1])
    GAME.toggleStance()


def fumble(gain, result):
    if gain:
        GAME.yard += (int)(result.split(" ")[1])
    else:
        GAME.yard -= (int)(result.split(" ")[1])
    GAME.toggleStance()
    GAME.down = 1


def qtrouble(result):
    pass


def penalty(result, towards):
    if GAME.localstance == towards:
        GAME.yard -= (int)(result.split(" ")[1])
    else:
        GAME.yard += (int)(result.split(" ")[1])
    # No down change on penalties
    GAME.down -= 1
    # Penalties are always considered oob
    GAME.boob = True


PLAYMAP = {
    '+': soft,
    '-': soft,
    ':+': lambda s: hard(True, s),
    ':-': lambda s: hard(False, s),
    'OFF': lambda s, t='Offense': penalty(s, towards=t),
    'DEF': lambda s, t='Defense': penalty(s, towards=t),
    'PI': lambda s, t='Defense': penalty(s, towards=t),
    'INC': incomplete,
    ':+TD': lambda s: hard(True, s),
    'QT': qtrouble,
    'INT': interception,
    'F+': lambda s: fumble(True, s),
    'F-': lambda s: fumble(False, s),
    'BK-': fumble
}
