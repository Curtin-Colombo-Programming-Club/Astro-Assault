import datetime
import math
import random
import time
from server import GLOBALS
import pygame
from typing import Self


class _StaticSprite(pygame.sprite.Sprite):
    """
    A class representing a static sprite that could be altered manually.

    Attributes:
        __img_path: A string representing the file path of the sprite's image.
        __w_factor: A float representing the width factor for scaling the image.
        __h_factor: A float representing the height factor for scaling the image.
        _im: A pygame surface representing the scaled image.
        _imc: A copy of the sprite's image with the current rotation applied.
        _rect: A pygame Rect representing the sprite's bounding rectangle.
        _angle: A float representing the angle of rotation of the sprite.

    Parameters:
        _img_path: A string representing the file path of the sprite's image.
        _center: A tuple representing the center coordinates of the sprite.
        _w_factor: A float representing the width factor for scaling the image (default is 1).
        _h_factor: A float representing the height factor for scaling the image (default is 1).
        _angle: A float representing the initial angle of rotation of the sprite (default is 0).

    Methods:
        image: A property that returns the rotated image of the sprite.
        rect: A property that returns the bounding rectangle of the sprite.
        center: A property that returns the center coordinates of the sprite.
        x: A property that returns the x-coordinate of the sprite's center.
        y: A property that returns the y-coordinate of the sprite's center.
        angle: A property that returns the current angle of rotation of the sprite.
        _on_screen_resize: A method to adjust the sprite's image when the screen is resized.
    """
    def __init__(self, _img_path, _center, _w_factor=1, _h_factor=1, _angle=0):
        super().__init__()
        self.__img_path = _img_path
        self.__w_factor = _w_factor
        self.__h_factor = _h_factor
        self._im = pygame.transform.scale(
            _im := pygame.image.load(_img_path),
            (
                _im.get_width() * _w_factor * GLOBALS.C_RATIO * GLOBALS.W_RATIO,
                _im.get_height() * _h_factor * GLOBALS.C_RATIO * GLOBALS.H_RATIO
            )
        )
        self._imc = self._im
        self._rect = self._im.get_rect()
        self.rect.center = _center
        self._angle = 0

    @property
    def image(self) -> pygame.image:
        """
        Get the rotated image of the sprite.

        Returns:
            A pygame Surface object representing the rotated image of the sprite.
        """
        self._imc = pygame.transform.rotate(self._im, self.angle)
        return self._imc

    @property
    def rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the sprite.

        Returns:
            A pygame Rect object representing the bounding rectangle of the sprite.
        """
        self._rect = self._imc.get_rect(center=self.center)
        return self._rect

    @property
    def center(self) -> tuple:
        """
        Get the center coordinates of the sprite.

        Returns:
            A tuple representing the center coordinates (x, y) of the sprite.
        """
        return tuple(self._rect.center)

    @property
    def x(self) -> int | float:
        """
        Get the x-coordinate of the sprite's center.

        Returns:
            An integer or float representing the x-coordinate of the sprite's center.
        """
        return self._rect.centerx

    @property
    def y(self) -> int | float:
        """
        Get the y-coordinate of the sprite's center.

        Returns:
            An integer or float representing the y-coordinate of the sprite's center.
        """
        return self.rect.centery

    @property
    def angle(self) -> int | float:
        """
        Get the current angle of rotation of the sprite.

        Returns:
            A float representing the current angle of rotation of the sprite.
        """
        return self._angle

    def _on_screen_resize(self) -> None:
        """
        Adjust the sprite's image when the screen is resized.

        Parameters:
            None

        Returns:
            None
        """
        self._im = pygame.transform.scale(
            _im := pygame.image.load(self.__img_path),
            (_im.get_width() * self.__w_factor * GLOBALS.C_RATIO * GLOBALS.W_RATIO,
             _im.get_height() * self.__h_factor * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )

        self.rect.center = (self.x * GLOBALS.W_RATIO / GLOBALS.p_W_RATIO, self.y * GLOBALS.H_RATIO / GLOBALS.p_H_RATIO)


class _DynamicSprite(_StaticSprite):
    def __init__(self, _img_path, _center, _w_factor=1, _h_factor=1, _angle=0):
        super().__init__(_img_path=_img_path, _center=_center, _w_factor=_w_factor, _h_factor=_h_factor, _angle=_angle)
        self._force = 0
        self._angle = 0
        self._d_angle = 0
        self._mass = 0
        self._acceleration = 0
        self._velocity = [0, 0]

    @property
    def mass(self) -> int | float:
        return self._mass

    @property
    def speed(self) -> int | float:
        return math.sqrt(self._velocity[0] ** 2 + self._velocity[1] ** 2)

    @property
    def velocity(self) -> tuple:
        return tuple(self._velocity)

    def update(self, *args, **kwargs):
        self._angle -= self._d_angle / _fps if (_fps := GLOBALS.FPS) > 0 else 1
        if abs(self._angle) > 180:
            self._angle = -(self._angle / abs(self._angle) * 360 - self._angle)

        _time = 1 / GLOBALS.TICK_RATE

        _add_speed = self._acceleration * _time

        self._velocity[0] += _add_speed * math.sin(math.radians(self.angle))
        self._velocity[1] += _add_speed * math.cos(math.radians(self.angle))

        _x = self.x + self.velocity[0] * _time * GLOBALS.W_RATIO
        _y = self.y + self.velocity[1] * _time * GLOBALS.H_RATIO

        if _x < 0:
            _x = GLOBALS.WIDTH
        if _x > GLOBALS.WIDTH:
            _x = 0
        if _y < 0:
            _y = GLOBALS.HEIGHT
        if _y > GLOBALS.HEIGHT:
            _y = 0

        self._rect.center = (_x, _y)


class _Sprite(pygame.sprite.Sprite):
    def __init__(self, _x, _y):
        super().__init__()
        self._im = pygame.surface.Surface((100, 100))
        self._imc = self._im
        self._rect = self._im.get_rect()
        self.rect.center = (_x, _y)
        self._force = 0
        self._angle = 0
        self._d_angle = 0
        self._mass = 0
        self._acceleration = 0
        self._velocity = [0, 0]

    @property
    def image(self):
        self._imc = pygame.transform.rotate(self._im, self.angle)
        return self._imc

    @property
    def rect(self):
        self._rect = self._imc.get_rect(center=self.center)
        return self._rect

    @property
    def center(self):
        return tuple(self._rect.center)

    @property
    def x(self):
        return self._rect.centerx

    @property
    def y(self):
        return self.rect.centery

    @property
    def force(self):
        return self._force

    @property
    def angle(self):
        return self._angle

    @property
    def mass(self):
        return self._mass

    @property
    def speed(self):
        return math.sqrt(self._velocity[0] ** 2 + self._velocity[1] ** 2)

    @property
    def velocity(self):
        return tuple(self._velocity)

    def update(self, *args, **kwargs):
        self._angle -= self._d_angle / _fps if (_fps := GLOBALS.FPS) > 0 else 1
        if abs(self._angle) > 180:
            self._angle = -(self._angle / abs(self._angle) * 360 - self._angle)

        """
        s = u .t + 0.5 . a . t**2
        """

        _t = 1 / GLOBALS.TICK_RATE

        # initial velocity
        _u = self._velocity

        _u_t_x = _u[0] * _t
        _u_t_y = _u[1] * _t

        # final velocity
        self._velocity[0] += self._acceleration * math.sin(math.radians(self.angle)) * _t
        self._velocity[1] += self._acceleration * math.cos(math.radians(self.angle)) * _t

        _s_x = self._velocity[0] * _t
        _s_y = self._velocity[1] * _t

        print(_s_x, _s_y, self.speed)

        _x = self.x + _s_x
        _y = self.y + _s_y

        if _x < 0:
            _x = GLOBALS.WIDTH
        if _x > GLOBALS.WIDTH:
            _x = 0
        if _y < 0:
            _y = GLOBALS.HEIGHT
        if _y > GLOBALS.HEIGHT:
            _y = 0

        self._rect.center = (_x, _y)

    def _on_screen_resize(self, _img, _wf, _hf):
        self._im = pygame.transform.scale(
            _im := pygame.image.load(_img),
            (_im.get_width() * _wf * GLOBALS.C_RATIO * GLOBALS.W_RATIO,
             _im.get_height() * _hf * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )

        self.rect.center = (self.x * GLOBALS.W_RATIO / GLOBALS.p_W_RATIO, self.y * GLOBALS.H_RATIO / GLOBALS.p_H_RATIO)


class _Group(pygame.sprite.Group):
    """
    A custom sprite group class inherited from pygame.sprite.Group.

    This class extends the functionality of the pygame.sprite.Group class by adding custom methods.

    Parameters:
        *_sprites: Optional initial sprites to add to the group.

    Methods:
        updatex: Updates and renders all sprites in the group on the specified screen.
        on_screen_resize: Calls the on_screen_resize method for all sprites in the group.
    """

    def __init__(self, *_sprites):
        super().__init__(_sprites)

    def updatex(self, *args, **kwargs):
        """
        Update and render all sprites in the group on the specified screen.

        Parameters:
            *_args: Optional arguments passed to the update method of each sprite.
            **kwargs: Keyword arguments passed to the update method of each sprite.
                "_screen": The pygame surface on which to render the sprites.
                "special_flags": Optional special flags for blit operations.

        Returns:
            None
        """
        _screen = kwargs["_screen"]
        _special_flags = kwargs.get("special_flags", 0)
        for sprite in self.sprites():
            sprite.update(_screen=_screen)
            _screen.blit(sprite.image, sprite.rect, None, _special_flags)

    def on_screen_resize(self):
        """
        Call the on_screen_resize method for all sprites in the group.

        Parameters:
            None

        Returns:
            None
        """
        for sprite in self.sprites():
            sprite.on_screen_resize()


class Laser(_Sprite):
    def __init__(self, _x, _y, _angle, _ship: _Sprite, _index=1):
        super().__init__(_x=_x, _y=_y)
        self._ship = _ship
        self._index = _index
        self._im = pygame.transform.scale(
            _im := pygame.image.load(f"server/images/laser{_index}.svg"),
            (_im.get_width() * 4 * GLOBALS.C_RATIO * GLOBALS.W_RATIO,
             _im.get_height() * 3 * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )
        self._imc = self._im
        self._angle = _angle
        _speed = -1000
        self._velocity = [_speed * math.sin(math.radians(_angle)) + _ship.velocity[0],
                          _speed * math.cos(math.radians(_angle)) + _ship.velocity[1]]
        self._seconds = 0

    @property
    def ship(self):
        return self._ship

    def update(self, *args, **kwargs):
        super().update()
        self._seconds += 1 / GLOBALS.FPS

        if self._seconds > 1:
            self.kill()

    def on_screen_resize(self):
        self._on_screen_resize(_img=f"server/images/laser{self._index}.svg", _wf=4, _hf=3)


class Missile(_Sprite):
    def __init__(self, _x, _y, _angle, _ship):
        super().__init__(_x=_x, _y=_y)
        self._ship = _ship
        self._im = pygame.transform.scale(
            _im := pygame.image.load(f"server/images/missile.svg"),
            (_im.get_width() * 2 * GLOBALS.C_RATIO * GLOBALS.W_RATIO,
             _im.get_height() * 2 * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )
        self._imc = self._im
        self._angle = _angle
        _speed = -300
        self._velocity = [_speed * math.sin(math.radians(_angle)) + _ship.velocity[0],
                          _speed * math.cos(math.radians(_angle)) + _ship.velocity[1]]
        self._acceleration = -600
        self._seconds = 0

    @property
    def ship(self):
        return self._ship

    def update(self, *args, **kwargs):
        super().update()
        self._seconds += 1 / GLOBALS.FPS

        if self._seconds > 2:
            self.kill()

    def on_screen_resize(self):
        self._on_screen_resize(_img=f"server/images/missile.svg", _wf=2, _hf=2)


class Lasers(_Group):
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
        _x_off = 31 * GLOBALS.C_RATIO * GLOBALS.W_RATIO * (-1 if _ship.primary_chamber == "left" else 1)
        _y_off = 11 * GLOBALS.C_RATIO * GLOBALS.H_RATIO
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


class Missiles(_Group):
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
        _x_off = 36 * GLOBALS.C_RATIO * GLOBALS.W_RATIO * (-1 if _ship.secondary_chamber == "left" else 1)
        _y_off = -11 * GLOBALS.C_RATIO * GLOBALS.H_RATIO
        _offset_theta = math.atan2(_y_off, _x_off)
        _r = math.sqrt(_x_off ** 2 + _y_off ** 2)
        _ship_angle = -_ship.angle

        # print("new l", _ship_angle,  _offset_theta)

        _missile = Missile(_x=_ship.x + (_r * math.cos(math.radians(_ship_angle) + _offset_theta)),
                           _y=_ship.y + (_r * math.sin(math.radians(_ship_angle) + _offset_theta)),
                           _angle=_ship.angle,
                           _ship=_ship)
        self.add(_missile)

        return _missile


class LaserHit(_Sprite):
    def __init__(self, _x, _y, _angle):
        super().__init__(_x, _y)
        self._im = pygame.transform.scale(
            _im := pygame.image.load(f"server/images/laser_hit.svg").convert_alpha(),
            (_im.get_width() * 2 * GLOBALS.C_RATIO * GLOBALS.W_RATIO,
             _im.get_height() * 2 * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )
        self._imc = self._im
        self._angle = _angle
        self._timer = 0
        self._speed = -1

    def update(self, *args, **kwargs):
        super().update()
        self._timer += 1 / GLOBALS.FPS
        self._im.set_alpha(int(255 - 255 * self._timer))
        if self._timer >= 1:
            self.kill()

    def on_screen_resize(self):
        self._on_screen_resize(_img=f"server/images/laser_hit.svg", _wf=2, _hf=2)


class MissileHit(_Sprite):
    ...


class HitMarks(_Group):
    def __init__(self, *_hit_marks):
        super().__init__(_hit_marks)

    def add(self, *_hit_marks):
        for _hit_mark in _hit_marks:
            if isinstance(_hit_mark, (LaserHit, MissileHit)):
                super().add(_hit_mark)


class AfterBurner(_Sprite):
    def __init__(self, _ship, _side):
        super().__init__(_ship.x, _ship.y)

        self._im = pygame.transform.scale(
            _im := pygame.image.load(f"server/images/after_burner.png"),
            (_im.get_width() * GLOBALS.C_RATIO * GLOBALS.W_RATIO, _im.get_height() * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )
        self._imc = self._im
        self._side = _side
        self._angle = _ship.angle
        self._stretch = 0

        self.__pos(_ship=_ship)

    @property
    def image(self):
        self._imc = pygame.transform.rotate(
            pygame.transform.scale(
                self._im,
                (self._im.get_width(), self._im.get_height() * self._stretch)
            ),
            self.angle
        )
        return self._imc

    def __pos(self, _ship):
        _x_off = 56 * GLOBALS.C_RATIO * GLOBALS.W_RATIO * (-1 if self._side == "left" else 1)
        _y_off = 82 * GLOBALS.C_RATIO * GLOBALS.H_RATIO
        _offset_theta = math.atan2(_y_off, _x_off)
        _r = math.sqrt(_x_off ** 2 + _y_off ** 2)
        _ship_angle = -_ship.angle

        # print("new l", _ship_angle,  _offset_theta)

        self._rect.center = (_ship.x + (_r * math.cos(math.radians(_ship_angle) + _offset_theta)) - math.sin(
            math.radians(_ship_angle)) * self._im.get_height() * GLOBALS.W_RATIO * GLOBALS.C_RATIO * self._stretch / 2,
                             _ship.y + (_r * math.sin(math.radians(_ship_angle) + _offset_theta)) + math.cos(
                                 math.radians(
                                     _ship_angle)) * self._im.get_height() * GLOBALS.H_RATIO * GLOBALS.C_RATIO * self._stretch / 2)

    def update(self, *args, **kwargs):
        _ship = kwargs["_ship"]
        self._angle = _ship.angle
        _force = abs(_ship.force) if _ship.force <= 0 else 0
        self._stretch = 3 * _force / GLOBALS.UNIT_FORCE

        self.__pos(_ship)

    def on_screen_resize(self):
        self._on_screen_resize(_img=f"server/images/after_burner.png", _wf=1, _hf=1)


class Ship(_Sprite):
    def __init__(self, _x, _y, _player):
        super().__init__(_x, _y)
        self._player = _player
        self._im = pygame.transform.scale(
            _im := pygame.image.load("server/images/ship.svg"),
            (200 * GLOBALS.C_RATIO * GLOBALS.W_RATIO, 200 * GLOBALS.C_RATIO * GLOBALS.H_RATIO)
        )
        self._imc = self._im

        self._mass = 1000

        self._flames = pygame.sprite.Group()

        self._flames.add(AfterBurner(_ship=self, _side="right"))
        self._flames.add(AfterBurner(_ship=self, _side="left"))

        self._primary_chamber = "right"
        self._primary_3_counter = 0

        self._secondary_chamber = "right"
        self._secondary_timer = 0
        self._secondary_timing = False

        self._health = 100
        self._dead = False

        self._last_movement_update = 0

    @property
    def player(self):
        return self._player

    @property
    def primary_chamber(self):
        return self._primary_chamber

    @property
    def secondary_chamber(self):
        return self._secondary_chamber

    @property
    def primary_3_counter(self):
        return self._primary_3_counter

    @property
    def dead(self):
        return self._dead

    def update(self, *args, **kwargs):
        _screen = kwargs["_screen"]

        pygame.draw.rect(_screen, (0, 0, 255), self.rect, 2)
        _username = pygame.transform.scale(
            _im := pygame.font.Font(None, 40).render(self.player.username, True, (255, 255, 255)),
            (_im.get_width() * GLOBALS.W_RATIO * GLOBALS.C_RATIO, _im.get_height() * GLOBALS.H_RATIO * GLOBALS.C_RATIO))
        _screen.blit(_username, (
        self.x - _username.get_width() / 2, self.rect.top - _username.get_height() - 10 * GLOBALS.H_RATIO))
        super().update()
        self._flames.update(_ship=self)
        self._flames.draw(_screen)
        # timers
        if self._secondary_timing:
            self._secondary_timer += 1 / GLOBALS.FPS
            if self._secondary_timer >= 5:
                self._secondary_timer = 0
                self._secondary_timing = False

    def dealDamage(self, _type: int):
        if _type == 1:
            self._health -= 1
        elif _type == 2:
            self._health -= 10

        if self._health <= 0:
            self.kill()
            self._dead = True
            self._player.died()

    def respawn(self):
        if self._dead:
            self._health = 100
            self._dead = False
            self._rect.center = (random.randint(0, GLOBALS.WIDTH), random.randint(0, GLOBALS.HEIGHT))
            self.add(GLOBALS.SHIPS)

    def sockMoveUpdate(self, _dx, _dy):
        # angle change
        self._d_angle = 100 * _dx

        # acceleration
        """
        acceleration calculation
        =================
        F = uf . f%
        F = m . a  →  a = F / m
        
        ∴ acceleration = (unit force . force factor) / mass    
        """
        _unit_force = GLOBALS.UNIT_FORCE
        _force_factor = _dy if _dy <= 0 else _dy / 2
        self._force = _unit_force * _force_factor

        self._acceleration = self._force / self.mass
        # -----

        # speed constrains
        """_maxSpeed = GLOBALS.MAX_SPEED
        print(self.velocity)

        # max speed
        if abs(self.speed) > _maxSpeed:
            _angle = math.degrees(math.atan2(-self._velocity[0], -self._velocity[1]))
            self._velocity[0] = - _maxSpeed * math.sin(math.radians(_angle))
            self._velocity[1] = - _maxSpeed * math.cos(math.radians(_angle))"""

    def sockTriggerUpdate(self, _n):
        if _n == 2:
            self._primary_3_counter += 1
            GLOBALS.LASERS.newLaser(_ship=self)
            if self._primary_3_counter == 3:
                self._primary_3_counter = 0
                self._primary_chamber = "left" if self.primary_chamber == "right" else "right"
        elif _n == 3:
            if self._secondary_timer == 0:
                GLOBALS.MISSILES.newMissile(_ship=self)
                self._secondary_chamber = "left" if self._secondary_chamber == "right" else "right"
                if self._secondary_chamber == "right":
                    self._secondary_timing = True

    def on_screen_resize(self):
        self._on_screen_resize(_img="server/images/ship.svg", _wf=1, _hf=1)

    def __str__(self):
        return (f"Ship(\n"
                f"\tPos: {self.center}\n"
                f"\tHealth: {self._health}\n"
                f")")


class Ships(_Group):
    def __init__(self, *_ships):
        super().__init__(_ships)

    @property
    def ships(self):
        return self.sprites()

    def add(self, *_ships):
        for _ship in _ships:
            if isinstance(_ships, Ship):
                super().add(_ship)

    def newShip(self, _player) -> Ship:
        # _ship = Ship(_player=_player, _x=random.randint(0, GLOBALS.WIDTH), _y=random.randint(0, GLOBALS.HEIGHT))
        _ship = Ship(_player=_player, _x=400, _y=0)
        self.add(_ship)

        return _ship


class Player:
    def __init__(self, _token: str):
        self.__online = False
        self.__lastOnline = datetime.datetime.now()

        self.__token = _token
        self.__username = "user-name"

        self.__ship: Ship = GLOBALS.SHIPS.newShip(_player=self)
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

    def newPlayer(self, _token: str) -> Player:
        _player = Player(_token)
        self.add(_player)

        return _player

    def __getitem__(self, _token) -> Player:
        return self.__players.get(_token, None)


def check_collision(_TSprite: Laser | Missile, _TSprite2: Ship) -> bool:
    if _TSprite.ship != _TSprite2 and _TSprite.rect.colliderect(_TSprite2.rect):
        try:
            _tc = _TSprite.center
            _a = \
            _TSprite2.image.get_at((_TSprite.center[0] - _TSprite2.rect.left, _TSprite.center[1] - _TSprite2.rect.top))[
                3]
            if _a:
                _hm = LaserHit(_x=_tc[0], _y=_tc[1], _angle=_TSprite.angle)
                GLOBALS.HIT_MARKS.add(_hm)
                _TSprite2.dealDamage(1 if isinstance(_TSprite, Laser) else 2 if isinstance(_TSprite, Missile) else 0)
                if _TSprite2.dead:
                    _TSprite.ship.player.killed()
                return True
        except IndexError:
            pass
    else:
        return False
