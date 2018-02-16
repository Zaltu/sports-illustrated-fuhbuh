# CMD play for testing

from src import GAME
from src.play import play

GAME.setTeam('raiders.json')
GAME.setEnemy('raiders.json')

GAME.rolls = {
    'Attack':'+ 5 *',
    'Defense':':- 2'
}

print GAME

print play.processPlay()
