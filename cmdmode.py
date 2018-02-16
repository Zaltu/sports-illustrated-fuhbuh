# CMD play for testing
from pprint import pprint as pp

from src import GAME
from src import turnController
from src.play import play

GAME.setTeam('raiders.json')
GAME.setEnemy('raiders.json')

GAME.rolls = {
    'Attack':'+ 5 *',
    'Defense':':- 2'
}

pp(GAME)

GAME.turn = "dummy"
GAME.down = 1

GAME.validateState()

turnController.fullTurn()

pp(GAME)
