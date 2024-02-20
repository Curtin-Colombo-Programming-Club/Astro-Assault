import datetime
import math
import random
import time
import pygame
from typing import Self
import Server


class Player:
    def __init__(self, _token: str, _username: str, _color: tuple):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()

        self.__token = _token
        self.__username = _username
        self.__display = None
        self.__kills = 0
        self.__deaths = 0
        self.__color = _color

    @property
    def display(self):
        return self.__display

    @display.setter
    def display(self, _display):
        self.__display = _display

    @property
    def color(self):
        return self.__color

    @property
    def online(self):
        return self.__online

    @property
    def lastOnline(self):
        return self.__lastOnline

    @property
    def token(self):
        return self.__token

    @property
    def username(self):
        return self.__username

    def connect(self):
        self.__online = True
        self.__lastOnline = datetime.datetime.now()

    def disconnect(self):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()

    def sockSend(self, _event, _data):
        Server.SOCK.send(_event=_event, _data=_data, _to=self.token, _namespace="/")

    def killed(self):
        self.__kills += 1
        self.sockSend(_event="kills", _data={"kills": self.__kills})

    def died(self):
        self.__deaths += 1
        self.sockSend(_event="deaths", _data={"deaths": self.__deaths})

    def __str__(self):
        return (f"Player(\n"
                f"\ttoken      : {self.token}\n"
                f"\tonline     : {self.online}\n"
                f"\tlast online: {self.lastOnline}\n"
                ")")


class Players:
    def __init__(self, *_players):
        self.__players = {}
        self.add(_players)

    @property
    def players(self) -> dict:
        return self.__players

    def add(self, *_players):
        for _player in _players:
            if isinstance(_player, Player):
                self.players[_player.token] = _player
                # _player.ship.add(GLOBALS.SHIPS)

    def newPlayer(self, _token: str, _username: str, _color: tuple) -> Player:
        _player = Player(_token=_token, _username=_username, _color=_color)
        self.add(_player)

        return _player

    def __getitem__(self, _token) -> Player:
        return self.__players.get(_token, None)


class Display:
    def __init__(self, _token: str, _index: int):
        self.__token = _token
        self.__name = f"Astro-Assault-{_index}"
        self.__players = {}

    @property
    def name(self):
        return self.__name

    @property
    def token(self):
        return self.__token

    @property
    def players(self):
        return self.__players

    @property
    def count(self):
        return len(self.players.values())

    def addPlayer(self, _player: "Player"):
        self.__players[_player.token] = _player


class Displays:
    def __init__(self):
        self.__displays = {}

    @property
    def displays(self) -> list[Display]:
        return list(self.__displays.values())

    @property
    def count(self):
        return len(self.displays)

    def add(self, _token, _display: Display):
        self.__displays[_token] = _display
        return _display

    def new(self, _token):
        self.__displays[_token] = Display(_token=_token, _index=self.count + 1)
        self.sockSend(
            _event="post_connect",
            _data={"name": self.__displays[_token].name},
            _token=_token
        )
        return self.__displays[_token]

    def remove(self, _token):
        self.__displays.pop(_token, None)

    def sockSend(self, _event, _data, _token):
        Server.SOCK.send(_event=_event, _data=_data, _to=_token, _namespace="/game")

    def triggerUpdate(self, _sock_data, _player_token):
        _player: Player = Server.PLAYERS[_player_token]
        _display: Display = _player.display
        self.sockSend(_event="trigger_update", _data=_sock_data, _token=_display.token)

    def movementUpdate(self, _sock_data, _player_token):
        _player: Player = Server.PLAYERS[_player_token]
        _display: Display = _player.display
        self.sockSend(_event="movement_update", _data=_sock_data, _token=_display.token)

    def joinPlayer(self, _player: Player):
        """
        state:
            0 - no displays
            1 - joined
            2 - full
        """
        returnState = 0

        if self.count:
            returnState = 2
            for _display in self.displays:
                if _display.count < 5:  # max play per display is 5
                    self.sockSend(
                        _event="new_ship",
                        _data={
                            "username": _player.username,
                            "color": _player.color,
                            "token": _player.token
                        },
                        _token=_display.token
                    )
                    _display.addPlayer(_player)
                    _player.display = _display
                    returnState = 1
                    break

        return returnState

    def playerConnect(self, _player_token: str):
        _player: Player = Server.PLAYERS[_player_token]
        _player.connect()
        _display: Display = _player.display
        self.sockSend(_event="player_connect", _data={"token": _player_token}, _token=_display.token)

    def playerDisconnect(self, _player_token: str):
        _player: Player = Server.PLAYERS[_player_token]
        _player.disconnect()
        _display: Display = _player.display
        self.sockSend(_event="player_disconnect", _data={"token": _player_token}, _token=_display.token)

    def __getitem__(self, _token):
        return self.__displays[_token]
