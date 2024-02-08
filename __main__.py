import sys
from time import sleep

import pygame.display
import pygame.display
from flask import Flask
from flask_socketio import SocketIO
from server import GLOBALS
from server.GameUtils import *
from server.Controllers import *
import threading

# GLOBALS
GLOBALS.PLAYERS = Players()
GLOBALS.LASERS = Lasers()
GLOBALS.MISSILES = Missiles()
GLOBALS.GAMERUNNING = False

# inits
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
pygame.init()

# controls
SocketController(socketio).control()
HTTPController(app).control()


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

        # Check for collisions between the two groups
        collisions = pygame.sprite.groupcollide(GLOBALS.MISSILES, GLOBALS.PLAYERS, False, False)

        for sprite1, sprite2_list in collisions.items():
            for sprite2 in sprite2_list:
                print(sprite1, sprite2_list)
                pygame.draw.rect(screen, (255, 0, 0), sprite1.rect, 2)
                pygame.draw.rect(screen, (255, 0, 0), sprite2.rect, 2)

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clk.tick(60)

        GLOBALS.FPS = clk.get_fps()


GameThread = threading.Thread(target=Game)
GameThread.daemon = True
GameThread.start()

sleep(2)

socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
