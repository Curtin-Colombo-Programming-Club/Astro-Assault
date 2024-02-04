import datetime
import math
import random
from server import GLOBALS
import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.__im = pygame.transform.scale(pygame.image.load("server/images/ship.png"), (200, 300))
        self.__rect = self.__im.get_rect()
        self.rect.center = (_x, _y)
        self.__angle = 0
        self.__vel = [0, 0]

        print(_x, _y)

    @property
    def image(self):
        return self.__im

    @property
    def rect(self):
        return self.__rect

    @property
    def center(self):
        return self.rect.center

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property
    def angle(self):
        theta = math.atan2(self.y, self.x)
        self.__angle = math.degrees(theta)
        return self.__angle

    def dVelocity(self, _dx, _dy):
        # print(_dx, _dy)
        ...

    def update(self, *args, **kwargs):
        super().update(args, kwargs)


class Player:
    def __init__(self, _token:str, _ship: Ship):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()
        self.__token = _token
        self.__ship = _ship

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
    def ship(self):
        return self.__ship

    def connect(self):
        self.__online = True
        self.__lastOnline = datetime.datetime.now()

    def disconnect(self):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()

    def __str__(self):
        return (f"Player(\n"
                f"\ttoken      : {self.token}\n"
                f"\tonline     : {self.online}\n"
                f"\tlast online: {self.lastOnline}\n"
                ")")


class Players(pygame.sprite.Group):
    def __init__(self, *_players):
        self.__players = {}
        self.add(_players)
        _ships = [_player.ship for _player in _players]
        
        super().__init__(_ships)

    @property
    def players(self) -> dict:
        return self.__players

    def add(self, *_players):
        for _player in _players:
            if isinstance(_player, Player):
                self.players[_player.token] = _player
                super().add(_player.ship)

    def newPlayer(self, _token: str) -> Player:
        _player = Player(_token, Ship(random.randint(0, GLOBALS.WIDTH), random.randint(0, GLOBALS.HEIGHT)))
        self.add(_player)

        print(_player.ship.center)

        return _player

    def __getitem__(self, _token) -> Player:
        return self.__players.get(_token, None)
