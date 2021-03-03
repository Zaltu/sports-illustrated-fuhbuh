import random
from pprint import pprint as pp
from libs import json_reader
from src import GAME


FUMBLE_CHANCE_FIELD = "FUMBLE_CHANCE"


def roll(callout, stance, offensePlay=None): # eg roll('Line Plunge')
    stats = json_reader.readJson(GAME.team, attribute=stance)
    numRoll = random.random()*100
    if stance == "Offense":
        #pp(stats)
        #print callout
        #print offensePlay
        GAME.rolls[stance] = stats[callout][GAME.weightedRoll(stance, numRoll)]
    else:
        #pp(stats)
        #print callout
        #print offensePlay
        GAME.rolls[stance] = stats[callout][offensePlay][GAME.weightedRoll(stance, numRoll)]

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


def _rolltype(rollRes, position=0):
    return rollRes.split(" ")[position]


"""
These represent all the different play types that can occur and their resolves.
"""
def soft():
    mod1 = (''.join(GAME.rolls["Defense"].split(" ")[:2]))
    mod2 = (''.join(GAME.rolls["Offense"].split(" ")[:2]))
    if mod2 == "+TD" or mod1 == "+TD":
        GAME.yard = 100
        GAME.TD = True
    else:
        GAME.yard += (int)(mod1)+(int)(mod2)
    if _rolltype(GAME.rolls['Offense'], position=-1) == "*" or _rolltype(GAME.rolls['Defense'], position=-1) == "*":
        GAME.boob = True


def softs(singlePlay):
    mod = (''.join(singlePlay.split(" ")[:2]))
    if mod == "+TD":
        GAME.yard = 100
    else:
        GAME.yard += (int)(mod)
    if singlePlay[-1] == "*":
        GAME.boob = True


def hard(result):
    mod = result.split(" ")[1]
    if mod == "+TD":
        GAME.yard = 100
        return
    GAME.yard += (int)(mod)


def incomplete(result):
    # Incomplete is always considered oob
    GAME.boob = True


def interception(result):
    GAME.yard += (int)(result.split(" ")[1])
    GAME.toggleStance()


def fumble(result):
    if GAME.localstance == "Offense":
        fum = json_reader.readJson(GAME.team, attribute=FUMBLE_CHANCE_FIELD)
    else:
        fum = json_reader.readJson(GAME.enemy, attribute=FUMBLE_CHANCE_FIELD)
    GAME.yard += (int)(result.split(" ")[1])
    roll = random.random()*100
    if roll <= fum:
        print("Fumble recovered!")
        return
    print("Fumble lost!")
    GAME.toggleStance()
    GAME.down = 1


def penalty(result, gain):
    if not gain:
        GAME.yard -= (int)(result.split(" ")[1])
    else:
        GAME.yard += (int)(result.split(" ")[1])
    # No down change on penalties
    GAME.down -= 1
    # Penalties are always considered oob
    GAME.boob = True


def customKey(ctype, key):
    print(ctype + "!")
    if GAME.localstance == 'Offense':
        line = json_reader.readJson(GAME.team, attribute=key)
    else:
        line = json_reader.readJson(GAME.enemy, attribute=key)
    print(line)
    newRoll = GAME.weightedRoll('Offense', random.random()*100)
    newPlay = line[newRoll]
    print(ctype + " roll: %s" % newPlay)
    PLAYMAP[_rolltype(newPlay)](newPlay)



PLAYMAP = {
    '+': softs,
    '-': softs,
    ':': lambda r: hard(r),
    'OFF': lambda r: penalty(r, False),
    'DEF': lambda r: penalty(r, True),
    'PI': lambda r: penalty(r, True),
    'INC': incomplete,
    'QT': lambda r: customKey("QT", "QT"),
    'INT': interception,
    'F': lambda r: fumble(r),
    'BK': fumble,
    'B': lambda r: customKey("Breakaway", "Breakaway")
}
