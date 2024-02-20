import threading
from time import sleep

from Server.controllers import *
from Server.utils import *


SOCK: SocketController | None = None
PLAYERS: Players | None = None
DISPLAYS: Displays | None = None

# inits
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def init():
    global PLAYERS, DISPLAYS, SOCK
    # GLOBALS
    PLAYERS = Players()
    DISPLAYS = Displays()
    SOCK = SocketController(socketio)
    SOCK.control()
    HTTPController(app).control()

