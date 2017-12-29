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
    prioStance = determinePriority()
    if prioStance != '+':
        GAME.playmap[_rolltype(GAME.rolls[prioStance])](prioStance)
    else:
        GAME.playmap[prioStance]()


def determinePriority():
    defType = _rolltype(GAME.rolls['Defense'])
    attType = _rolltype(GAME.rolls['Attack'])
    if defType not in GAME.simplePriorityLow:
        return 'Defense'
    elif attType not in GAME.simplePriorityLow:
        return 'Attack'
    else:
        return '+'


def _rolltype(rollRes):
    return rollRes.split(" ")[0]
