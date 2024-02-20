import pygame

import Screen
from Screen.utils import *
import sys
import time
from Screen.sock import *
import Screen.sock as sock
import socketio
import os


NAME: str = ""
SHIPS: Ships | None = None
LASERS: Lasers | None = None
MISSILES: Missiles | None = None
HIT_MARKS: HitMarks | None = None
FORCES: Forces | None = None
GAMERUNNING = None
FPS = 0
ELAPSED_TIME = 1
TICK_RATE = 1
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False
DRAW_FORCES = False
H_RATIO = HEIGHT / 1080
p_H_RATIO = H_RATIO
W_RATIO = WIDTH / 1920
p_W_RATIO = W_RATIO
C_RATIO = 2 / 3

OFFLINE_SHIPS: SimpleShips | None = None
DEAD_SHIPS: SimpleShips | None = None

UNIT_FORCE = 300_000
DENSITY = 0.0001
DRAG_FACTOR = 0.05

sio = socketio.Client()


def on_screen_resize():
    global SHIPS, OFFLINE_SHIPS, LASERS, MISSILES, HIT_MARKS, FORCES, GAMERUNNING
    SHIPS.on_screen_resize()
    LASERS.on_screen_resize()
    MISSILES.on_screen_resize()
    HIT_MARKS.on_screen_resize()


def init():
    Screen.SHIPS = Ships()
    Screen.OFFLINE_SHIPS = SimpleShips()
    Screen.DEAD_SHIPS = SimpleShips()
    Screen.LASERS = Lasers()
    Screen.MISSILES = Missiles()
    Screen.HIT_MARKS = HitMarks()
    Screen.FORCES = Forces()
    Screen.GAMERUNNING = False
    pygame.init()
    eventManager(sio)
    # connect(sio)


def run():
    global SHIPS, LASERS, MISSILES, HIT_MARKS, FORCES, GAMERUNNING

    if GAMERUNNING:
        return -1

    GAMERUNNING = True
    screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT), pygame.DOUBLEBUF | pygame.SCALED | pygame.HWSURFACE | pygame.HWACCEL)
    pygame.display.set_caption("Astro Assault")

    # Set the icon
    pygame.display.set_icon(pygame.image.load(f"{os.path.dirname(__file__)}/images/icon.png"))

    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    Screen.WIDTH = screen.get_width()
    Screen.HEIGHT = screen.get_height()
    Screen.H_RATIO = Screen.HEIGHT / 1080
    Screen.W_RATIO = Screen.WIDTH / 1920
    print(Screen.WIDTH, Screen.HEIGHT)

    # Set up font
    font = pygame.font.Font(None, 45)  # You can choose your own font and size

    # Main game loop
    clk = pygame.time.Clock()
    last_tick_time = pygame.time.get_ticks()
    _start = time.time()
    while True:
        st = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Screen.quit()
            elif event.type == pygame.KEYDOWN:
                # Check if Alt and Enter are pressed simultaneously
                if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    Screen.FULLSCREEN = not Screen.FULLSCREEN
                    Screen.p_H_RATIO = Screen.H_RATIO
                    Screen.p_W_RATIO = Screen.W_RATIO
                    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED | pygame.HWSURFACE | pygame.HWACCEL) if Screen.FULLSCREEN else pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.SCALED | pygame.HWSURFACE | pygame.HWACCEL)
                    Screen.WIDTH = screen.get_width()
                    Screen.HEIGHT = screen.get_height()
                    Screen.H_RATIO = Screen.HEIGHT / 1080
                    Screen.W_RATIO = Screen.WIDTH / 1920
                    on_screen_resize()
                    print(Screen.WIDTH, Screen.HEIGHT)
                if event.key == pygame.K_f and pygame.key.get_mods() & (pygame.KMOD_LSHIFT or pygame.KMOD_RSHIFT):
                    Screen.DRAW_FORCES = not Screen.DRAW_FORCES

        _end = time.time()
        _elapsed = _end - _start
        _start = _end
        current_tick_time = pygame.time.get_ticks()
        elapsed_time = current_tick_time - last_tick_time
        last_tick_time = current_tick_time
        Screen.ELAPSED_TIME = elapsed_time

        # print(Screen.ELAPSED_TIME)
        Screen.TICK_RATE = 1/_elapsed if _elapsed > 0 else 1

        # Clear the screen
        screen.fill(black)

        # updatex
        #print(SHIPS)
        LASERS.updatex(_screen=screen)

        MISSILES.updatex(_screen=screen)

        Screen.SHIPS.updatex(_screen=screen)

        HIT_MARKS.updatex(_screen=screen)

        if Screen.DRAW_FORCES:
            FORCES.updatex(_screen=screen)

        # Check for collisions between the two groups
        collisions1 = pygame.sprite.groupcollide(MISSILES, LASERS, True, True)
        collisions2 = pygame.sprite.groupcollide(LASERS, SHIPS,
                                                 True, False,
                                                 check_collision)
        collisions3 = pygame.sprite.groupcollide(MISSILES, SHIPS,
                                                 True, False,
                                                 check_collision)

        Screen.FPS = clk.get_fps()

        # Render FPS text
        fps_text = pygame.transform.scale(_im := font.render(str(int(Screen.FPS)), True, (0, 255, 10)), (_im.get_width() * Screen.W_RATIO * Screen.C_RATIO, _im.get_height() * Screen.H_RATIO * Screen.C_RATIO))
        screen.blit(fps_text, (10, 10))  # Adjust position as needed

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clk.tick(200)
        # print("fps", 1/(time.time()-st))


def quit():
    pygame.quit()
    sio.disconnect()
    sys.exit()
