import datetime
import math
import random
import time
import GLOBALS
import pygame
from typing import Self
from Game.Utils import *


class Player:
    def __init__(self, _token: str, _username: str, _color: tuple):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()

        self.__token = _token
        self.__username = _username

        self.__ship: Ship = GLOBALS.SHIPS.newShip(_player=self, _color=_color)
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
            self.__ship.add(GLOBALS.SHIPS)

    def disconnect(self):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()
        self.__ship.kill()

    def sockSend(self, _event, _data):
        GLOBALS.SOCK.send(_event=_event, _data=_data, _to=self.token)

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
