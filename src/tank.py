from __future__ import annotations

import math
from typing import Optional

import pygame

import constants
from caches import animation_cache
from cannonballs import (
    Cannonball,
    Cannonball105mm,
    Cannonball60mm,
    Cannonball80mm,
    CannonballType,
)
from collidable import Collidable
from context import instance
from draw import Drawable
from explotion import Explosion
from player import Player


class Tank(Drawable, Collidable):
    """
    This class represents a tank in the game,
    It has functionalities to draw it,
    detect collisions and shoot a cannonball in a specific direction and speed
    """

    player: Player
    color: pygame.Color | str
    position: pygame.Vector2
    shoot_velocity: float  # m/s
    shoot_angle: float  # rad //
    actual: int  # bala seleccionada
    available: dict[int, int]
    life: int
    is_alive: bool

    def __init__(
        self, color: pygame.Color | str, position: pygame.Vector2, player: Player
    ):
        self.player = player
        self.color = color
        self.position = position
        self.shoot_angle = 3.0 * math.pi / 4.0  # rad
        self.shoot_velocity = 145  # m/s
        self.actual = CannonballType.MM60
        self.available = player.ammunition
        self.is_alive = True
        self.life = 100
        self.animacion_fuego = Explosion(
            self.position, animation_cache["fire"], (50, 50), loop=True
        )
        self.available[0] = 0
        self.available[1] = 0
        self.available[3] = 0

    def collides_with(
        self, point: pygame.Vector2, validation_distance: float = 0
    ) -> bool:
        """
        This function is responsible for checking if the tank was hit by the
        cannonball returned True or False as appropriate
        """
        if ((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2) ** (
            1 / 2
        ) <= validation_distance:
            return True
        return False

    def shoot(self) -> Optional[Cannonball]:
        """
        This function calculates the directions to fire the projectile,
        and calculates the position of the projectile after firing.
        It also creates and returns the Cannonball object with these attributes.
        """
        v_x = self.shoot_velocity * math.cos(self.shoot_angle)
        # the -1 is since in this system the vertical coordinates are inverted
        v_y = -1 * self.shoot_velocity * math.sin(self.shoot_angle)

        start_velocity = pygame.Vector2(v_x, v_y)

        if self.actual == CannonballType.MM60:
            if self.available[0] > 0:
                self.available[0] = self.available[0] - 1
                new_x = self.position.x + (10 + constants.TANK_RADIO) * math.cos(
                    self.shoot_angle
                )
                new_y = self.position.y - (10 + constants.TANK_RADIO) * math.sin(
                    self.shoot_angle
                )

                start_point = pygame.Vector2(new_x, new_y)

                return Cannonball60mm(start_point, start_velocity)
        elif self.actual == CannonballType.MM80:
            if self.available[1] > 0:
                self.available[1] = self.available[1] - 1
                new_x = self.position.x + (20 + constants.TANK_RADIO) * math.cos(
                    self.shoot_angle
                )
                new_y = self.position.y - (20 + constants.TANK_RADIO) * math.sin(
                    self.shoot_angle
                )

                start_point = pygame.Vector2(new_x, new_y)
                return Cannonball80mm(start_point, start_velocity)
        elif self.actual == CannonballType.MM105:
            if self.available[2] > 0:
                self.available[2] = self.available[2] - 1
                new_x = self.position.x + (30 + constants.TANK_RADIO) * math.cos(
                    self.shoot_angle
                )
                new_y = self.position.y - (30 + constants.TANK_RADIO) * math.sin(
                    self.shoot_angle
                )

                start_point = pygame.Vector2(new_x, new_y)
                return Cannonball105mm(start_point, start_velocity)
        return None

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function is responsible for drawing the tank and updates the
        position of the tank gun according to its angle. Additionally, if mode
        is activated developer draws the hitbox
        """
        if not self.is_alive:
            self.color = "#232323"
            self.animacion_fuego.draw(screen)
            self.animacion_fuego.tick(1.0 / instance.fps)

        if constants.DEVELOPMENT_MODE:
            pygame.draw.circle(
                screen,
                "yellow",
                (self.position.x, self.position.y),
                constants.TANK_RADIO,
            )
        cannon_angle_x = math.cos(self.shoot_angle)
        cannon_angle_y = math.sin(self.shoot_angle)
        cannon_x = self.position.x + 20 * cannon_angle_x
        cannon_y = self.position.y - 20 * cannon_angle_y
        muzzle_x = cannon_x + 5 * cannon_angle_x
        muzzle_y = cannon_y - 5 * cannon_angle_y

        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.position.x - 5, self.position.y - 2, 10, 7),
        )
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.position.x - 12.5,
                self.position.y + 5,
                25,
                10,
            ),
        )
        pygame.draw.rect(
            screen,
            constants.GRAY,
            pygame.Rect(
                self.position.x - 12.5,
                self.position.y + 15,
                25,
                4,
            ),
        )

        for i in range(6):
            pygame.draw.circle(
                screen,
                constants.BLACK,
                (
                    self.position.x - 12 + 5 * i,
                    self.position.y + 18,
                ),
                3,
            )

        # cannon
        pygame.draw.line(
            screen,
            self.color,
            (self.position.x, self.position.y),
            (cannon_x, cannon_y),
            4,
        )
        pygame.draw.line(
            screen, self.color, (cannon_x, cannon_y), (muzzle_x, muzzle_y), 6
        )
