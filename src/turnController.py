"""
Module storing all functionality revolving around managing a single turn in a game of fuhbuh.
"""
from src import GAME, QNAMES
from src.play import play

def turnOver():
    """
    Turn the ball over to the team currently on defense.
    """
    GAME.build_state("Switched sides!")
    GAME.down = 1
    GAME.toggleStance()
    GAME.build_state("Offense is now on the %s yard line." % GAME.yard)


def clock(star):
    """
    Adjust the clock by one play (30 seconds). If the ball is out of bounds, a play lasts 10 seconds instead
    of 30.

    :param bool star: ball out of bounds
    """
    GAME.clock[1] -= 30 if not star else 10
    if GAME.clock[1] <= 0:
        GAME.build_state("Changing quarters")
        changeQuarters()
    GAME.boob = False

def changeQuarters():
    """
    Update clock for quarter change.
    If halftime, reset and kickoff, if 5th quarter, game's done.
    """
    GAME.clock[0] = QNAMES[QNAMES.index(GAME.clock[0])+1]
    if GAME.clock[0] == 'END':
        gameOver()
    GAME.clock[1] = 720
    if GAME.clock[0] == QNAMES[2]:
        GAME.printables.append("Halftime!")
        if GAME.startingstance == "Offense" and GAME.localstance == "Offense":
            GAME.toggleStance()
        kickoff()


def gameOver():
    """
    The game is done. Toggle killswitch.
    """
    GAME.build_state("Game over")  # Only for CMD mode
    GAME.build_state("Final score: %s to %s" % (GAME.score[0], GAME.score[1]))  # Only for CMD mode
    GAME.end = True


def handleFluff():
    """
    Log some stats as to the current state of the game.
    For CMD mode only.
    """
    if GAME.firstdown >= 100:
        GAME.build_state("%s and goal on the %s" % (QNAMES[GAME.down-1], GAME.yard))
    else:
        GAME.build_state("%s and %s on the %s" % (QNAMES[GAME.down-1], GAME.firstdown-GAME.yard, GAME.yard))


def handleFluffCall():
    """
    Log the calls made, and the rolled results on their individual table.
    """
    GAME.build_state("Offense callout: %s -> %s" % (GAME.offplay, GAME.rolls['Offense']))
    GAME.build_state("Defense callout: %s -> %s" % (GAME.defplay, GAME.rolls['Defense']))


def handleTD():
    """
    Manage touchdowns. Update the score and toggle the TD switch, but DO NOT KICKOFF AGAIN YET.
    """
    if GAME.yard >= 100:
        handleScore()
        GAME.build_state("TOUCHDOWN!")  # Only for CMD mode
        GAME.TD = True


def handleScore():
    """
    Update the score of the game by one touchdown.
    TODO: handle extra points, safeties and field goals.
    """
    if GAME.localstance == "Offense":
        GAME.score[0] += 7
    else:
        GAME.score[1] += 7


def handleDowns():
    """
    Handle everything concerning the changing of downs.
    Ignore if TD
    Set to first down if |gain|>10
    Increment down
    If 5th down, turn the ball over to the defensive team.
    """
    if GAME.yard >= 100:  # TD
        return
    if GAME.yard >= GAME.firstdown:
        GAME.down = 1
        GAME.firstdown = GAME.yard + 10
        GAME.build_state("First Down!")  # Only for CMD mode
    else:
        GAME.down += 1
    if GAME.down == 5:
        turnOver()


def fullTurn():
    """
    Process everything needed for a full turn of fuhbuh.
    The rolls should already be complete before this function is run.
    Resets the chosen offensive and defensive plays at the end.
    """
    handleFluffCall()  # Only for CMD mode
    play.processPlay()
    handleDowns()
    handleTD()
    clock(GAME.boob)
    GAME.offplay = None
    GAME.defplay = None
    handleFluff()  # Only for CMD mode


def kickoff():
    """
    Process all necesary calls for a kickoff.
    TODO: Kickoff returns as a decision.
    """
    GAME.TD = False
    GAME.yard = 40
    play.customKey('Kickoff', 'Kickoff')
    GAME.toggleStance()
    play.customKey('Kickoff Return', 'Kickoff Return')
    GAME.firstdown = GAME.yard + 10
    GAME.down = 1
    handleFluff()  # Only for CMD mode


def punt():
    """
    Process all necessary calls for a punt.
    TODO: Punt return is sus.
    """
    play.customKey('Punt', 'Punt')
    GAME.toggleStance()
    play.customKey('Punt Return', 'Punt Return')
    GAME.firstdown = GAME.yard + 10
    GAME.down = 1
    handleFluff()
