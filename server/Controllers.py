import datetime
import json
import uuid
from typing import Dict
from Server.utils import *
from flask_socketio import SocketIO, join_room, emit, namespace
from flask import Flask, render_template, request, make_response, url_for, send_file, redirect, jsonify
from Server.utils import *
import qrcode
from io import BytesIO
import Server


def token(client_addr) -> str:
    uuid1 = uuid.uuid1()
    uuid4 = str(uuid.uuid4()).replace("-", "")
    uuid3 = str(uuid.uuid3(uuid1, client_addr)).replace("-", "")

    return f"{uuid4}.{uuid3}"


class SocketController:
    def __init__(self, socketio: SocketIO):
        self.__io = socketio
        self.__players: Players = Server.PLAYERS
        self.__player_sessions = {}
        self.__display_sessions = {}

    def control(self):
        @self.__io.on("connect", namespace="/")
        def on_connect():
            client_address = request.remote_addr
            print(f"Client connected from IP address: {client_address}")
            print("connected, sid:", request.sid)
            _token = request.args.get('token')
            _player = self.__players[_token]

            if _player is None:
                self.__io.emit("error", "none existing user!")
            else:

                print(f"SOCK connection Established;\n{_player}")

                _player.connect()
                print(f"player online;\n{_player}")

                self.__player_sessions[request.sid] = _player

                join_room(sid=request.sid, room=_token)

                emit("auth", {"token": _token}, to=_token)
                emit('cookie_set',
                     {'cookie_name': 'auth_token', 'cookie_value': _token,
                      'expiry_time': (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()})

        @self.__io.on("movement", namespace="/")
        def on_movement(data):
            returnData: dict[str, str | int] = {"status": -1, "message": ""}

            _dx = data["dx"]
            _dy = data["dy"]
            _token = data.get('auth_token', None)

            _player = self.__players[_token]

            if _player:

                Server.DISPLAYS.movementUpdate(
                    _sock_data={
                        "dx": _dx,
                        "dy": _dy,
                        "token": _token
                    },
                    _player_token=_token
                )

                returnData["status"] = 200
                returnData["message"] = "success!"
            else:
                returnData["status"] = 404
                returnData["message"] = "player not found!"

            return returnData

        @self.__io.on("trigger", namespace="/")
        def on_trigger(data):
            returnData: dict[str, str | int] = {"status": -1, "message": ""}

            _n = data["n"]
            # print("trigger", _n)
            _token = data.get("auth_token", None)

            _player = self.__players[_token]

            if _player:
                Server.DISPLAYS.triggerUpdate(
                    {
                        "n": _n,
                        "token": _token
                    },
                    _player_token=_token
                )

                returnData["status"] = 200
                returnData["message"] = "success!"
            else:
                returnData["status"] = 404
                returnData["message"] = "player not found!"

            return returnData

        @self.__io.on("respawn", namespace="/")
        def on_respawn(data):
            returnData: dict[str, str | int] = {"status": -1, "message": ""}

            _token = data.get('auth_token', None)

            _player = self.__players[_token]

            if _player:
                _ship = _player.ship
                _ship.respawn()
                returnData["status"] = 200
                returnData["message"] = "success!"
            else:
                returnData["status"] = 404
                returnData["message"] = "player not found!"

        @self.__io.on("disconnect", namespace="/")
        def on_disconnect():
            print(request.cookies.get('auth_token'), "disconnect!")

            try:
                _player = self.__player_sessions[request.sid]
                Server.DISPLAYS.playerDisconnect(_player_token=_player.token)

                self.__player_sessions.pop(request.sid, None)
            except KeyError:
                pass

        @self.__io.on("connect", namespace="/game")
        def game_connect():
            client_address = request.remote_addr
            sid = request.sid
            print(f"Screen connected from IP address: {client_address}")
            print("> connected, sid:", sid)

            _token = f"display.{token(request.remote_addr)}"
            join_room(sid=sid, room=_token)

            _d = Server.DISPLAYS.new(_token=_token)

            self.__display_sessions[sid] = _d

            print("@connect")

        @self.__io.on("disconnect", namespace="/game")
        def game_disconnect():
            client_address = request.remote_addr
            sid = request.sid
            print(f"Screen disconnected from IP address: {client_address}")
            print("> disconnected, sid:", sid)
            _d = self.__display_sessions[sid]
            Server.DISPLAYS.remove(_d.token)
            self.__display_sessions.pop(sid, None)

    def send(self, _event: str, _data, _to, _namespace):
        self.__io.emit(_event, _data, to=_to, namespace=_namespace)


class HTTPController:
    def __init__(self, app: Flask):
        self.__app = app
        self.__app.template_folder = "../Client/templates"
        self.__app.static_folder = "../Client/static"
        self.__players = Server.PLAYERS

    def control(self):
        @self.__app.route("/", methods=["GET", "POST"])
        def start():
            if request.method == "GET":
                _token = request.cookies.get('auth_token', None)
                _player = self.__players[_token]
                if _player:
                    return render_template("controller3.html")
                else:
                    return render_template("start.html")
            elif request.method == "POST":
                _username = request.form.get("username", "no-name")
                _color = tuple(json.loads(request.form.get("color", "[255, 255, 255]")))
                _token = f"player.{token(request.remote_addr)}"
                print(request.form)
                _player = self.__players.newPlayer(
                    _token=_token,
                    _username=_username,
                    _color=_color
                )

                Server.DISPLAYS.joinPlayer(_player=_player)

                _expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
                response = make_response(jsonify({'auth_token': _token, 'username': _username}))
                response.set_cookie(key='auth_token', value=_token, path="/", expires=_expiration_time)
                response.set_cookie(key='username', value=_username, path="/", expires=_expiration_time)
                response.set_cookie(key='login_status', value='true', path="/", expires=_expiration_time)
                response.status = 200

                return response

        @self.__app.route("/game", methods=["GET", "POST"])
        def game():
            response = make_response()
            response.status = 200

            return response

        @self.__app.route("/<path>.qr", methods=["GET"])
        def qr(path):
            print(path)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            url = request.url_root + path
            print(url)
            qr.add_data(url)
            qr.make(fit=True)

            qr_img_stream = BytesIO()

            qr.make_image(fill_color="black", back_color="white").save(qr_img_stream)
            qr_img_stream.seek(0)

            return send_file(qr_img_stream, mimetype='image/png')


