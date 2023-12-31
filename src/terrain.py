import random
from random import randint

import pygame

import constants
from collidable import Collidable
from context import instance
from draw import Drawable


class Terrain(Drawable, Collidable):
    """
    This class represents the terrain, allowing it to be generated and drawn randomly
    for each game session. It also checks collisions with the terrain.
    """

    size: tuple[int, int]
    ground_lines: list[int]
    new_ground_lines: list[list[float]]
    falling: list[list[tuple[float, float]]]

    def generate_terrain(self, mountains: int, valley: int):
        """
        This function generates random terrain by dividing it into segments,
        where deformations (using the mountain and valley functions) are added.
        Mountains and valleys are generated within specific segments and are
        determined randomly.
        """
        deformations = mountains + valley
        segment_size = self.size[0] // deformations
        segment_start = 0
        segment_end = segment_size
        deformations_index = [*range(deformations)]
        random.shuffle(deformations_index)
        valleys = deformations_index[0:valley]

        for i in range(deformations):
            start = segment_start + randint(3 * (-segment_size // 4), segment_size // 3)
            end = segment_end + randint(-segment_size // 3, 3 * (segment_size // 4))

            start = max(start, 0)
            end = min(end, self.size[0] - 1)

            if i in valleys:
                deep = randint((self.size[1] // 4) // 4, (self.size[1] // 4) // 2)
                self.valley(start, end, deep)
            else:
                max_height = (self.size[1] - constants.SEA_LEVEL) // 2
                height = randint(max_height // 4, max_height)
                self.mountain(start, end, height)

            segment_start += segment_size
            segment_end += segment_size

    def mountain(self, i: int, j: int, height: int):
        """
        This function creates mountains from a start point to an end point,
        including their midpoint to make them symmetrical. The first for loop
        adds values to the ground_lines list that increase up to the midpoint,
        while the second for loop adds values that decrease from the midpoint
        to the end point.
        """
        m = (i + j) // 2
        original_max = (m - i - 1) ** 2
        multiplier = height / original_max

        for k in range(i, m):
            self.ground_lines[k] += int(((k - i) ** 2) * multiplier)

        for k in range(m, j):
            self.ground_lines[k] += int(((j - k) ** 2) * multiplier)

    def valley(self, start: int, end: int, depth: int):
        """
        This function creates valleys from a start point to an end point, including
        their midpoint to make them symmetrical. The first for loop adds values to
        the ground_lines list that decrease up to the midpoint, while the second
        for loop adds values that increase from the midpoint to the end point.
        """
        m = (start + end) // 2
        original_max = (m - start - 1) ** 2
        multiplier = depth / original_max

        for i in range(start, m):
            self.ground_lines[i] -= int(((i - start) ** 2) * multiplier)

        for j in range(m, end):
            self.ground_lines[j] -= int(((j - end) ** 2) * multiplier)

    def __init__(
        self, size: tuple[int, int], mountains: int, valleys: int, colors: list[str]
    ):
        """
        Initializes the Terrain object with the specified size, number of mountains
        and valleys, and color layers for rendering.
        """
        self.size = size
        self.ground_lines = [constants.SEA_LEVEL] * (self.size[0])

        if constants.MAP_SEED != -1:
            random.seed(constants.MAP_SEED)

        # Generate the terrain
        self.generate_terrain(mountains, valleys)
        random.seed()

        self.terrain_layer_colors = colors
        self.layers_num = len(colors)

        self.new_ground_lines = []
        self.falling = []
        self.is_falling = False
        self.falling_speed = 0
        # Transform to a new model
        for height in self.ground_lines:
            self.new_ground_lines.append([height / self.layers_num] * self.layers_num)
            self.falling.append([(0, 0)] * self.layers_num)

    def tick(self, dt: float, gravity: float):
        """
        This method is responsible for the calculations for each frame of the
        fall of the ground.
        """
        self.is_falling = False
        self.falling_speed += gravity * dt
        for i, layers in enumerate(self.falling):
            top_point = None
            for j, layer in enumerate(layers):
                if layer == (0, 0):
                    continue
                self.is_falling = True
                top_point = instance.map_size[1] - layer[0]
                layers[j] = (layer[0] + self.falling_speed * dt, layer[1])

            if top_point is not None and top_point < self.ground_lines[i]:
                for j, layer in enumerate(layers):
                    self.new_ground_lines[i][j] += layer[1]
                    self.falling[i][j] = (0, 0)

    def draw_falling(self, screen: pygame.surface.Surface) -> None:
        """
        This method is responsible for each frame when the ground is destroyed
        and a part of it needs to fall.
        """
        for i, layers in enumerate(self.falling):
            for layer, color in zip(layers, self.terrain_layer_colors):
                if layer == (0, 0):
                    continue
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        i,
                        layer[0],
                        1,
                        layer[1],
                    ),
                )

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Draws different layers of the terrain using different colors and heights,
        simulating the substrate of the ground.
        """
        for i, layers in enumerate(self.new_ground_lines):
            latest_height = 0
            for layer, color in zip(layers, self.terrain_layer_colors):
                if layer != 0:
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(
                            i,
                            self.size[1] - latest_height - layer,
                            1,
                            layer + 1,
                        ),
                    )
                latest_height += layer
        self.draw_falling(screen)

    def collides_with(
        self, point: pygame.Vector2, validation_distance: float = 0
    ) -> bool:
        """
        Checks if the position of the projectile collides with the terrain,
        comparing the terrain height at the corresponding line with the cannon's
        coordinate.
        """
        line_index = int(point.x)

        return point.y > (self.size[1] - self.ground_lines[line_index])
