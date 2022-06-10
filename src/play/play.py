"""
Module containing all necessary logic to process the plays made by each team.
"""
import random
from libs import json_reader
from src import GAME


FUMBLE_CHANCE_FIELD = "FUMBLE_CHANCE"


def roll(callout, stance, offensePlay=None):
    """
    Roll the dice on the callout requested, at the stance requested.
    Callouts are only valid on a single stance, mind you.
    Defensive callouts require the offensive callout to calculate.
    Roll results are stored in the GAME.rolls[stance] state.
    eg roll('Line Plunge', 'Offense')

    :param str callout: the player-made callout
    :param str stance: the stance of the callout (Offense or Defense)
    :param str offensePlay: the offense callout, if attempting to roll a defense callout. Default None.
    """
    stats = json_reader.readJson(GAME.team, attribute=stance)
    numRoll = random.random()*100
    if stance == "Offense":
        GAME.rolls[stance] = stats[callout][GAME.weightedRoll(stance, numRoll)]
    else:
        GAME.rolls[stance] = stats[callout][offensePlay][GAME.weightedRoll(stance, numRoll)]

def processPlay():
    """
    Butt heads of both rolls, and determine the outcome of the turn as a whole.
    """
    finalStance = determinePriority()
    if finalStance:
        PLAYMAP[_rolltype(GAME.rolls[finalStance])](GAME.rolls[finalStance])#call resolve
        GAME.boob = GAME.rolls[finalStance].split(" ")[-1] == "*" or GAME.boob
    else:
        soft()


def determinePriority():
    """
    Determines which stance's play has priority, depending on the values rolled.
    If both rolls should be kept for processing, returns None.

    :returns: priority stance (Offense, Defense, None)
    :rtype: str
    """
    defType = _rolltype(GAME.rolls['Defense'])
    attType = _rolltype(GAME.rolls['Offense'])
    if defType not in GAME.simplePriorityLow:
        return 'Defense'
    elif attType not in GAME.simplePriorityLow:
        return 'Offense'
    else:
        return None


def _rolltype(rollRes, position=0):
    """
    Helper function to split just the roll type or the value out of the full roll value received from the
    JSON.

    :param str rollRes: Roll result. The full play of one team.
    :param int position: position in the roll result. Hard-coded arbitrary stuff. Default: roll type

    :returns: whichever part of the play was requested (default: roll type)
    :rtype: str
    """
    return rollRes.split(" ")[position]



#These represent all the different play types that can occur and their resolves.
def soft():
    """
    Pure yardage gain or loss. Lowest priority, and only roll type which uses both rolls, if both are soft.
    """
    mod1 = (''.join(GAME.rolls["Defense"].split(" ")[:2]))
    mod2 = (''.join(GAME.rolls["Offense"].split(" ")[:2]))
    if mod2 == "+TD" or mod1 == "+TD":
        GAME.yard = 100
        GAME.TD = True
    else:
        GAME.yard += (int)(mod1)+(int)(mod2)
    if _rolltype(GAME.rolls['Offense'], position=-1) == "*"\
       or _rolltype(GAME.rolls['Defense'], position=-1) == "*":
        GAME.boob = True


def softs(singlePlay):
    """
    Pure yardage gain or loss, same as above, but for when only one stance is relevant to the calculation.

    :param str singlePlay: the full single play to process.
    """
    mod = (''.join(singlePlay.split(" ")[:2]))
    if mod == "+TD":
        GAME.yard = 100
        GAME.TD = True
    else:
        GAME.yard += (int)(mod)
    if singlePlay[-1] == "*":
        GAME.boob = True


def hard(result):
    """
    Hard plays override soft plays, but not much else.

    :param str result: the full single play to process.
    """
    mod = result.split(" ")[1]
    if mod == "+TD":
        GAME.yard = 100
        return
    GAME.yard += (int)(mod)


def incomplete(_):
    """
    Incomplete pass. Nothing changes.
    *Incomplete is always considered oob for clock purposes.

    :param str _: unused play. Incomplete always behaves the same.
    """
    GAME.boob = True


def interception(result):
    """
    Ball travels a certain distance, then the stances are reversed.

    :param str result: the full single play to process.
    """
    GAME.yard += (int)(result.split(" ")[1])
    GAME.toggleStance()
    GAME.down = 1


def fumble(result):
    """
    Ball travels a certain distance and gets dropped. There is a fixed chance of recovery.
    If fumble is not recovered, toggle stance.

    :param str result: the full single play to process.
    """
    if GAME.localstance == "Offense":
        fum = json_reader.readJson(GAME.team, attribute=FUMBLE_CHANCE_FIELD)
    else:
        fum = json_reader.readJson(GAME.enemy, attribute=FUMBLE_CHANCE_FIELD)
    GAME.yard += (int)(result.split(" ")[1])
    recroll = random.random()*100
    if recroll <= fum:
        GAME.build_state("Fumble recovered!")
        return
    GAME.toggleStance()
    GAME.down = 1
    GAME.build_state("Fumble lost!")


def penalty(result, gain):
    """
    Penalties change the yardage by a strict amount, but do not change the down, unless a first down is
    reached.

    :param str result: the full single play to process.
    :param bool gain: if the penalty is a yardage gain or loss for the offensive team
    """
    if not gain:
        GAME.yard -= (int)(result.split(" ")[1])
    else:
        GAME.yard += (int)(result.split(" ")[1])
    # No down change on penalties
    GAME.down -= 1
    # Penalties are always considered oob
    GAME.boob = True


def customKey(ctype, key):
    """
    Fuhbuh cards have certain extra tables, all with the same number of rolls possible. This function rolls
    onto the table and processes the result immediately.
    Used for:
        Kickoff
        Kickoff Return
        Offside Kickoff
        Punt
        Punt Return
        Field Goal Kick
        QT
        Breakaway
    :param str ctype: which type of roll to perform (eg "Kickoff")
    :param str key: the same thing apparently, I forget why they're different
    """
    GAME.build_state(ctype + "!")
    if GAME.localstance == 'Offense':
        line = json_reader.readJson(GAME.team, attribute=key)
    else:
        line = json_reader.readJson(GAME.enemy, attribute=key)
    print(line)
    newRoll = GAME.weightedRoll('Offense', random.random()*100)
    newPlay = line[newRoll]
    GAME.build_state(ctype + " roll: %s" % newPlay)
    PLAYMAP[_rolltype(newPlay)](newPlay)


PLAYMAP = {
    '+': softs,
    '-': softs,
    ':': hard,
    'OFF': lambda r: penalty(r, False),
    'DEF': lambda r: penalty(r, True),
    'PI': lambda r: penalty(r, True),
    'INC': incomplete,
    'QT': lambda r: customKey("QT", "QT"),
    'INT': interception,
    'F': fumble,
    'BK': fumble,
    'B': lambda r: customKey("Breakaway", "Breakaway")
}
