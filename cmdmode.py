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
GAME.rolls = {}

GAME.validateState()

GAME.firstdown = 50

for i in range(0, 10):
    GAME.localstance = "Defense"
    play.roll("Standard", offensePlay=GAME.callout)

    GAME.localstance = "Offense"
    turnController.fullTurn()

    if GAME.TD:
        turnController.kickoff()

print "Final yard: %s" % GAME.yard
print "Final down: %s" % GAME.down



#i = random.random()*100
#print i
#print GAME.weightedRoll("Attack", i)
