from src.play import roll, processPlay
from src.turnController import graphicDispatch
import conn

def dispatchC(calloutInput):
    localReg = {GAME.localStance: roll(calloutInput, GAME.localStance)}

    host = conn.socket.validateResolveHost()
    if host
        host.update(localReg)
        graphicDispatch(processPlay(host))
    else:
        conn.socket.send(localReg)
    return
