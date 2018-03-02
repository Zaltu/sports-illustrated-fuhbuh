# CMD play for testing
from pprint import pprint as pp
import random
from src import GAME
from src import turnController
from src.play import play

GAME.setTeam('raiders.json')
GAME.setEnemy('raiders.json')

GAME.turn = "dummy"
GAME.down = 1
GAME.callout = 'End Run'
GAME.into = "End Run"
GAME.rolls = {}
GAME.localstance = "Offense"
GAME.end = False

GAME.validateState()

GAME.firstdown = 50

def fullGame():
    for i in range(0, 150):

        if GAME.localstance == "Offense":
            GAME.localstance = "Defense"
            play.roll("Standard", offensePlay=GAME.into)

            GAME.callout = "End Run"
            GAME.localstance = "Offense"
            turnController.fullTurn()
        else:
            GAME.localstance = "Offense"
            play.roll("End Run")

            GAME.callout = "Standard"
            GAME.localstance = "Defense"
            turnController.fullTurn()


        if GAME.TD:
            turnController.kickoff()

    print "Final yard: %s" % GAME.yard
    print "Final down: %s" % GAME.down


errors = []
for i in range(0, 100000):
    try:
        GAME.down = 1
        GAME.yard = 40
        GAME.firstdown = 50
        GAME.clock = ["1st", 720]
        GAME.end = False
        fullGame()
    except Exception as e:
        errors.append(e)

pp(errors)

#i = random.random()*100
#print i
#print GAME.weightedRoll("Attack", i)
