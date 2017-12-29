import math.random
from libs import json_reader
import src.GAME as GAME


#TODO validate ecessity of 'stance' attribute
def roll(callout, stance): # eg roll('Line Plunge', 'offense')
    stats = json_reader.read(GAME.team, attribute=stance)
    numRoll = math.random()
    result = stats[callout][GAME.weightedRoll(callout, stance, numRoll)]
    return result
    #host = conn.socket.validateResolveHost TODO: this goes to dispatcher


def processPlay(rolls):
    finalType = determinePriority(rolls['Defense'], rolls['Offense'])


def determinePriority(defRoll, attRoll):
    defType = _rolltype(defRoll)
    if defType not in GAME.simplePriorityLow:
        return defRoll
    elif attRoll not in GAME.simplePriorityLow:
        pass

def _rolltype(rollRes):
    return rollRes.split(" ")[0]
