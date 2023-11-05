import pygame
import random
import math
from player import Player
from tank import Tank
from cannonballs import (
    CannonballType,
)

class Bot(Tank):
    def __init__(
        self, color: pygame.Color | str, position: pygame.Vector2, player: Player
    ):
        super().__init__(color, position, player)

    def random_shoot(self, position2: pygame.Vector2):
        self.selection_cannonball()
        delta_x = position2.x - self.position.x
        delta_y = position2.y - self.position.y
        d = pygame.math.Vector2(delta_x, delta_y).length()
        print("d: ", d)
        angle = abs(pygame.math.Vector2(delta_x, delta_y).angle_to(pygame.math.Vector2(1, 0)))
        angle = math.radians(angle)
        print("angle: ", angle)
        if delta_y != 0:
            velocity = (d * 9.8) / (2 * abs(delta_y))
            print("velocity: ", velocity)
        else:
            velocity = 0
            print("velocity: ", velocity)
        self.shoot_angle = angle
        self.shoot_velocity = velocity

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
