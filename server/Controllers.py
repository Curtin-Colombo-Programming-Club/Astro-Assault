import datetime
import json
import uuid
from typing import Dict
from server.GameUtils import *
from flask_socketio import SocketIO, join_room, emit
from flask import Flask, render_template, request, make_response, url_for, send_file, redirect, jsonify
from server.GameUtils import *
from server import GLOBALS
import qrcode
from io import BytesIO


class SocketController:
    def __init__(self, socketio: SocketIO):
        self.__io = socketio
        self.__players: Players = GLOBALS.PLAYERS
        self.__sessions = {}

    def control(self):
        @self.__io.on('connect')
        def connect_handler():
            client_address = request.remote_addr
            print(f"Client connected from IP address: {client_address}")
            print("connected, sid:", request.sid)
            _token = request.args.get('token')
            _player = self.__players[_token]

            print(f"SOCK connection Established;\n{_player}")

            """if _player is None:
                uuid1 = uuid.uuid1()
                uuid4 = str(uuid.uuid4()).replace("-", "")
                uuid3 = str(uuid.uuid3(uuid1, client_address)).replace("-", "")
                _player = self.__players.newPlayer(f"{uuid4}.{uuid3}")
                _token = _player.token

                print(f"New player;\n{_player}")"""

            _player.connect()
            print(f"player online;\n{_player}")

            self.__sessions[request.sid] = _player

            join_room(sid=request.sid, room=_token)

            emit("auth", {"token": _token}, to=_token)
            emit('cookie_set',
                 {'cookie_name': 'auth_token', 'cookie_value': _token, 'expiry_time': (datetime.datetime.now()+datetime.timedelta(hours=1)).timestamp()})

        @self.__io.on("movement")
        def movement_handler(data):
            returnData: dict[str, str | int] = {"status": -1, "message": ""}

            _dx = data["dx"]
            _dy = data["dy"]
            _token = data.get('auth_token', None)

            _player = self.__players[_token]

            if _player:
                _ship = _player.ship
                _ship.sockMoveUpdate(_dx, _dy)
                returnData["status"] = 200
                returnData["message"] = "success!"
            else:
                returnData["status"] = 404
                returnData["message"] = "player not found!"

            return returnData

        @self.__io.on("trigger")
        def trigger_handler(data):
            returnData: dict[str, str | int] = {"status": -1, "message": ""}

            _n = data["n"]
            # print("trigger", _n)
            _token = data.get('auth_token', None)

            _player = self.__players[_token]

            if _player:
                _ship = _player.ship
                _ship.sockTriggerUpdate(_n)
                returnData["status"] = 200
                returnData["message"] = "success!"
            else:
                returnData["status"] = 404
                returnData["message"] = "player not found!"

            return returnData

        @self.__io.on("respawn")
        def respawn(data):
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

        @self.__io.on("disconnect")
        def disconnect_handler():
            print(request.cookies.get('auth_token'), "disconnect!")

            _player = self.__sessions[request.sid]
            _player.disconnect()

            self.__sessions.pop(request.sid, None)

    def send(self, _event: str, _data, _to):
        self.__io.emit(_event, _data, to=_to)


class HTTPController:
    def __init__(self, app: Flask):
        self.__app = app
        self.__app.template_folder = "client/templates"
        self.__app.static_folder = "client/static"
        self.__players = GLOBALS.PLAYERS

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
                uuid1 = uuid.uuid1()
                uuid4 = str(uuid.uuid4()).replace("-", "")
                uuid3 = str(uuid.uuid3(uuid1, request.remote_addr)).replace("-", "")
                _token = f"{uuid4}.{uuid3}"
                print(request.form)
                _player = self.__players.newPlayer(
                    _token=_token,
                    _username=_username,
                    _color=_color
                )

                _expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
                response = make_response(jsonify({'auth_token': _token, 'username': _username}))
                response.set_cookie(key='auth_token', value=_token, path="/", expires=_expiration_time)
                response.set_cookie(key='username', value=_username, path="/", expires=_expiration_time)
                response.set_cookie(key='login_status', value='true', path="/", expires=_expiration_time)
                response.status = 200

                return response

        @self.__app.route("/controller", methods=["GET"])
        def controller():
            _token = request.cookies.get('auth_token', None)
            _player = self.__players[_token]

            if _player:
                return render_template("controller3.html")
            else:
                return redirect("/")

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


