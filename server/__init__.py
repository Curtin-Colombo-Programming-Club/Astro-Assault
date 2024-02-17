from flask import Flask
from flask_socketio import SocketIO
import GLOBALS
from Server.Utils import *


# inits
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def init():
    # GLOBALS
    GLOBALS.PLAYERS = Players()
