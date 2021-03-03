"""
Module storing all functionality revolving around managing a single turn in a game of fuhbuh.
TODO: All prints should be changed to loggers, as they are for CMD mode.
"""
from src import GAME, QNAMES
from src.play import play

def turnOver():
    """
    Turn the ball over to the team currently on defense.
    """
    print("Switched sides!")  # Only for CMD mode
    GAME.down = 1
    GAME.toggleStance()
    print("Offense is now on the %s yard line." % GAME.yard)  # Only for CMD mode


def clock(star):
    """
    Adjust the clock by one play (30 seconds). If the ball is out of bounds, a play lasts 10 seconds instead
    of 30.

    :param bool star: ball out of bounds
    """
    GAME.clock[1] -= 30 if not star else 10
    if GAME.clock[1] <= 0:
        print("Changing quarters")  # Only for CMD mode
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
        print("Halftime!")
        if GAME.startingstance == "Offense" and GAME.localstance == "Offense":
            GAME.toggleStance()
        kickoff()


def gameOver():
    """
    The game is done. Toggle killswitch.
    """
    print("Game over")  # Only for CMD mode
    print("Final score: %s to %s" % (GAME.score[0], GAME.score[1]))  # Only for CMD mode
    GAME.end = True


def handleFluff():
    """
    Log some stats as to the current state of the game.
    For CMD mode only.
    """
    print("")
    if GAME.firstdown >= 100:
        print("%s and goal on the %s" % (QNAMES[GAME.down-1], GAME.yard))
    else:
        print("%s and %s on the %s" % (QNAMES[GAME.down-1], GAME.firstdown-GAME.yard, GAME.yard))

    print("Game time: %s" % GAME.clock)

def handleFluffCall():
    """
    Log the calls made, and the rolled results on their individual table.
    """
    print("Offense callout: %s -> %s" % (GAME.offplay, GAME.rolls['Offense']))
    print("Defense callout: %s -> %s" % (GAME.defplay, GAME.rolls['Defense']))


def handleTD():
    """
    Manage touchdowns. Update the score and toggle the TD switch, but DO NOT KICKOFF AGAIN YET.
    """
    if GAME.yard >= 100:
        print("TOUCHDOWN!")  # Only for CMD mode
        handleScore()
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
        print("First Down!")  # Only for CMD mode
        GAME.down = 1
        GAME.firstdown = GAME.yard + 10
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
    handleFluff()  # Only for CMD mode
    handleFluffCall()  # Only for CMD mode
    play.processPlay()
    handleDowns()
    handleTD()
    clock(GAME.boob)
    GAME.offplay = None
    GAME.defplay = None


def kickoff():
    """
    Process all necesary calls for a kickoff.
    TODO: Kickoff returns as a decision.
    """
    print("")  # Only for CMD mode
    GAME.TD = False
    GAME.yard = 40
    play.customKey('Kickoff', 'Kickoff')
    GAME.toggleStance()
    play.customKey('Kickoff Return', 'Kickoff Return')
    GAME.firstdown = GAME.yard + 10
    GAME.down = 1


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
