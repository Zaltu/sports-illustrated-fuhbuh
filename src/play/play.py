import random
from libs import json_reader
from src import GAME




def roll(callout): # eg roll('Line Plunge')
    stats = json_reader.read(GAME.team, attribute=GAME.localstance)
    numRoll = random.randint(1, 100)
    result = stats[callout][GAME.weightedRoll(GAME.localstance, numRoll)]
    return result
    #host = conn.socket.validateResolveHost TODO: this goes to dispatcher


def processPlay():
    finalType = determinePriority()
    if finalType:
        PLAYMAP[_rolltype(GAME.rolls[finalType])](finalType)#call resolve
    else:
        soft()


def determinePriority():
    defType = _rolltype(GAME.rolls['Defense'])
    attType = _rolltype(GAME.rolls['Attack'])
    if defType not in GAME.simplePriorityLow:
        return 'Defense'
    elif attType not in GAME.simplePriorityLow:
        return 'Attack'
    else:
        return None
    # TODO Resolve down
    # TODO Resolve clock


def _rolltype(rollRes):
    return rollRes.split(" ")[0]


"""
These represent all the different play types that can occur and their resolves.
"""
def soft():
    mod1 = (int)(''.join(GAME.rolls["Defense"].split(" ")[:2]))
    mod2 = (int)(''.join(GAME.rolls["Attack"].split(" ")[:2]))
    if mod2 == 100:
        # Soft TD
        pass
    GAME.yard += mod1+mod2
    print mod1
    print mod2
    print GAME.yard


def hard(gain, fromStance):
    mod = (int)(GAME.rolls[fromStance].split(" ")[1])
    if mod == 100:
        # Force TD
        pass
    if gain:
        GAME.yard += mod
    else:
        GAME.yard -= mod
    print mod
    print GAME.yard


def incomplete(fromStance):
    pass


def interception(fromStance):
    GAME.yard += (int)(GAME.rolls[fromStance].split(" ")[1])
    GAME.toggleStance()


def fumble(fromStance):
    GAME.yard += (int)(GAME.rolls[fromStance].split(" ")[1])
    GAME.toggleStance()


def qtrouble(fromStance):
    pass


def penalty(towards):
    pass


PLAYMAP = {
    '+': soft,
    '-': soft,
    ':+': lambda s: hard(True, s),
    ':-': lambda s: hard(False, s),
    'OP': lambda t='OP': penalty(towards=t),
    'DF': lambda t='DF': penalty(towards=t),
    'PI': lambda t='PI': penalty(towards=t),
    '0': incomplete,
    ':+TD': lambda s: hard(True, s),
    'QT': qtrouble,
    'INT': interception,
    'F+': fumble,
    'F-': fumble,
    'BK-': fumble
}
