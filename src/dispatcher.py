from src.play import roll, processPlay
from src import turnController

def dispatch(calloutInput):
    localReg = roll(calloutInput, GAME.localStance)

    host = conn.socket.validateResolveHost() #TODO: this goes to dispatcher
    if host
        host.update(localReg)
        turnController(processPlay(host))
    return