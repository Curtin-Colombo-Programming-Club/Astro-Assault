import datetime
import uuid
from flask_socketio import SocketIO, join_room, emit
from flask import Flask, render_template, request, make_response
from server.GameUtils import *


class SocketController:
    def __init__(self, socketio: SocketIO, players: Players):
        self.__io = socketio
        self.__players = players
        self.__sessions = {}

    def control(self):
        @self.__io.on('connect')
        def connect_handler():
            client_address = request.remote_addr
            print(f"Client connected from IP address: {client_address}")
            print("connected, sid:", request.sid)
            _token = request.args.get('token')
            _player = self.__players[_token]

            print(f"Existing player;\n{_player}" if _player else "Creating new Player")

            if _player is None:
                uuid1 = uuid.uuid1()
                uuid4 = str(uuid.uuid4()).replace("-", "")
                uuid3 = str(uuid.uuid3(uuid1, client_address)).replace("-", "")
                _player = self.__players.newPlayer(f"{uuid4}.{uuid3}")
                _token = _player.token

                print(f"New player;\n{_player}")

            _player.connect()
            print(f"player online;\n{_player}")

            self.__sessions[request.sid] = _player

            join_room(sid=request.sid, room=_token)

            emit("auth", {"token": _token}, to=_token)
            emit('cookie_set',
                 {'cookie_name': 'auth_token', 'cookie_value': _token, 'expiry_time': (datetime.datetime.now()+datetime.timedelta(hours=1)).timestamp()})

        @self.__io.on("movement")
        def movement_handler(data):
            returnData = {"status": -1, "message": ""}

            _dx = data["dx"]
            _dy = data["dy"]
            _token = request.cookies.get('auth_token')

            _player = self.__players[_token]

            if _player:
                _ship = _player.ship
                _ship.dVelocity(_dx, _dy)
                returnData["status"] = 200
                returnData["message"] = "success!"
            else:
                returnData["status"] = 404
                returnData["message"] = "player not found!"

            return returnData

        @self.__io.on("disconnect")
        def disconnect_handler():
            print(request.cookies.get('auth_token'), "disconnect!")

            _player = self.__sessions[request.sid]
            _player.disconnect()

            self.__sessions.pop(request.sid, None)


class HTTPController:
    def __init__(self, app: Flask, players: Players):
        self.__app = app
        self.__app.template_folder = "client/templates"
        self.__app.static_folder = "client/static"
        self.__players = players

    def control(self):
        @self.__app.route("/controller", methods=["GET"])
        def controller():
            print(request.cookies.get('auth_token'))
            return render_template("controller.html")

        @self.__app.route("/test", methods=["GET"])
        def test():
            print(request.cookies.get('auth_token'), "/test")
            return render_template("test2.html")
