import math
import pygame
import constants
from random import randint

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
        self.shoot_angle = 90
        self.shoot_velocity = 0

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
