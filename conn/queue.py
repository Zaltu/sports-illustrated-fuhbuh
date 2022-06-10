"""
Queue management object. Used to manage what state the queue is in, manage recieved information and fire
update events to the socket.
"""
from src import GAME
from src import turnController
from src.play import play


class Player():
    """
    Class representing a player connecting to the Fuhbuh multiplayer instance.

    :param socketio connection: connection with the remote player
    :param str team: player's team name
    :param FuhbuhQueue queue: the multiplayer game manager
    :param WebSocket socketconn: the player's ws connection, to send updates to
    """
    def __init__(self, nameid, team, queue, socketconn):
        self.nameid = nameid
        self.team = team
        self.queue = queue
        self.socketconn = socketconn
        if GAME.team:
            GAME.setEnemy(team, nameid)
            self.localstance = "Defense"
        else:
            GAME.setTeam(team, nameid)
            self.localstance = "Offense"

    def makeCall(self, call):
        """
        Acknowledge the recept of a call made by this player.

        :param str call: call made by the player (eg "End Run")
        """
        self.queue.submitCall(call, self.localstance, self)


class FuhbuhQueue():
    """
    Handles the management of a single given game of fuhbuh.
    Acts as the endpoint registrar for the socket governing the multiplayer game. Receives events from both
    players and fires events once the play has been processed.
    """
    def __init__(self):
        self.player1 = None
        self.player2 = None

    def connect(self, nameid, playerteam, connection):
        """
        Top-level observer pattern for connecting a player to the model.
        Passes the event received to the connection implementation, and sets the game state up if all players
        have joined.
        :param socketio nameid: UUID for this player, so we know when 2 have joined
        :param str playerteam: name of the team to assign.
        :param WebSocket connection: the player's ws connection, to send updates to
        """
        if self.player1:
            self.player2 = Player(nameid, playerteam, self, connection)
        else:
            self.player1 = Player(nameid, playerteam, self, connection)
        if self.player1 and self.player2:
            self.setupGame()

    def disconnect(self, disconnection):
        """
        Disconnect the player from the game, and reset the state for the next match.

        :param socketio disconnection: socket that was cleared

        :raises SystemError: if an unknown connection disconnected
        """
        self.player1 = None
        self.player2 = None
        self.setupGame()

    def setupGame(self):
        """
        Set up all the default values for the game state.
        """
        GAME.turn = "dummy"
        GAME.down = 1
        GAME.callout = 'End Run'
        GAME.rolls = {}
        GAME.localstance = "Offense"
        GAME.end = False
        GAME.startingstance = "Offense"
        GAME.firstdown = 50
        GAME.down = 1
        GAME.yard = 40
        GAME.firstdown = 50
        GAME.clock = ["1st", 720]
        GAME.end = False
        GAME.score = [0, 0]
        GAME.validateState()

    def submitCall(self, call, stance, player):
        """
        Process the result of the call, if possible.
        If all necessary calls have been made, process the turn.

        :param str call: the call made by the player (eg End Run)
        :param str stance: the stance (context) the call is made in
        """
        if call == "Kickoff":
            turnController.kickoff()
            self.correctStances()
            GAME.printables.append("READY")
            return
        elif call == "Punt":
            turnController.punt()
            self.correctStances()
            GAME.printables.append("READY")
            return

        if stance == "Offense":
            GAME.offplay = call
            GAME.callout = call
            play.roll(GAME.offplay, "Offense")
            if GAME.defplay:
                play.roll(GAME.defplay, "Defense", offensePlay=GAME.offplay)
            else:
                print("Waiting to player %s" % player.nameid)
                player.socketconn.send("WAITING")

        if stance == "Defense":
            GAME.defplay = call
            if GAME.offplay:
                play.roll(GAME.defplay, "Defense", offensePlay=GAME.offplay)
            else:
                print("Waiting to player %s" % player.nameid)
                player.socketconn.send("WAITING")

        if GAME.defplay and GAME.offplay:
            turnController.fullTurn()
            self.correctStances()
            GAME.printables.append("READY")



    def correctStances(self):
        """
        Correct player stances for future call submissions.
        We consider player1 to be TEAM and player2 to be ENEMY.
        Which is kind of dumb and will probably backfire.
        """
        self.player1.localstance = GAME.localstance
        if GAME.localstance == "Offense":
            self.player2.localstance = "Defense"
        else:
            self.player2.localstance = "Offense"
