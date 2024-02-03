import sys
from flask import Flask
from flask_socketio import SocketIO
from server.GameUtils import *
from server.Controllers import *
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
pygame.init()

Players = Players()

Players.newPlayer("4322222")

SocketController(socketio, Players).control()
HTTPController(app, Players).control()

GAMERUNNING = False


# Set up display
def Game():
    global GAMERUNNING

    if GAMERUNNING:
        return -1

    GAMERUNNING = True
    width, height = 800, 600
    screen = pygame.display.set_mode((10000, 10000), pygame.FULLSCREEN)
    pygame.display.set_caption("Basic Pygame Example")

    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    print(screen.get_width(), screen.get_height())

    print(Players)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update game logic here

        # Clear the screen
        screen.fill(black)

        # Draw game elements here
        Players.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(60)


"""GameThread = threading.Thread(target=Game)
GameThread.daemon = True
GameThread.start()"""

socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
