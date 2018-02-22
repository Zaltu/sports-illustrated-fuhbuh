# CMD play for testing
from pprint import pprint as pp
import random
from src import GAME
from src import turnController
from src.play import play

GAME.setTeam('raiders.json')
GAME.setEnemy('raiders.json')

GAME.rolls = {
    'Defense':'+ 0'
}

GAME.turn = "dummy"
GAME.down = 1
GAME.callout = 'Line Plunge'
GAME.localstance = "Offense"

GAME.validateState()

#i = random.random()*100
#print i

#print GAME.weightedRoll("Attack", i)

turnController.fullTurn()
pp(GAME)
