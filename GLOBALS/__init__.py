from Server.utils import *
from Server import controllers

# GLOBALS
SOCK: Controllers.SocketController | None = None
FPS = 0
ELAPSED_TIME = 1
TICK_RATE = 1
GAMERUNNING = False
GAMEPAUSED = False
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False
H_RATIO = 1
p_H_RATIO = H_RATIO
W_RATIO = 1
p_W_RATIO = W_RATIO
C_RATIO = 2 / 3
UNIT_FORCE = 300_000
DENSITY = 0.0001
DRAG_FACTOR = 0.05
# η
NEETA = 1
PLAYERS: Players | None = None
SHIPS: Ships | None = None
LASERS: Lasers | None = None
MISSILES: Missiles | None = None
HIT_MARKS: HitMarks | None = None
SHIP_MASKS = None
FORCES: Forces | None = None
DRAW_FORCES: bool = False
