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
import sys


def main(*args, **kwargs):
    Server.init()
    Game.init()

    GameThread = threading.Thread(target=Game.run)
    GameThread.daemon = True
    GameThread.start()

    sleep(2)
    Server.start()


if __name__ == "__main__":
    main(sys.argv)

