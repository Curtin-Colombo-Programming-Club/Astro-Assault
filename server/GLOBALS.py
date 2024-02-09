from server.GameUtils import *
from server.Controllers import *

# GLOBALS
SOCK: SocketController | None = None
FPS = 0
GAMERUNNING = False
WIDTH = 1000
HEIGHT = 1000
H_RATIO = 1
W_RATIO = 1
C_RATIO = 2 / 3
PLAYERS: Players | None = None
SHIPS: Ships | None = None
LASERS: Lasers | None = None
MISSILES: Missiles | None = None
HIT_MARKS: HitMarks | None = None
