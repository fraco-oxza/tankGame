import random
from random import randint

import pygame

import constants
from collidable import Collidable
from draw import Drawable


class Terrain(Drawable, Collidable):
    """
    Esta clase representa al terreno, permite generar y dibujarlo aleatoriamente
    por cada partida, además comprueba colisiones con este
    """

    size: tuple[int, int]
    ground_lines: list[int]
    new_ground_lines: list[list[float]]

    def generate_terrain(self, mountains: int, valley: int):
        """
        Esta función genera el terreno aleatorio,  dividiendolo en segmentos,
        donde se agregan deformaciones  (usando las funciones montañas y
        valles).
        Las montañas y valles se generan dentro de segmentos específicos y se
        determinan aleatoriamente.
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
        Esta función montañas va desde un punto de inicio, hasta un punto
        final, incluyendo su punto medio para que sean simétricas. El primer
        for incluye en la lista ground_lines los valores que van creciendo
        hasta el punto medio, mientras que el segundo for los valores que van
        decreciendo desde el punto medio hasta el punto final
        """
        m = (i + j) // 2
        original_max = (m - i - 1) ** 2
        multiplier = (height / original_max) / constants.TERRAIN_LINE_WIDTH

        for k in range(i, m):
            self.ground_lines[k // constants.TERRAIN_LINE_WIDTH] += int(
                ((k - i) ** 2) * multiplier
            )

        for k in range(m, j):
            self.ground_lines[k // constants.TERRAIN_LINE_WIDTH] += int(
                ((j - k) ** 2) * multiplier
            )

    def valley(self, inicio: int, fin: int, profundidad: int):
        """
        Esta función valles desde un punto de inicio, hasta un punto final,
        incluyendo su punto medio para que sean simétricos. El primer for
        incluye en la lista ground_lines los valores que van decreciendo hasta
        el punto medio, mientras que el segundo for los valores que van
        creciendo desde el punto medio hasta el final
        """
        m = (inicio + fin) // 2
        original_max = (m - inicio - 1) ** 2
        multiplier = (profundidad / original_max) / constants.TERRAIN_LINE_WIDTH

        for i in range(inicio, m):
            self.ground_lines[i // constants.TERRAIN_LINE_WIDTH] -= int(
                ((i - inicio) ** 2) * multiplier
            )

        for j in range(m, fin):
            self.ground_lines[j // constants.TERRAIN_LINE_WIDTH] -= int(
                ((j - fin) ** 2) * multiplier
            )

    def __init__(
        self, size: tuple[int, int], mountains: int, valleys: int, colors: list[str]
    ):
        self.size = size
        self.ground_lines = [constants.SEA_LEVEL] * (
            self.size[0] // constants.TERRAIN_LINE_WIDTH
        )

        if constants.MAP_SEED != -1:
            random.seed(constants.MAP_SEED)

        # Se genero el terreno
        self.generate_terrain(mountains, valleys)
        random.seed()

        self.terrain_layer_colors = colors
        self.layers_num = len(colors)

        self.new_ground_lines = []
        # Transformar a nuevo modelo
        for height in self.ground_lines:
            self.new_ground_lines.append([height / self.layers_num] * self.layers_num)

        print(self.new_ground_lines.__len__(), self.ground_lines.__len__())

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Esta función dibuja diferentes capas del terreno utilizando diferentes
        colores y alturas, esto permite simular el sustrato del suelo
        """
        for i, layers in enumerate(self.new_ground_lines):
            latest_height = -5
            for layer, color in zip(layers, self.terrain_layer_colors):
                if layer != 0:
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(
                            i * constants.TERRAIN_LINE_WIDTH,
                            self.size[1] - latest_height - layer - 3,
                            constants.TERRAIN_LINE_WIDTH,
                            layer + 3,
                        ),
                    )
                latest_height += layer

    def collides_with(self, point: pygame.Vector2) -> bool:
        """
        Esta función se encarga de verificar si la posición de la bala colisionó
        o no con el terreno, esto lo hace comparando la altura del terreno en la
        línea correspondiente al punto con la coordenada del cañón
        """
        line_index = int(point.x) // constants.TERRAIN_LINE_WIDTH

        return point.y > (self.size[1] - self.ground_lines[line_index])
