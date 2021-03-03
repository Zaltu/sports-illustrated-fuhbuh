from src.play import roll, processPlay
from src.turnController import graphicDispatch
from src import GAME
import conn

def dispatchC(calloutInput):
    localReg = {GAME.localStance: roll(calloutInput, GAME.localStance)}

    host = conn.socket.validateResolveHost()
    if host:
        host.update(localReg)
        GAME.rolls = host
        graphicDispatch(processPlay())
    else:
        conn.socket.send(localReg)
    return
