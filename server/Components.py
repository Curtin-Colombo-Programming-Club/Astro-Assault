import os
import math
import pygame
import random
from typing import Self
import Server
import numpy as np


class _StaticComponent:

    def __init__(self, _center, _angle=0):
        """
        Initializes a _StaticSprite object.

        Args:
            _angle (int | float): The initial angle of rotation of the sprite.
        """

        self._center = _center
        self._angle = _angle

    @property
    def center(self) -> tuple:
        """
        Get the center coordinates of the sprite.

        Returns:
            A tuple representing the center coordinates (x, y) of the sprite.
        """
        return tuple(self._center)

    @property
    def x(self) -> int | float:
        """
        Get the x-coordinate of the sprite's center.

        Returns:
            An integer or float representing the x-coordinate of the sprite's center.
        """
        return self.center[0]

    @property
    def y(self) -> int | float:
        """
        Get the y-coordinate of the sprite's center.

        Returns:
            An integer or float representing the y-coordinate of the sprite's center.
        """
        return self.center[1]

    @property
    def angle(self) -> int | float:
        """
        Get the current angle of rotation of the sprite.

        Returns:
            A float representing the current angle of rotation of the sprite.
        """
        return self._angle

    def __dict__(self):
        return {
            "x": self.x,
            "y": self.y
        }


class _DynamicComponent(_StaticComponent):
    def __init__(self, _center, _angle=0):
        super().__init__(_center=_center, _angle=_angle)
        self._force = Server.FORCES.newForce(_color=(0, 0, 255), _text="Fe")
        self._drag_force = Server.FORCES.newForce(_color=(255, 0, 0), _text="Fd")
        self._area = 0.001
        self._d_angle = 0
        self._mass = 1
        self._acceleration = 0
        self._velocity = [0, 0]

    @property
    def force(self) -> "Force":
        """
        Getter for the force property.

        Returns:
            An int or float
        """
        return self._force

    @property
    def mass(self) -> int | float:
        """
        Getter for the mass property.
        """
        return self._mass

    @property
    def speed(self) -> int | float:
        """
        Getter for the speed property.
        """
        return math.sqrt(self._velocity[0] ** 2 + self._velocity[1] ** 2)

    @property
    def velocity(self) -> tuple:
        """
        Getter for the velocity property.
        """
        return tuple(self._velocity)

    def update(self, *args, **kwargs) -> Self:

        # angle change
        self._angle -= self._d_angle / _tr if (_tr := Server.TICK_RATE) > 0 else 1
        if abs(self._angle) > 180:
            self._angle = -(self._angle / abs(self._angle) * 360 - self._angle)

        # velocity and displacement
        """
        Calculations
        ============
        Final Velocity
        --------------
        v = u + a . t

        Displacement
        ------------
        Since updates are called at each computing elapsed time period (1/tick-rate)
        We break the velocity and time planes into segments and find the area in it
        ∴ s = 0.5 (u + v) . t  ←  trapezium rule

        Drag Force
        ----------
        Fd = 0.5 ⋅ ρ ⋅ A ⋅ v^2 . Cd 

        Resultant Force
        --------------
        Fr = Fe + Fd

        Acceleration
        ------------
        ∴ acceleration = Fr / mass  
        """

        # Drag Force
        self._drag_force.value = 0.5 * Server.DENSITY * self._area * (self.speed ** 2) * Server.DRAG_FACTOR
        self._drag_force.angle = math.degrees(math.atan2(-self.velocity[0], -self.velocity[1]))
        # print("@update", self._drag_force.angle,self._drag_force.value, self._force.value, self.speed)

        # Resultant Force
        _Rx = self._force.value * math.sin(math.radians(self.force.angle)) + self._drag_force.value * math.sin(
            math.radians(self._drag_force.angle))
        _Ry = self._force.value * math.cos(math.radians(self.force.angle)) + self._drag_force.value * math.cos(
            math.radians(self._drag_force.angle))
        _Fr = math.sqrt(_Rx ** 2 + _Ry ** 2)

        # Resultant Angle
        _angle = math.atan2(_Rx, _Ry)

        # Acceleration
        self._acceleration = _Fr / self.mass

        # time
        _t = 1 / Server.TICK_RATE

        # initial velocity
        _u = self.velocity

        # final velocity
        self._velocity[0] += self._acceleration * math.sin(_angle) * _t
        self._velocity[1] += self._acceleration * math.cos(_angle) * _t
        _v = self.velocity

        _s_x = 0.5 * (_u[0] + _v[0]) * _t
        _s_y = 0.5 * (_u[1] + _v[1]) * _t

        # Update position
        _x = self.x + _s_x
        _y = self.y + _s_y

        if _x < 0:
            _x = Server.WIDTH
        if _x > Server.WIDTH:
            _x = 0
        if _y < 0:
            _y = Server.HEIGHT
        if _y > Server.HEIGHT:
            _y = 0

        self._center = (_x, _y)

        # returns self
        return self


class _Group:

    def __init__(self):
        self.__components = np.array([], dtype=object)
        self.__update = np.vectorize(lambda _comp: _comp.update())

    @property
    def components(self) -> np.array:
        return self.__components

    def add(self, _component: _DynamicComponent | _StaticComponent):
        if _component not in self.components:
            self.__components = np.append(self.components, _component)

    def remove(self, _component):
        self.__components = self.components[self.components != _component]

    def update(self, *args, **kwargs):
        try:
            self.__update(self.components)
        except Exception as e:
            pass


class Laser(_DynamicComponent):

    def __init__(self, _x, _y, _angle, _ship: "Ship", _index=1):
        """
        Initializes a Laser object.

        Args:
            _x (int | float): The x-coordinate of the laser's starting position.
            _y (int | float): The y-coordinate of the laser's starting position.
            _angle (int | float): The angle at which the laser is fired.
            _ship (_DynamicSprite): The ship from which the laser is fired.
            _index (int, optional): The index of the laser image. Defaults to 1.
        """

        super().__init__(_center=(_x, _y),
                         _angle=_angle)
        self._ship = _ship
        self._index = _index

        self._area = 0.001

        _speed = -1000
        self._velocity = [_speed * math.sin(math.radians(_angle)) + _ship.velocity[0],
                          _speed * math.cos(math.radians(_angle)) + _ship.velocity[1]]
        self._seconds = 0

    @property
    def ship(self) -> "Ship":
        """
        Getter for the ship property.
        """
        return self._ship

    def update(self, *args, **kwargs) -> Self:
        """
        Updates the position and state of the laser.
        """
        super().update()
        self._seconds += 1 / Server.TICK_RATE

        if self._seconds > 1:
            self.kill()

        return self


class Missile(_DynamicComponent):
    def __init__(self, _x, _y, _angle, _ship: "Ship"):
        """
        Initializes a Missile object.

        Args:
            _x (int | float): The x-coordinate of the missile's starting position.
            _y (int | float): The y-coordinate of the missile's starting position.
            _angle (int | float): The angle at which the missile is fired.
            _ship (Ship): The ship from which the missile is fired.
        """

        super().__init__(_center=(_x, _y),
                         _angle=_angle)
        self._ship = _ship

        _speed = -300
        self._velocity = [_speed * math.sin(math.radians(_angle)) + _ship.velocity[0],
                          _speed * math.cos(math.radians(_angle)) + _ship.velocity[1]]
        self._force.value = -1000
        self._force.angle = _angle
        self._seconds = 0

    @property
    def ship(self) -> "Ship":
        """
        Getter for the ship property.
        """
        return self._ship

    def update(self, *args, **kwargs) -> Self:
        """
        Updates the position and state of the missile.

        Returns:
            Missile: The updated Missile object.
        """
        super().update()
        self._seconds += 1 / Server.TICK_RATE

        if self._seconds > 2:
            self.kill()

        return self


class Lasers(_Group):
    """
    A class representing a group of lasers.

    Inherits from _Group.

    Attributes:
        lasers (list[Laser]): List of lasers in the group.

    Methods:
        lasers: Getter for the lasers property.
        add(*_lasers): Adds lasers to the group.
        newLaser(_ship: "Ship"): Creates a new laser fired from a ship and adds it to the group.

    """

    def __init__(self):
        super().__init__()

    def newLaser(self, _ship: "Ship") -> Laser:
        """
        Creates a new laser fired from a ship and adds it to the group.

        Args:
            _ship (Ship): The ship from which the laser is fired.

        Returns:
            Laser: The newly created laser object.
        """
        _x_off = 31 * (-1 if _ship.primary_chamber == "left" else 1)
        _y_off = 11
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
    def __init__(self):
        super().__init__()

    def newMissile(self, _ship) -> Missile:
        """
        Creates a new missile fired from a ship and adds it to the group.

        Args:
            _ship (Ship): The ship from which the missile is fired.

        Returns:
            Missile: The newly created missile object.
        """
        _x_off = 36 * (-1 if _ship.secondary_chamber == "left" else 1)
        _y_off = -11
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


class Force:
    def __init__(self, _color, _name: str):
        self.__name = _name
        self.__start = [0, 0]
        self.__value = 0
        self.__angle = 0

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, _val):
        if isinstance(_val, (int, float)):
            self.__value = _val
        else:
            raise ValueError

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, _val):
        if isinstance(_val, (int, float)):
            self.__angle = _val
        else:
            raise ValueError

    def update(self, _val):
        self.__value = _val


class Forces:
    def __init__(self):
        self.__fls: list[Force] = []

    def add(self, _force: Force):
        self.__fls.append(_force)

        return self

    def newForce(self, _color, _text: str):
        _fa = Force(_color=_color, _name=_text)
        self.add(_force=_fa)

        return _fa


class Ship(_DynamicComponent):
    def __init__(self, _x, _y, _player, _color=(0, 0, 255)):
        super().__init__(_center=(_x, _y))

        self.__color = _color

        self._player = _player

        self._mass = 1000
        self._area = 250000

        self._primary_chamber = "right"
        self._primary_3_counter = 0

        self._secondary_chamber = "right"
        self._secondary_timer = 0
        self._secondary_timing = False

        self._health = 100
        self._dead = False

        self._last_movement_update = 0

        Server.FORCES.newForce(_color=(0, 0, 255), _text="Fe")

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
        # args
        _screen = kwargs["_screen"]

        # updating force object
        self.force.angle = self.angle
        self.force.start = self.center

        # timers
        if self._secondary_timing:
            self._secondary_timer += 1 / Server.TICK_RATE
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
            self._rect.center = (random.randint(0, Server.WIDTH), random.randint(0, Server.HEIGHT))
            self.add(Server.SHIPS)

    def sockMoveUpdate(self, _dx, _dy):
        # angle change
        self._d_angle = 100 * _dx

        # acceleration
        """
        acceleration calculation
        =================
        F = uf . f%
        F = m . a  →  a = F / m  
        """
        _unit_force = Server.UNIT_FORCE
        _force_factor = _dy if _dy <= 0 else _dy / 2
        self._force.value = _unit_force * _force_factor
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
            Server.LASERS.newLaser(_ship=self)
            if self._primary_3_counter == 3:
                self._primary_3_counter = 0
                self._primary_chamber = "left" if self.primary_chamber == "right" else "right"
        elif _n == 3:
            if self._secondary_timer == 0:
                Server.MISSILES.newMissile(_ship=self)
                self._secondary_chamber = "left" if self._secondary_chamber == "right" else "right"
                if self._secondary_chamber == "right":
                    self._secondary_timing = True

    def __dict__(self):
        _d = super().__dict__()
        _d["token"] = self.player.token

        return _d

    def __str__(self):
        return (f"Ship(\n"
                f"\tPos: {self.center}\n"
                f"\tHealth: {self._health}\n"
                f")")


class Ships(_Group):
    def __init__(self):
        super().__init__()

    def newShip(self, _player, _color) -> Ship:
        # _ship = Ship(_player=_player, _x=random.randint(0, GLOBALS.WIDTH), _y=random.randint(0, GLOBALS.HEIGHT))
        _ship = Ship(_player=_player, _x=400, _y=0, _color=_color)
        self.add(_ship)

        return _ship

    def __iter__(self):
        for _c in self.components:
            yield dict(_c)


"""def check_collision(_TSprite: Laser | Missile, _TSprite2: Ship) -> bool:
    if _TSprite.ship != _TSprite2 and _TSprite.rect.colliderect(_TSprite2.rect):
        try:
            _tc = _TSprite.center
            _a = \
                _TSprite2.image.get_at(
                    (_TSprite.center[0] - _TSprite2.rect.left, _TSprite.center[1] - _TSprite2.rect.top))[
                    3]
            if _a:
                _hm = LaserHit(_x=_tc[0], _y=_tc[1], _angle=_TSprite.angle)
                Server.HIT_MARKS.add(_hm)
                _TSprite2.dealDamage(1 if isinstance(_TSprite, Laser) else 2 if isinstance(_TSprite, Missile) else 0)
                if _TSprite2.dead:
                    _TSprite.ship.player.killed()
                return True
        except IndexError:
            pass
    else:
        return False
"""
