import sys
import time
from time import sleep
import pygame.display
import pygame.display
import GLOBALS
import Game
from Game.Utils import *
import Server
from Server import app, socketio
from Server.Utils import *
from Server.Controllers import *
import threading
import pygame.surface


Server.init()
Game.init()

# controls
GLOBALS.SOCK = SocketController(socketio)
GLOBALS.SOCK.control()
HTTPController(app).control()

GameThread = threading.Thread(target=Game.run)
GameThread.daemon = True
GameThread.start()

sleep(2)

socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
