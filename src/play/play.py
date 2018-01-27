from libs import json_reader
import src.GAME as GAME
import math.random


#TODO validate ecessity of 'stance' attribute
def roll(callout, stance): # eg roll('Line Plunge', 'offense')
    stats = json_reader.read(GAME.team, attribute=stance)
    roll = math.random()
    result = stats[callout][GAME.weightedRoll(callout, stance, roll)]
    return result
    #host = conn.socket.validateResolveHost TODO: this goes to dispatcher


def processPlay(rolls):
	finalType = determinePriority(rolls['Defense'], rolls['Offense'])

	if finalType:
		GAME.playmap[_rolltype(finalType)]()#call resolve
	else:
		soft(rolls)

def determinePriority(defRoll, attRoll):
	defType = _rolltype(defRoll)
	if defType not in GAME.simplePriorityLow:
		return defRoll
	elif attRoll not in GAME.simplePriorityLow:
		return attRoll
	else
		return None

def _rolltype(roll):
	return roll.split(" ")[0]