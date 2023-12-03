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
    """
    This class is a subclass of Tank, it represents a tank bot that can fire projectiles randomly,
    select projectiles based on their availability and purchase new projectiles on its own.
    """

    def __init__(
        self, color: pygame.Color | str, position: pygame.Vector2, player: Player
    ):
        super().__init__(color, position, player)

    def random_shoot(self, position2: pygame.Vector2, gravity):
        """
        This method simulates a cannon shot in the game.
        Depending on the random option, it calculates the angle and speed of the projectile differently
        (with a formula depending on the position of other tank or 100% random).
        Use selection_cannonball for projectile type selection.
        """
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
        """
        This method chooses the type of projectile based on the availability of different types.
        Prioritize shells with zero availability,
        and if options are available, select a specific shell based on priority order.
        """
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
        """
        This method simulates a process of randomly purchasing cannon shells,
        where the type of shell and the player's amount of money determine whether the purchase is made and what type
        of shell is added to the inventory.
        """
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
