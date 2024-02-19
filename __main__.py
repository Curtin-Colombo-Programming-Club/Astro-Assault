import argparse
from time import sleep
import Server
from Server import app, socketio
from Server.utils import *
from Server.controllers import *
import threading
import Screen
from Screen.utils import *


def main():
    parser = argparse.ArgumentParser(description='Description of your program')

    # Add arguments
    parser.add_argument('--host', type=int, help='Description of arg1')
    parser.add_argument('--port', '-p', type=float, help='Description of arg2')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the parsed arguments
    print("arg1:", args.host)
    print("arg2:", args.port)
    Server.init()
    Screen.init()

    GameThread = threading.Thread(target=Screen.run)
    GameThread.daemon = True
    GameThread.start()

    sleep(2)
    st = threading.Thread(
        target=Server.start,
        kwargs={
            "app": app,
            "host": args.host if args.host else "0.0.0.0",
            "port": args.port if args.port else 5000,
            "debug": False,
            "use_reloader": False,
            "allow_unsafe_werkzeug": True
        }
    )
    st.run()
    st.daemon = True
    print("reeeedaaaa")


if __name__ == "__main__":
    main()

