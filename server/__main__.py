import Server
import threading
import argparse


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

    GameThread = threading.Thread(target=Server.game, daemon=True)
    GameThread.start()

    Server.socketio.run(
        app=Server.app,
        host=args.host if args.host else "0.0.0.0",
        port=args.port if args.port else 5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )


if __name__ == "__main__":
    main()

