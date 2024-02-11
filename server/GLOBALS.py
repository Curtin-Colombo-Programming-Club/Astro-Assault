from server.GameUtils import *
from server.Controllers import *

# GLOBALS
SOCK: SocketController | None = None
FPS = 0
ELAPSED_TIME = 1
GAMERUNNING = False
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False
H_RATIO = 1
W_RATIO = 1
C_RATIO = 2 / 3
UNIT_FORCE = 500e-8
MAX_SPEED = 5
PLAYERS: Players | None = None
SHIPS: Ships | None = None
LASERS: Lasers | None = None
MISSILES: Missiles | None = None
HIT_MARKS: HitMarks | None = None
