# CMD play for testing
from pprint import pprint as pp
import random
import sys
import traceback
from src import GAME
from src import turnController
from conn import queue

ALL_D = ["Standard", "Short Yardage", "Spread", "Pass Prevent Short", "Pass Prevent Long", "Blitz"]  # 6
ALL_A = ["Line Plunge", "Off Tackle", "End Run", "Draw", "Screen", "Short", "Medium", "Long", "Sideline"]  # 9

def fullGame():
    """
    Test one full game of fuhbuh, from first kickoff to touchdown.
    """
    Q = queue.FuhbuhQueue()

    Q.connect(None, "raiders")
    Q.connect(None, "raiders")

    while not GAME.end:
        if Q.player1.localstance == "Offense":
            Q.player1.makeCall(ALL_A[random.randint(0, 8)])
            Q.player2.makeCall(ALL_D[random.randint(0, 5)])
        else:
            Q.player1.makeCall(ALL_D[random.randint(0, 5)])
            Q.player2.makeCall(ALL_A[random.randint(0, 8)])

        if GAME.TD:
            turnController.kickoff()

    print("Final yard: %s" % GAME.yard)
    print("Final down: %s" % GAME.down)

def heavyTest():
    """
    Perform a more intensive error testing by executing 100000 full games.
    Takes a while, and it prints everything...
    """
    errors = []
    while range(0, 100000):
        try:
            fullGame()
        except:  #pylint: disable=bare-except
            traceback.print_exc()
            sys.exit(0)
            errors.append(traceback.format_exc())

    pp(errors)


fullGame()
#heavyTest()
