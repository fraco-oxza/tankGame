import math
import pygame

from random import randint

from player import Player
from tank import Tank


class Bot(Tank):
    def __init__(
        self, color: pygame.Color | str, position: pygame.Vector2, player: Player
    ):
        super().__init__(color, position, player)

    def random_shoot(self, position2: pygame.Vector2):
        """"
        distance = (
            (position2.x - self.position.x) ** 2 + (position2.y - self.position.y) ** 2
        ) ** (1 / 2)
        theta = math.atan2(position2.y - self.position.y, position2.x - self.position.x)
        angle = math.degrees(theta)
        velocity = distance / (
            1
            / (2 * math.cos(theta))
            * (position2.y - self.position.y)
            / (position2.x - self.position.x)
            * math.sin(theta)
        )
        """
        self.shoot_angle = randint(10, 180)
        self.shoot_velocity = randint(50, 200)
