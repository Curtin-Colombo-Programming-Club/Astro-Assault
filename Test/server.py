import argparse
import Server


def main():
    # Create ArgumentParser object
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
    Server.start(
        host=args.host if args.host else "0.0.0.0",
        port=args.port if args.port else 5000,
        debug=True,
        use_reloader=True
    )


if __name__ == '__main__':
    main()
