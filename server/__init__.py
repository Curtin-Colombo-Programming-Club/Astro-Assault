import threading
from time import sleep

from Server.controllers import *
from Server.components import *
from Server.utils import *


SOCK: SocketController | None = None
PLAYERS = None
DISPLAYS: Displays | None = None
SHIPS: Ships | None = None
LASERS: Lasers | None = None
MISSILES: Missiles | None = None
FORCES: Forces | None = None
GAMERUNNING = None
TICK_RATE: float = 0
WIDTH = 1920
HEIGHT = 1080
C_RATIO = 2 / 3

UNIT_FORCE = 300_000
DENSITY = 0.0001
DRAG_FACTOR = 0.05

# inits
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def init():
    global PLAYERS, DISPLAYS, SOCK, SHIPS, LASERS, MISSILES, FORCES
    # GLOBALS
    PLAYERS = Players()
    DISPLAYS = Displays()
    SHIPS = Ships()
    LASERS = Lasers()
    MISSILES = Missiles()
    FORCES = Forces()
    SOCK = SocketController(socketio)
    SOCK.control()
    HTTPController(app).control()


def game():
    global TICK_RATE, SHIPS, LASERS, MISSILES
    _start = time.time()
    print(SHIPS)
    i = 0
    while True:
        # tick rate
        _end = time.time()
        _elapsed = _end - _start
        _start = _end
        TICK_RATE = 1 / _elapsed if _elapsed > 0 else 1
        SHIPS.update()
        LASERS.update()
        MISSILES.update()

        sleep(0.001)
