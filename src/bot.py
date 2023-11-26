from __future__ import annotations

import math
import random

import pygame

from cannonballs import (
    CannonballType,
)
from player import Player
from tank import Tank

class Bot(Tank):
    def __init__(
        self, color: pygame.Color | str, position: pygame.Vector2, player: Player
    ):
        super().__init__(color, position, player)

    def random_shoot(self, position2: pygame.Vector2, gravity):
        option = random.randint(0, 1)
        if option == 0:
            self.selection_cannonball()
            delta_x = position2.x - self.position.x
            delta_y = position2.y - self.position.y
            d = pygame.math.Vector2(delta_x, delta_y).length()
            angle = abs(
                pygame.math.Vector2(delta_x, delta_y).angle_to(
                    pygame.math.Vector2(1, 0)
                )
            )
            angle = math.radians(angle)
            if delta_y != 0:
                velocity = (d * gravity) / (2 * abs(delta_y))
            else:
                velocity = 0
            self.shoot_angle = angle
            self.shoot_velocity = velocity
        if option == 1:
            self.selection_cannonball()
            self.shoot_angle = math.radians(random.randint(10, 180))
            self.shoot_velocity = random.randint(20, 100)

    def selection_cannonball(self):
        if self.available[0] == 0:
            self.actual = CannonballType.MM80
        if self.available[1] == 0:
            self.actual = CannonballType.MM105
        if self.available[2] == 0:
            if self.available[1] != 0:
                self.actual = CannonballType.MM80
            if self.available[0] != 0:
                self.actual = CannonballType.MM60

    def buy_cannonballs(self):
        buy = True
        while buy:
            cannon = random.randint(1, 3)
            if self.player.money < 1000:
                buy = False
            if cannon == 1 and self.player.money >= 1000:
                self.player.money = self.player.money - 1000
                self.available[0] = self.available[0] + 1

            if cannon == 2 and self.player.money >= 2500:
                self.player.money = self.player.money - 2500
                self.available[1] = self.available[1] + 1

            if cannon == 3 and self.player.money >= 4000:
                self.player.money = self.player.money - 4000
                self.available[2] = self.available[2] + 1
