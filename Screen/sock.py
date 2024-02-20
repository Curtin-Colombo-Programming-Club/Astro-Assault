import json

import Screen


def eventManager(sio):
    # Define event handlers
    @sio.on("connect", namespace="/game")
    def on_connect():
        print('Connected to server')

    @sio.on("post_connect", namespace="/game")
    def on_post_connect(data):
        print(json.dumps(data, indent=4))
        for _ship_dict in data["ships"]:
            _ship = Screen.SHIPS.new(
                _token=_ship_dict["token"],
                _x=(_x := _ship_dict["x"]),
                _y=(_y := _ship_dict["y"]),
                _username=_ship_dict["username"],
                _color=(_color := _ship_dict["color"]),
                _angle=(_angle := _ship_dict["angle"])
            )
            _ship.center = (_x * Screen.W_RATIO, _y * Screen.H_RATIO)
            _ship.velocity = _ship_dict["velocity"]
            _ship.color = _color
            _ship.angle = _angle
            _ship.force.value = _ship_dict["force"]["value"]
            _ship.force.angle = _ship_dict["force"]["angle"]
            _ship.drag_force.value = _ship_dict["drag_force"]["value"]
            _ship.drag_force.angle = _ship_dict["drag_force"]["angle"]

        for _laser_dict in data["lasers"]:
            _ship = Screen.SHIPS[_laser_dict["token"]]
            _laser = Screen.LASERS.newLaser(
                _ship=_ship,
                _center=(_laser_dict["x"], _laser_dict["y"]),
                _angle=_laser_dict["angle"]
            )
            _laser.velocity = _laser_dict["velocity"]
            _laser.drag_force.value = _laser_dict["drag_force"]["value"]
            _laser.drag_force.angle = _laser_dict["drag_force"]["angle"]

    @sio.event
    def on_disconnect():
        print('Disconnected from server')

    @sio.on('new_ship', namespace='/game')
    def on_new_ship(data):
        _x = data["x"]
        _y = data["y"]
        _username = data["username"]
        _color = data["color"]
        _token = data["token"]

        s = Screen.SHIPS.new(_token=_token, _color=_color, _x=_x, _y=_y, _username=_username)
        print(s, Screen.SHIPS)
        print('on_new_ship:', data)

    @sio.on('new_.*', namespace='/game')
    def on_new_component(data):
        _component: str = data["event"][4:]
        _x = data["x"]
        _y = data["y"]
        _username = data["username"]
        _c = getattr(Screen, f"{_component.upper()}S")

        print('on_new_component:', data)

    @sio.on('del_.*', namespace='/game')
    def on_del_component(data):
        component = data["event"][4:]
        print('on_del_component:', data)

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
