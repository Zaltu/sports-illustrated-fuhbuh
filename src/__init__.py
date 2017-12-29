from libs.namespace import Namespace
from src.play import play
from gui.sub.coinflip import CoinFlip
from gui.sub.stateerror import StateError


STANCES = ['Offense', 'Defense', 'Kick', 'Return']
GAME = Namespace()
GAME.clock = ['1st', 720]
GAME.simplePriorityLow = ['+', '-']
GAME.score = (0, 0) # (Me, Them)
GAME.state = CoinFlip
GAME.conn = None # IP address or connection object for the second player

GAME.playmap = {
    '+': play.soft,
    '-': play.soft,
    ':+': play.hard,
    ':-': play.hard,
    'OP': lambda t='OP': play.penalty(towards=t),
    'DF': lambda t='DF': play.penalty(towards=t),
    'PI': lambda t='PI': play.penalty(towards=t),
    '0': play.incomplete,
    ':TD': play.hard,
    'QT': play.qtrouble,
    'INT': play.intercept
}

GAME.priority = {

}


def setTeam(team):
    GAME.team = team
    return 1

def setEnemy(team):
    GAME.enemy = team
    return 1

def setState(state):
    GAME.state = state
    return 1

GAME.setTeam = setTeam
GAME.setEnemy = setEnemy
GAME.setState = setState

def validateState():
    try:
        assert GAME.team
        assert GAME.enemy
        assert GAME.state
        assert GAME.turn
        assert GAME.clock
        assert GAME.score
        assert GAME.conn
    except AssertionError:
        GAME.state = StateError
        return 0
    return 1
