import math
import random
from random import randint

import pygame

import constants
from draw import Drawable


class SnowStorm(Drawable):
    """
    This class is responsible for adding small particles to the map, changing depending on the biome.
    """

    snowflakes: list[pygame.Vector2]
    wind: float
    wind_target: float

    def __init__(self, storm_color: str):
        self.snowflakes = []
        for _ in range(constants.SNOWFLAKES):
            self.add_random_snowflake()
        self.wind = 0
        self.wind_target = 0
        self.storm_color = storm_color

    def add_random_snowflake(self):
        """Add a snowflake at a random valid position within the map"""
        self.snowflakes.append(
            pygame.Vector2(
                randint(0, constants.WINDOWS_SIZE[0]),
                randint(0, constants.WINDOWS_SIZE[1]),
            )
        )

    def tick(self, dt: float) -> None:
        """
        This function is responsible for advancing the snowflakes and
        repositioning them if they have gone off the map.
        """
        for snowflake in self.snowflakes:
            snowflake.y += constants.GRAVITY / 10.0  # gravity

            # Corner case down
            if snowflake.y > (constants.WINDOWS_SIZE[1]):
                snowflake.y -= constants.WINDOWS_SIZE[1]

            # Corner case sides
            if snowflake.x > constants.WINDOWS_SIZE[0]:
                snowflake.x -= constants.WINDOWS_SIZE[0]
            elif snowflake.x < 0:
                snowflake.x += constants.WINDOWS_SIZE[0]

            if abs(self.wind - self.wind_target) < 1e-9:
                self.wind_target = (random.random() - 0.5) * 10.0

            wind_diff = self.wind_target - self.wind
            self.wind += math.tanh(wind_diff) * dt * 1e-5

            snowflake.x += self.wind

    def draw_snowflakes(self, screen: pygame.surface.Surface):
        """This function draws each snowflake present in the list of snowflakes."""
        for snowflake in self.snowflakes:
            pygame.draw.circle(screen, self.storm_color, snowflake, 1)

    def draw(self, screen: pygame.surface.Surface) -> None:
        """This function only draws the particles on the screen"""
        self.draw_snowflakes(screen)
