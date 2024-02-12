import sys
import time
from time import sleep

import pygame.display
import pygame.display
from flask import Flask
from flask_socketio import SocketIO
from server import GLOBALS
from server.GameUtils import *
from server.Controllers import *
import threading
import pygame.surface

# GLOBALS
GLOBALS.PLAYERS = Players()
GLOBALS.SHIPS = Ships()
GLOBALS.LASERS = Lasers()
GLOBALS.MISSILES = Missiles()
GLOBALS.HIT_MARKS = HitMarks()
GLOBALS.GAMERUNNING = False


def on_screen_resize():
    GLOBALS.SHIPS.on_screen_resize()
    GLOBALS.LASERS.on_screen_resize()
    GLOBALS.MISSILES.on_screen_resize()
    GLOBALS.HIT_MARKS.on_screen_resize()


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
    screen = pygame.display.set_mode((GLOBALS.WIDTH, GLOBALS.HEIGHT))
    pygame.display.set_caption("Astro Assault")

    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    GLOBALS.WIDTH = screen.get_width()
    GLOBALS.HEIGHT = screen.get_height()
    GLOBALS.H_RATIO = GLOBALS.HEIGHT / 1080
    GLOBALS.W_RATIO = GLOBALS.WIDTH / 1920
    print(GLOBALS.WIDTH, GLOBALS.HEIGHT)

    print("screen", hasattr(screen, "blits"))

    # Set up font
    font = pygame.font.Font(None, 45)  # You can choose your own font and size

    # Main game loop
    clk = pygame.time.Clock()
    last_tick_time = pygame.time.get_ticks()
    while True:
        st = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Check if Alt and Enter are pressed simultaneously
                if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    GLOBALS.FULLSCREEN = not GLOBALS.FULLSCREEN
                    GLOBALS.p_H_RATIO = GLOBALS.H_RATIO
                    GLOBALS.p_W_RATIO = GLOBALS.W_RATIO
                    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN) if GLOBALS.FULLSCREEN else pygame.display.set_mode((1280, 720))
                    GLOBALS.WIDTH = screen.get_width()
                    GLOBALS.HEIGHT = screen.get_height()
                    GLOBALS.H_RATIO = GLOBALS.HEIGHT / 1080
                    GLOBALS.W_RATIO = GLOBALS.WIDTH / 1920
                    on_screen_resize()
                    print(GLOBALS.WIDTH, GLOBALS.HEIGHT)

        current_tick_time = pygame.time.get_ticks()
        elapsed_time = current_tick_time - last_tick_time
        GLOBALS.ELAPSED_TIME = elapsed_time
        GLOBALS.TICK_RATE = 1000/elapsed_time if elapsed_time > 0 else 1
        # Update game logic here

        # Clear the screen
        screen.fill(black)

        # updatex
        GLOBALS.LASERS.updatex(_screen=screen)

        GLOBALS.MISSILES.updatex(_screen=screen)

        GLOBALS.SHIPS.updatex(_screen=screen)

        GLOBALS.HIT_MARKS.updatex(_screen=screen)

        # Check for collisions between the two groups
        collisions1 = pygame.sprite.groupcollide(GLOBALS.MISSILES, GLOBALS.LASERS, True, True)
        collisions2 = pygame.sprite.groupcollide(GLOBALS.LASERS, GLOBALS.SHIPS,
                                                 True, False,
                                                 check_collision)
        collisions3 = pygame.sprite.groupcollide(GLOBALS.MISSILES, GLOBALS.SHIPS,
                                                 True, False,
                                                 check_collision)

        GLOBALS.FPS = clk.get_fps()

        # Render FPS text
        fps_text = pygame.transform.scale(_im := font.render(str(int(GLOBALS.FPS)), True, (0, 255, 10)), (_im.get_width() * GLOBALS.W_RATIO * GLOBALS.C_RATIO, _im.get_height() * GLOBALS.H_RATIO * GLOBALS.C_RATIO))
        screen.blit(fps_text, (10, 10))  # Adjust position as needed

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clk.tick(200)
        #print("fps", 1/(time.time()-st))

        last_tick_time = current_tick_time


GameThread = threading.Thread(target=Game)
GameThread.daemon = True
GameThread.start()

sleep(2)

socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
