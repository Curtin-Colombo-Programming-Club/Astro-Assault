from flask_socketio import SocketIO, join_room, emit
from flask import Flask, render_template, request
from server.GameUtils import *


class SocketController:
    def __init__(self, socketio: SocketIO, players: Players):
        self.__io = socketio
        self.__players = players

    def control(self):
        @self.__io.on('connect')
        def connect_handler():
            client_address = request.remote_addr
            print(f"Client connected from IP address: {client_address}")
            print("connected", request.sid)
            _token = request.args.get('token')
            _player = self.__players[_token]

            if _player is None:
                _player = self.__players.newPlayer("custom-token")
                _token = _player.token

            _player.connect()

            print(_player)

            join_room(sid=request.sid, room=_token)

            emit("auth", {"token": _token}, to=_token)

            request.token = _token

        @self.__io.on("disconnect")
        def disconnect_handler():
            _player = self.__players[request.token]
            _player.disconnect()


class HTTPController:
    def __init__(self, app: Flask, players: Players):
        self.__app = app
        self.__app.template_folder = "client/templates"
        self.__app.static_folder = "client/static"
        self.__players = players

    def control(self):
        @self.__app.route("/controller", methods=["GET"])
        def controller():
            print("hereeeee", self.__app.template_folder)
            return render_template("controller.html")

        @self.__app.route("/test", methods=["GET"])
        def test():
            return render_template("test2.html")
