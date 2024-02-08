import sys
from time import sleep

import pygame.display
import pygame.display
from flask import Flask
from flask_socketio import SocketIO
from server import GLOBALS
import server
from server.GameUtils import *
from server.Controllers import *
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
pygame.init()

# globals
GLOBALS.PLAYERS = Players()
GLOBALS.LASERS = Lasers()
GLOBALS.MISSILES = Missiles()

SocketController(socketio).control()
HTTPController(app).control()
SocketController(socketio).control()
HTTPController(app).control()

# GLOBALS
GLOBALS.GAMERUNNING = False


# Set up display
def Game():
    if GLOBALS.GAMERUNNING:
        return -1

    GLOBALS.GAMERUNNING = True
    screen = pygame.display.set_mode((10000, 10000), pygame.FULLSCREEN)
    pygame.display.set_caption("Basic Pygame Example")

    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    GLOBALS.WIDTH = screen.get_width()
    GLOBALS.HEIGHT = screen.get_height()
    GLOBALS.H_RATIO = GLOBALS.HEIGHT / 1080
    GLOBALS.W_RATIO = GLOBALS.WIDTH / 1920
    GLOBALS.H_RATIO = GLOBALS.HEIGHT / 1080
    GLOBALS.W_RATIO = GLOBALS.WIDTH / 1920
    print(GLOBALS.WIDTH, GLOBALS.HEIGHT)

    print(Players)

    # Main game loop
    clk = pygame.time.Clock()
    clk = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update game logic here

        # Clear the screen
        screen.fill(black)

        # Draw game elements here
        GLOBALS.LASERS.draw(screen)
        GLOBALS.LASERS.update()

        GLOBALS.MISSILES.draw(screen)
        GLOBALS.MISSILES.update()

        GLOBALS.PLAYERS.draw(screen)
        GLOBALS.PLAYERS.update()

        # Update the display
        pygame.display.update()
        pygame.display.update()

        # Control the frame rate
        clk.tick(60)

        GLOBALS.FPS = clk.get_fps()
        clk.tick(60)

        GLOBALS.FPS = clk.get_fps()


GameThread = threading.Thread(target=Game)
GameThread.daemon = True
GameThread.start()

sleep(2)

socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
