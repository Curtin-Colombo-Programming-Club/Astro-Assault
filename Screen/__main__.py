import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(fr"{os.path.dirname(CURRENT_DIR)}\Server")

import ctypes
import Screen
import argparse


def main():
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    parser = argparse.ArgumentParser(description='Description of your program')

    # Add arguments
    parser.add_argument('--host', type=str, help='Description of arg1')
    parser.add_argument('--port', '-p', type=int, help='Description of arg2')

    # Parse the command-line arguments
    args = parser.parse_args()

    Screen.init()
    Screen.connect(host=args.host if args.host else "192.168.8.2", port=args.port if args.port else 5000, sio=Screen.sio)
    Screen.run()


if __name__ == "__main__":
    main()
