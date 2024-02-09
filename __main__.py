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
GLOBALS.SHIPS = Ships()
GLOBALS.LASERS = Lasers()
GLOBALS.MISSILES = Missiles()
GLOBALS.HIT_MARKS = HitMarks()
GLOBALS.GAMERUNNING = False

# inits
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
pygame.init()

# controls
GLOBALS.SOCK = SocketController(socketio)
GLOBALS.SOCK.control()
HTTPController(app).control()


# Set up display
def Game():
    if GLOBALS.GAMERUNNING:
        return -1

    GLOBALS.GAMERUNNING = True
    screen = pygame.display.set_mode((10000, 10000), pygame.FULLSCREEN)
    pygame.display.set_caption("Astro Assault")

    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    GLOBALS.WIDTH = screen.get_width()
    GLOBALS.HEIGHT = screen.get_height()
    GLOBALS.H_RATIO = GLOBALS.HEIGHT / 1080
    GLOBALS.W_RATIO = GLOBALS.WIDTH / 1920
    print(GLOBALS.WIDTH, GLOBALS.HEIGHT)

    print(Players)

    # Set up font
    font = pygame.font.Font(None, 20)  # You can choose your own font and size

    # Main game loop
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

        GLOBALS.SHIPS.draw(screen)
        GLOBALS.SHIPS.update()

        GLOBALS.HIT_MARKS.draw(screen)
        GLOBALS.HIT_MARKS.update()

        # Check for collisions between the two groups
        collisions1 = pygame.sprite.groupcollide(GLOBALS.MISSILES, GLOBALS.LASERS, True, True)
        collisions2 = pygame.sprite.groupcollide(GLOBALS.LASERS, GLOBALS.SHIPS,
                                                 True, False,
                                                 check_collision)
        collisions3 = pygame.sprite.groupcollide(GLOBALS.MISSILES, GLOBALS.SHIPS,
                                                 True, False,
                                                 check_collision)

        """for sprite1, sprite2_list in collisions2.items():
            for sprite2 in sprite2_list:
                sprite2.dealDamage(1)
                #pygame.draw.rect(screen, (255, 0, 0), sprite1.rect, 2)
                #pygame.draw.rect(screen, (255, 0, 0), sprite2.rect, 2)"""

        GLOBALS.FPS = clk.get_fps()

        # Render FPS text
        fps_text = font.render("FPS: " + str(int(GLOBALS.FPS)), True, (0, 255, 10))
        screen.blit(fps_text, (10, 10))  # Adjust position as needed

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clk.tick(100)


GameThread = threading.Thread(target=Game)
GameThread.daemon = True
GameThread.start()

sleep(2)

socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
