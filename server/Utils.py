import datetime
import math
import random
import time
import pygame
from typing import Self
import Server
from Server.components import *


class Player:
    def __init__(self, _token: str, _username: str, _color: tuple):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()

        self.__token = _token
        self.__username = _username

        self.__ship: Ship = Server.SHIPS.newShip(_player=self, _color=_color)
        self.__kills = 0
        self.__deaths = 0

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

    @property
    def ship(self):
        return self.__ship

    def connect(self):
        self.__online = True
        self.__lastOnline = datetime.datetime.now()
        if not self.ship.dead:
            Server.SHIPS.add(self.ship)

    def disconnect(self):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()
        Server.SHIPS.remove(self.ship)

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
    def __init__(self, _token: str):
        self.__token = _token

    @property
    def token(self):
        return self.__token


class Displays:
    def __init__(self):
        self.__displays = {}

    @property
    def displays(self):
        return self.__displays

    def add(self, _token, _display: Display):
        self.__displays[_token] = _display
        return _display

    def remove(self, _token):
        self.__displays.pop(_token, None)

    def sockSend(self, _event, _data, _token):
        Server.SOCK.send(_event=_event, _data=_data, _to=_token, _namespace="/game")

    def triggerUpdate(self, _data):
        [self.sockSend(_event=f"trigger_update", _data=_data, _token=_display.token) for _display in self.__displays.values()]

    def movementUpdate(self, _data):
        [self.sockSend(_event=f"movement_update", _data=_data, _token=_display.token) for _display in self.__displays.values()]

    def newComponent(self, _component, _data):
        [self.sockSend(_event=f"new_{_component}", _data=_data, _token=_display.token) for _display in self.__displays.values()]

    def __getitem__(self, _token):
        return self.__displays[_token]

