from src import GAME


# DEPRECATED

def setTeam(team):
    GAME.team = team
    return 1

def setEnemy(team):
    GAME.enemy = team
    return 1

def setState(state):
    GAME.state = state
    return 1
