import json
import random

import Screen


def eventManager(sio):
    # Define event handlers
    @sio.on("connect", namespace="/game")
    def on_connect():
        print('Connected to server')

    @sio.event
    def on_disconnect():
        print('Disconnected from server')

    @sio.on('new_ship', namespace='/game')
    def on_new_ship(data):
        _x = random.randint(0, Screen.WIDTH)
        _y = random.randint(0, Screen.HEIGHT)
        _username = data["username"]
        _color = data["color"]
        _token = data["token"]

        s = Screen.SHIPS.new(_token=_token, _color=_color, _x=_x, _y=_y, _username=_username)
        print(s, Screen.SHIPS)
        print('on_new_ship:', data)

    @sio.on("movement_update", namespace="/game")
    def on_movement_update(data):
        _token = data["token"]
        _dx = data["dx"]
        _dy = data["dy"]
        Screen.SHIPS.sockMovementUpdate(_token=_token, _dx=_dx, _dy=_dy)

    @sio.on("trigger_update", namespace="/game")
    def on_trigger_update(data):
        _token = data["token"]
        _n = data["n"]
        Screen.SHIPS.sockTriggerUpdate(_token=_token, _n=_n)


# Connect to the server
def connect(sio, host="localhost", port=5000):
    sio.connect(f"http://{host}:{port}", namespaces=['/game'])
