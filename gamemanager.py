import json

from src import GAME
from src import turnController
from conn import queue

WAITING_PRINTABLES = ["WAITING"]

class Gamer():
    def __init__(self):
        self.ready = False
        self.Q = queue.FuhbuhQueue()

    def connectPlayer(self, event, connection):
        if not self.Q.player1:
            self.Q.connect(event["user_name"], event["message"], connection)
            return WAITING_PRINTABLES
        if not self.Q.player2:
            self.Q.connect(event["user_name"], event["message"], connection)
            self.ready = True
            turnController.handleFluff()
            toprint = [[[self.Q.player1.nameid,self.Q.player1.team],[self.Q.player2.nameid,self.Q.player2.team]]] + GAME.printables
            GAME.printables = []
            return toprint

    def makeplay(self, event):
        if event["user_name"] == self.Q.player1.nameid:
            self.Q.player1.makeCall(event["message"])
        elif event["user_name"] == self.Q.player2.nameid:
            self.Q.player2.makeCall(event["message"])

        if GAME.TD:
            turnController.kickoff()

    def emit(self, printables):
        for printable in printables:
            try:
                self.Q.player1.socketconn.send(json.dumps({
                    "user_name": "system",
                    "message": printable
                }))
            except AttributeError:
                # Player1 not yet ready
                pass
            try:
                self.Q.player2.socketconn.send(json.dumps({
                    "user_name": "system",
                    "message": printable
                }))
            except AttributeError:
                # Player2 not yet ready
                pass

game = Gamer()

def staticfork(event, connection):
    if not game.ready:
        game.emit(game.connectPlayer(event, connection) or ["Connected Successfully", event["message"]])
    else:
        game.makeplay(event)
        toprint = GAME.printables
        GAME.printables = []
        game.emit(toprint or WAITING_PRINTABLES)
    


