import random
from libs import json_reader
import src.GAME as GAME


def roll(callout): # eg roll('Line Plunge')
    stats = json_reader.read(GAME.team, attribute=GAME.localstance)
    numRoll = random.randint(1, 100)
    result = stats[callout][GAME.weightedRoll(GAME.localstance, numRoll)]
    return result
    #host = conn.socket.validateResolveHost TODO: this goes to dispatcher


def processPlay():
    finalType = determinePriority()
    
    if finalType:
        GAME.playmap[_rolltype(finalType)]()#call resolve
    else:
        soft(rolls)


def determinePriority():
    defType = _rolltype(GAME.rolls['Defense'])
    attType = _rolltype(GAME.rolls['Attack'])
    if defType not in GAME.simplePriorityLow:
        return 'Defense'
    elif attType not in GAME.simplePriorityLow:
        return 'Attack'
    else:
        return '+'
    # TODO Resolve down
    # TODO Resolve clock


def _rolltype(rollRes):
    return rollRes.split(" ")[0]


"""
These represent all the different play types that can occur and their resolves.
"""
def soft():
    mod1 = (int)(GAME.rolls["Defense"].split(" ")[1])
    mod2 = (int)(GAME.rolls["Attack"].split(" ")[1])
    if mod2 == 100:
        # Soft TD
        pass
    GAME.yard += mod1+mod2


def hard(fromStance):
    mod = (int)(GAME.rolls[fromStance].split(" ")[1])
    if mod == 100:
        # Force TD
        pass
    GAME.yard += mod


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


def penalty(towards, fromStance):
    pass
