import json

from flask import Flask
from flask_sock import Sock, ConnectionClosed

import gamemanager

VALIDATE_SERVER_EVENT_MESSAGE = "SERVER VALIDATION"

app = Flask(__name__)
sock = Sock(app)

@sock.route('/')
def echo(conn):
    try:
        while True:
            data = conn.receive()
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                print("INCORRECT DATA FORMAT")
                print(data)
                continue
            print('received:\n' + str(data))
            if data.get("data") == "User Connected":
                conn.send(VALIDATE_SERVER_EVENT_MESSAGE)
                continue
            gamemanager.staticfork(data, conn)
    except ConnectionClosed:
        print("Disconnected")
        gamemanager.disconnect()

if __name__ == '__main__':
    Flask.run(app, debug=True)