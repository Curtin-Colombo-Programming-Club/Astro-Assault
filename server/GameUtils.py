import datetime
import math
import random
from server import GLOBALS
import pygame


class _Sprite(pygame.sprite.Sprite):
class _Sprite(pygame.sprite.Sprite):
    def __init__(self, _x, _y):
        super().__init__()
        self._im = pygame.surface.Surface((100, 100))
        self._imc = self._im
        self._rect = self._im.get_rect()
        super().__init__()
        self._im = pygame.surface.Surface((100, 100))
        self._imc = self._im
        self._rect = self._im.get_rect()
        self.rect.center = (_x, _y)
        self._angle = 0
        self._speed = 0
        self._angle = 0
        self._speed = 0

    @property
    def image(self):
        self._imc = pygame.transform.rotate(self._im, self.angle)
        return self._imc
        self._imc = pygame.transform.rotate(self._im, self.angle)
        return self._imc

    @property
    def rect(self):
        self._rect = self._imc.get_rect(center=self.center)
        return self._rect
        self._rect = self._imc.get_rect(center=self.center)
        return self._rect

    @property
    def center(self):
        return self._rect.center
        return self._rect.center

    @property
    def x(self):
        return self._rect.centerx
        return self._rect.centerx

    @property
    def y(self):
        return self.rect.centery

    @property
    def angle(self):
        return self._angle

    def update(self, *args, **kwargs):
        _x = self.x + self._speed * math.sin(math.radians(self.angle))
        _y = self.y + self._speed * math.cos(math.radians(self.angle))

        if _x < 0:
            _x = GLOBALS.WIDTH
        if _x > GLOBALS.WIDTH:
            _x = 0
        if _y < 0:
            _y = GLOBALS.HEIGHT
        if _y > GLOBALS.HEIGHT:
            _y = 0

        self._rect.center = (_x, _y)


class Laser(_Sprite):
    def __init__(self, _x, _y, _angle, _ship, _index=1):
        super().__init__(_x=_x, _y=_y)
        self._ship = _ship
        self._im = pygame.transform.scale(
            _im := pygame.image.load(f"server/images/laser{_index}.svg"),
            (_im.get_width() * 2 / 3 * GLOBALS.W_RATIO, _im.get_height() * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )
        self._imc = self._im
        self._angle = _angle
        self._speed = -10 + _ship.speed
        self._seconds = 0

    @property
    def ship(self):
        return self._ship

    def update(self, *args, **kwargs):
        super().update()
        self._seconds += 1 / GLOBALS.FPS

        if self._seconds > 3:
            self.kill()


class Missile(_Sprite):
    def __init__(self, _x, _y, _angle, _ship):
        super().__init__(_x=_x, _y=_y)
        self._ship = _ship
        self._im = pygame.transform.scale(
            _im := pygame.image.load(f"server/images/missile.svg"),
            (_im.get_width() * GLOBALS.C_RATIO * GLOBALS.W_RATIO, _im.get_height() * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )
        self._imc = self._im
        self._angle = _angle
        self._speed = -8 + _ship.speed
        self._seconds = 0

    @property
    def ship(self):
        return self._ship

    def update(self, *args, **kwargs):
        super().update()
        self._seconds += 1 / GLOBALS.FPS

        if self._seconds > 3:
            self.kill()


class Lasers(pygame.sprite.Group):
    def __init__(self, *_lasers):
        super().__init__(_lasers)

    @property
    def lasers(self) -> list:
        return self.sprites()

    def add(self, *_lasers):
        for _laser in _lasers:
            if isinstance(_laser, Laser):
                super().add(_laser)

    def newLaser(self, _ship) -> Laser:
        _x_off = 30 * GLOBALS.C_RATIO * GLOBALS.W_RATIO * (-1 if _ship.primary_chamber == "left" else 1)
        _y_off = 10 * GLOBALS.C_RATIO * GLOBALS.H_RATIO
        _offset_theta = math.atan2(-_y_off, _x_off)
        _r = math.sqrt(_x_off ** 2 + _y_off ** 2)
        _ship_angle = -_ship.angle

        # print("new l", _ship_angle,  _offset_theta)

        _laser = Laser(_x=_ship.x + (_r * math.cos(math.radians(_ship_angle) + _offset_theta)),
                       _y=_ship.y + (_r * math.sin(math.radians(_ship_angle) + _offset_theta)),
                       _angle=_ship.angle,
                       _ship=_ship,
                       _index=2 if _ship.primary_3_counter == 3 else 1)
        self.add(_laser)

        return _laser


class Missiles(pygame.sprite.Group):
    def __init__(self, *_missiles):
        super().__init__(_missiles)

    @property
    def missiles(self) -> list:
        return self.sprites()

    def add(self, *_missiles):
        for _missile in _missiles:
            if isinstance(_missile, Missile):
                super().add(_missile)

    def newMissile(self, _ship) -> Missile:
        _x_off = 35 * GLOBALS.C_RATIO * GLOBALS.W_RATIO * (-1 if _ship.secondary_chamber == "left" else 1)
        _y_off = 10 * GLOBALS.C_RATIO * GLOBALS.H_RATIO
        _offset_theta = math.atan2(-_y_off, _x_off)
        _r = math.sqrt(_x_off ** 2 + _y_off ** 2)
        _ship_angle = -_ship.angle

        # print("new l", _ship_angle,  _offset_theta)

        _missile = Missile(_x=_ship.x + (_r * math.cos(math.radians(_ship_angle) + _offset_theta)),
                           _y=_ship.y + (_r * math.sin(math.radians(_ship_angle) + _offset_theta)),
                           _angle=_ship.angle,
                           _ship=_ship)
        self.add(_missile)

        return _missile


class Ship(_Sprite):
    def __init__(self, _x, _y, _player):
        super().__init__(_x, _y)
        self._player = _player
        self._im = pygame.transform.scale(
            _im := pygame.image.load("server/images/ship.svg"),
            (200 * GLOBALS.C_RATIO * GLOBALS.W_RATIO, 200 * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )

        print(self._im.get_height())
        self._imc = self._im
        self._primary_chamber = "right"
        self._secondary_chamber = "right"
        self._primary_3_counter = 0

    @property
    def speed(self):
        return self._speed

    @property
    def primary_chamber(self):
        return self._primary_chamber

    @property
    def secondary_chamber(self):
        return self._secondary_chamber

    @property
    def primary_3_counter(self):
        return self._primary_3_counter

    def sockMoveUpdate(self, _dx, _dy):
        self._angle -= 60 * ((GLOBALS.W_RATIO + GLOBALS.H_RATIO) / 2) * (1 / GLOBALS.FPS) * _dx
        self._speed += 3 * GLOBALS.W_RATIO * (1 / GLOBALS.FPS) * _dy

        if abs(self._angle) > 180:
            self._angle = -(self._angle / abs(self._angle) * 360 - self._angle)

        # speed constrains
        _maxSpeed = 12 * GLOBALS.W_RATIO
        _drag = 1 * GLOBALS.W_RATIO
        # drag
        if abs(self._speed) >= _drag:
            self._speed -= _drag * (1 / GLOBALS.FPS) * self._speed / abs(self._speed)
        elif abs(self._speed) >= _drag / 2:
            self._speed -= (_drag / 2) * (1 / GLOBALS.FPS) * self._speed / abs(self._speed)
        # max speed
        if abs(self._speed) > _maxSpeed:
            self._speed = _maxSpeed * self._speed / abs(self._speed)

    def sockTriggerUpdate(self, _n):
        if _n == 2:
            self._primary_3_counter += 1
            GLOBALS.LASERS.newLaser(_ship=self)
            if self._primary_3_counter == 3:
                self._primary_3_counter = 0
                self._primary_chamber = "left" if self.primary_chamber == "right" else "right"
        elif _n == 3:
            print("adding missile")
            GLOBALS.MISSILES.newMissile(_ship=self)
            self._secondary_chamber = "left" if self._secondary_chamber == "right" else "right"


class Player:
    def __init__(self, _token: str):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()
        self.__token = _token
        self.__ship = Ship(_x=random.randint(0, GLOBALS.WIDTH), _y=random.randint(0, GLOBALS.HEIGHT), _player=self)
        self.__ship = Ship(_x=random.randint(0, GLOBALS.WIDTH), _y=random.randint(0, GLOBALS.HEIGHT), _player=self)

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
        _player = Player(_token)
        _player = Player(_token)
        self.add(_player)

        print(_player.ship.center)

        return _player

    def __getitem__(self, _token) -> Player:
        return self.__players.get(_token, None)
