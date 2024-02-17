from flask import Flask
from flask_socketio import SocketIO
import GLOBALS
from Server.Controllers import *
from Server.Utils import *


# inits
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def init():
    # GLOBALS
    GLOBALS.PLAYERS = Players()
    GLOBALS.SOCK = SocketController(socketio)
    GLOBALS.SOCK.control()
    HTTPController(app).control()


def start(host="0.0.0.0", port=5000, debug=False, use_reloader=False):
    socketio.run(app, host=host, port=port, debug=debug, use_reloader=use_reloader, allow_unsafe_werkzeug=True)
