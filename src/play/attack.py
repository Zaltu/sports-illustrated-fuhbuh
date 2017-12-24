from libs import json_reader
import src.GAME as GAME
import math.random


#TODO validate ecessity of 'stance' attribute
def roll(callout, stance): # eg roll('Line Plunge', 'offense')
    teamstatsAttack = json_reader.read(GAME.team, attribute=stance)
    roll = math.random()
    result = teamstatsAttack[GAME.weightedRoll(callout, stance, roll)]
    return result
    #host = conn.socket.validateResolveHost TODO: this goes to dispatcher


def processPlay(stance1, stance2)
	
    pass