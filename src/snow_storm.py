from random import randint
from typing import Optional

import pygame

import constants
from draw import Drawable
from context import instance
from wind import Wind


class SnowStorm(Drawable):
    """
    This class is responsible for adding small particles to the map, changing
    depending on the biome.
    """

    snowflakes: list[pygame.Vector2]
    wind: Optional[Wind]
    gravity: float

    def __init__(self, storm_color: str, wind: Optional[Wind], gravity: float):
        """
        Initialize the class by loading the images and setting the initial
        position of the particles.
        """
        self.snowflakes = []
        for _ in range(constants.SNOWFLAKES):
            self.add_random_snowflake()
        self.wind = wind
        self.storm_color = storm_color
        self.gravity = gravity

    def add_random_snowflake(self):
        """Add a snowflake at a random valid position within the map"""
        self.snowflakes.append(
            pygame.Vector2(
                randint(0, instance.windows_size[0]),
                randint(0, instance.windows_size[1]),
            )
        )

    def tick(self, dt: float) -> None:
        """
        This function is responsible for advancing the snowflakes and
        repositioning them if they have gone off the map.
        """
        for snowflake in self.snowflakes:
            snowflake.y += constants.X_SPEED * self.gravity * dt  # gravity

            # Corner case down
            if snowflake.y > (instance.windows_size[1]):
                snowflake.y -= instance.windows_size[1]

            # Corner case sides
            if snowflake.x > instance.windows_size[0]:
                snowflake.x -= instance.windows_size[0]
            elif snowflake.x < 0:
                snowflake.x += instance.windows_size[0]

            if self.wind is not None:
                snowflake.x += constants.X_WIND_SPEED * self.wind.velocity * dt

    def draw_snowflakes(self, screen: pygame.surface.Surface):
        """This function draws each snowflake present in the list of snowflakes."""
        for snowflake in self.snowflakes:
            pygame.draw.circle(screen, self.storm_color, snowflake, 2)

    def draw(self, screen: pygame.surface.Surface) -> None:
        """This function only draws the particles on the screen"""
        self.draw_snowflakes(screen)
