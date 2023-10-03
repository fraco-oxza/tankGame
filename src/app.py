from __future__ import annotations

import math
import os
import random
import sys
from abc import abstractmethod
from random import randint
from typing import Optional

import pygame
from pygame.color import Color
from pygame.font import Font

import constants


# variable global, para mostrar pantalla de seleccion de bala


def resource_path(relative_path: str):
    """
    This function is responsible for loading the resources from the resources
    folder. It is conditional, since when the program is packaged in an
    executable, the folder directory changes and other directories must be
    used. When the _MEIPASS environment variable is set, it means it is
    packaged.
    """
    path = getattr(
        sys, "_MEIPASS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
    )
    return os.path.join(path, "resources", relative_path)


class Collidable:
    """
    Clase que contiene un método abstracto que se pasa a través de Override a
    otras clases, donde se espera haya colisiones.
    """

    @abstractmethod
    def collides_with(self, point: pygame.Vector2) -> bool:
        """
        Esta funcion es la encargada de decir si self, es decir la instancia
        colisionable ya colisionó con un punto. Debe retornar True en caso de
        que colisione y False en otro caso.
        """
        raise NotImplementedError


class Drawable:
    """
    Clase que contiene un método abstracto que se pasa a través de Override a
    otras clases, donde se crearán elementos visuales que serán mostrados por
    medio de la interfaz.
    """

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Esta funcion se encarga de dibujar una instancia, a traves de la screen
        que se le pasa en los parametros. No se debe hacer el pygame.display.flip
        """
        raise NotImplementedError


class SnowStorm(Drawable):
    snowflakes: list[pygame.Vector2]
    wind: float
    wind_target: float

    def __init__(self):
        self.snowflakes = []
        for _ in range(constants.SNOWFLAKES):
            self.add_random_snowflake()
        self.wind = 0
        self.wind_target = 0

    def add_random_snowflake(self):
        """Add a snowflake at a random valid position within the map."""
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
            pygame.draw.circle(screen, "#ffffff", snowflake, 1)

    def draw(self, screen: pygame.surface.Surface) -> None:
        self.draw_snowflakes(screen)


class Background(Drawable):
    """
    This class represents the game background, which loads an image and creates
    animations of falling snow with wind.
    """

    sky_image: pygame.Surface

    def __init__(self):
        """Initialize the class by loading the images and creating the snowflakes."""
        image_size = pygame.Vector2(
            constants.WINDOWS_SIZE[0],
            (1.0 / constants.ASPECT_RATIO) * constants.WINDOWS_SIZE[0],
        )
        self.sky_image = pygame.transform.scale(
            pygame.image.load(resource_path("images/sky.jpg")), image_size
        )
        self.sky_rect = self.sky_image.get_rect()

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function is responsible for drawing the background and the
        snowflakes.
        """
        screen.blit(self.sky_image, self.sky_rect.topleft)


class Terrain(Drawable, Collidable):
    """
    Esta clase representa al terreno, permite generar y dibujarlo aleatoriamente
    por cada partida, además comprueba colisiones con este
    """

    size: tuple[int, int]
    ground_lines: list[int]

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
                max_height = self.size[1] - (self.size[1] // 4)
                height = randint(max_height // 4, 3 * (max_height // 4))
                self.mountain(start, end, height)

            segment_start += segment_size
            segment_end += segment_size

    def mountain(self, i: int, j: int, height: int):
        """
        Esta función montañas va desde un punto de inicio, hasta un punto final,
        incluyendo su punto medio para que sean simétricas. El primer for
        incluye en la lista ground_lines los valores que van creciendo hasta el
        punto medio, mientras que el segundo for los valores que van decreciendo
        desde el punto medio hasta el punto final
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

    def __init__(self, size: tuple[int, int], mountains: int, valleys: int):
        self.size = size
        self.ground_lines = [constants.SEA_LEVEL] * (
            self.size[0] // constants.TERRAIN_LINE_WIDTH
        )

        if constants.MAP_SEED != -1:
            random.seed(constants.MAP_SEED)
        self.generate_terrain(mountains, valleys)
        random.seed()

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Esta función dibuja diferentes capas del terreno utilizando diferentes
        colores y alturas, esto permite simular el sustrato del suelo
        """
        for i, line in enumerate(self.ground_lines):
            pygame.draw.rect(
                screen,
                constants.TERRAIN_COLOR,
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    self.size[1] - line,
                    constants.TERRAIN_LINE_WIDTH,
                    line,
                ),
            )

    def collides_with(self, point: pygame.Vector2) -> bool:
        """
        Esta función se encarga de verificar si la posición de la bala colisionó
        o no con el terreno, esto lo hace comparando la altura del terreno en la
        línea correspondiente al punto con la coordenada del cañón
        """
        line_index = int(point.x) // constants.TERRAIN_LINE_WIDTH

        return point.y > (self.size[1] - self.ground_lines[line_index])


class Cannonball(Drawable):
    """
    Esta clase representa una bala de cañón en movimiento, proporciona
    funcionalidades para actualizar su posición, dibujar su trayectoria y
    obtener información.
    """

    position: pygame.Vector2
    velocity: pygame.Vector2
    trajectory: list[pygame.Vector2]
    max_height: int
    max_distance: int
    is_alive: bool

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        self.position = position
        self.velocity = velocity
        self.max_height = sys.maxsize
        self.max_distance = sys.maxsize
        self.is_alive = True
        self.trajectory = []

    def tick(self, dt: float):
        """
        Esta función va actualizando la posición de la bala por cada intervalo
        de tiempo, su propósito es simular el movimiento y comportamiento de la
        parábola que dibuja la bala del cañón
        """
        if self.position.y < self.max_height:
            self.max_height = int(self.position.y)
        self.position += self.velocity * dt
        self.velocity[1] += constants.GRAVITY * dt

        if (
            len(self.trajectory) == 0
            or (
                (self.trajectory[-1].x - self.position.x) ** 2
                + (self.trajectory[-1].y - self.position.y) ** 2
            )
            > 50
        ):
            self.trajectory.append(pygame.Vector2(self.position.x, self.position.y))

    def kill(self):
        """
        Esta función "desactiva" la bala de cañón para indicar qye ya no está en
        uso, para esto elimina el atributo trajectory del objeto y establece el
        estado de vida en False
        """
        del self.trajectory
        self.is_alive = False

    def draw_trajectory(self, screen: pygame.surface.Surface):
        """
        Esta función dibuja la trayectoria de la bala, por cada punto en la
        lista trajectory dibuja un circulo.
        """
        for point in self.trajectory:
            pygame.draw.circle(screen, "#000000", (point.x, point.y), 1)

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        pass

    def get_max_height(self) -> int:
        """
        esta función se encarga de retornar la altura máxima del lanzamiento de
        la bala
        """
        return constants.WINDOWS_SIZE[1] - self.max_height

    def calculate_distance_to(self, tank_position: pygame.Vector2) -> int:
        """
        esta función se encarga de retornar la distancia máxima entre la bala y
        el tanque que la lanzó
        """
        return (
            (self.position.x - tank_position.x) ** 2
            + (self.position.y - tank_position.y) ** 2
        ) ** (1 / 2)


class SelectCannonball(Drawable):
    cannonball60: Cannonball60mm
    cannonball80: Cannonball80mm
    cannonball105: Cannonball105mm
    tank_game: TankGame
    available: list[int]

    def __init__(self, tank_game: TankGame):
        self.font = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 14)
        self.text_cannonball60_info = None
        self.text_cannonball80_info = None
        self.text_cannonball105_info = None
        self.tank_game = tank_game

    @staticmethod
    def selection_screen(screen: pygame.surface):
        transparency = 140
        rect_surface = pygame.Surface((700, 300))
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = (300, 250)
        screen.blit(rect_surface, (rect_x1, rect_y1))

    def draw_cannonball_105_mm(self, screen: pygame.surface):
        position = pygame.Vector2(870, 420)
        pygame.draw.line(
            screen, "gray", position, (position.x + 70, position.y - 70), 20
        )
        pygame.draw.circle(screen, "black", position, 50)

        pygame.draw.line(
            screen,
            "yellow",
            (position.x + 70, position.y - 70),
            (position.x + 80, position.y - 80),
            20,
        )

    def draw_cannonball_80_mm(self, screen: pygame.surface):
        position = pygame.Vector2(630, 380)
        triangle = [
            (position.x, position.y),
            (position.x + 25, position.y - 50),
            (position.x + 50, position.y),
        ]

        pygame.draw.rect(
            screen, constants.DarkGreen, pygame.Rect(position.x, position.y, 50, 75)
        )
        pygame.draw.line(
            screen,
            "yellow",
            (position.x, position.y + 37.5),
            (position.x + 50, position.y + 37.5),
            25,
        )
        pygame.draw.polygon(screen, constants.DarkGreen, triangle)

        pygame.draw.line(
            screen,
            "orange",
            (position.x + 25, position.y + 75),
            (position.x + 25, position.y + 100),
            20,
        )

    def draw_cannonball_60_mm(self, screen: pygame.surface):
        position = pygame.Vector2(420, 370)
        pygame.draw.line(
            screen,
            "#4b5320",
            (position.x, position.y),
            (position.x, position.y + 80),
            40,
        )
        pygame.draw.line(
            screen,
            "#fbb741",
            (position.x, position.y + 60),
            (position.x, position.y + 80),
            40,
        )

    def cannonball_105_mm(self, screen: pygame.surface):
        self.text_cannonball105_info = self.font.render(
            f"Unidades Diponibles: {self.available[2]}",
            True,
            "white",
        )
        screen.blit(self.text_cannonball105_info, pygame.Vector2(790, 520))

    def cannonball_80_mm(self, screen: pygame.surface):
        self.text_cannonball80_info = self.font.render(
            f"Unidades Diponibles: {self.available[1]}",
            True,
            "white",
        )
        screen.blit(self.text_cannonball80_info, pygame.Vector2(570, 520))

    def cannonball_60_mm(self, screen: pygame.surface):
        self.text_cannonball60_info = self.font.render(
            f"Unidades Diponibles: {self.available[0]}",
            True,
            "white",
        )
        screen.blit(self.text_cannonball60_info, pygame.Vector2(350, 520))

    def draw(self, screen: pygame.surface.Surface) -> None:
        self.available = self.tank_game.tanks[self.tank_game.actual_player].available
        self.selection_screen(screen)
        self.cannonball_60_mm(screen)
        self.cannonball_80_mm(screen)
        self.cannonball_105_mm(screen)
        self.draw_cannonball_105_mm(screen)
        self.draw_cannonball_80_mm(screen)
        self.draw_cannonball_60_mm(screen)


class Cannonball105mm(Cannonball):
    damage: int
    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 50
        self.radius_damage = 30
        self.units_available = 3

    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.line(
            screen,
            "gray",
            (self.position.x, self.position.y),
            (self.position.x + 10, self.position.y - 14),
            4,
        )
        pygame.draw.circle(
            screen,
            "black",
            (self.position.x, self.position.y),
            12,
        )
        if self.is_alive:
            pygame.draw.line(
                screen,
                "yellow",
                (self.position.x + 10, self.position.y - 12),
                (self.position.x + 10, self.position.y - 15),
                4,
            )


class Cannonball60mm(Cannonball):
    damage: int
    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 30
        self.radius_damage = 10
        self.units_available = 3

    def draw(self, screen: pygame.surface.Surface) -> None:
        travel_angle = math.atan2(self.velocity.y, self.velocity.x)
        angle_x = math.cos(travel_angle)
        angle_y = math.sin(travel_angle)
        tail_x = self.position.x - 10 * angle_x
        tail_y = self.position.y - 10 * angle_y

        pygame.draw.line(
            screen,
            "#4b5320",
            (self.position.x, self.position.y),
            (tail_x, tail_y),
            4,
        )

        if self.is_alive:
            fire_x = tail_x - 6 * angle_x
            fire_y = tail_y - 6 * angle_y
            pygame.draw.line(screen, "#fbb741", (tail_x, tail_y), (fire_x, fire_y), 6)


class Cannonball80mm(Cannonball):
    damage: int
    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 40
        self.radius_damage = 20
        self.units_available = 10

    def draw(self, screen: pygame.surface.Surface) -> None:
        triangle = [
            (self.position.x, self.position.y),
            (self.position.x + 5, self.position.y - 10),
            (self.position.x + 10, self.position.y),
        ]

        pygame.draw.rect(
            screen,
            constants.DarkGreen,
            pygame.Rect(self.position.x, self.position.y, 10, 15),
        )
        pygame.draw.line(
            screen,
            "yellow",
            (self.position.x, self.position.y + 7.5),
            (self.position.x + 10, self.position.y + 7.5),
            5,
        )
        pygame.draw.polygon(screen, constants.DarkGreen, triangle)
        if self.is_alive:
            pygame.draw.line(
                screen,
                "orange",
                (self.position.x + 5, self.position.y + 15),
                (self.position.x + 5, self.position.y + 20),
                4,
            )


class Player:
    """
    Esta clase se encarga de asignar el puntaje obtenido por tiro a cada jugador,
    a través del cálculo de la distancia con la bala lanzada y el tanque en
    objetivo
    """

    name: str
    points: int

    def __init__(self, name: str, points: int):
        self.name = name
        self.points = points

    def score(self, impact: Impact, tank_position: pygame.Vector2):
        """
        Función que se encarga de asignar el puntaje mediante el cálculo de la
        distancia cuando la bala cae con el tanque objetivo, mientras la bala
        caiga más cerca se le asigna más puntaje al jugador
        """
        cannonball_position = impact.position
        distance = (
            (cannonball_position.x - tank_position.x) ** 2
            + (cannonball_position.y - tank_position.y) ** 2
        ) ** (1 / 2)
        if impact.impact_type == ImpactType.TERRAIN:
            if distance <= constants.TANK_RADIO * 2:
                self.points = self.points + 100
            elif distance <= constants.TANK_RADIO + 200:
                self.points = self.points + 50
            else:
                self.points = self.points - (self.points // 3)

        elif impact.impact_type == ImpactType.TANK:
            self.points += 10000


class CannonballType:
    MM60 = 0
    MM80 = 1
    MM105 = 2


class Tank(Drawable, Collidable):
    """
    Esta clase representa un tanque en el juego,
    cuenta con funcionalidades para dibujarlo, detectar colisiones y disparar
    una bala de cañón en una dirección y velocidad específica
    """

    player: Player
    color: pygame.Color
    position: pygame.Vector2
    shoot_velocity: float  # m/s
    shoot_angle: float  # rad //
    actual: int  # bala seleccionada
    available: list[int]
    select: SelectCannonball
    life: int

    def __init__(self, color: pygame.Color, position: pygame.Vector2, player: Player):
        self.player = player
        self.color = color
        self.position = position
        self.shoot_angle = 3.0 * math.pi / 4.0  # rad
        self.shoot_velocity = 145  # m/s
        self.actual = CannonballType.MM60
        self.available = [3, 10, 3]
        self.life = 100

    def collides_with(self, point: pygame.Vector2, cannon: int) -> bool:
        """
        Esta función se encarga de revisar si el tanque fue golpeado por la bala
        del cañón retornado True o False según corresponda
        """
        if ((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2) ** (
            1 / 2
        ) <= constants.TANK_RADIO:
            return True
        elif ((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2) ** (
            1 / 2
        ) <= 10 and cannon == 0:
            return True
        if ((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2) ** (
            1 / 2
        ) <= 20 and cannon == 1:
            return True
        if ((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2) ** (
            1 / 2
        ) <= 30 and cannon == 2:
            return True
        return False

    def shoot(self) -> Cannonball:
        """
        Esta función calcula las direcciones para disparar el proyectil,
        y calcula la  posición del proyectil después del disparo.
        También crea y retorna el objeto Cannonball con estos atributos.
        """
        v_x = self.shoot_velocity * math.cos(self.shoot_angle)
        # the -1 is since in this system the vertical coordinates are inverted
        v_y = -1 * self.shoot_velocity * math.sin(self.shoot_angle)

        new_x = self.position.x + 20 * math.cos(self.shoot_angle)
        new_y = self.position.y - 20 * math.sin(self.shoot_angle)

        start_point = pygame.Vector2(new_x, new_y)
        start_velocity = pygame.Vector2(v_x, v_y)

        if self.actual == CannonballType.MM60:
            if self.available[0] > 0:
                self.available[0] = self.available[0] - 1
                return Cannonball60mm(start_point, start_velocity)
        elif self.actual == CannonballType.MM80:
            if self.available[1] > 0:
                self.available[1] = self.available[1] - 1
                return Cannonball80mm(start_point, start_velocity)
        elif self.actual == CannonballType.MM105:
            if self.available[2] > 0:
                self.available[2] = self.available[2] - 1
                return Cannonball105mm(start_point, start_velocity)

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Esta función se encarga de dibujar el tanque y actualiza la posición del
        cañón del tanque según su ángulo. Además, si está activado el modo
        desarrollador dibuja la hitbox
        """
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


class HUD(Drawable):
    """
    Esta clase es responsable de mostrar elementos relacionados con la
    información en pantalla que no es parte del terreno o del juego en sí  :)
    """

    tanks: list[Tank]
    left = 100
    top = constants.WINDOWS_SIZE[1] - int((3 / 5) * constants.HUD_HEIGHT)
    width = 160
    height = 50

    def __init__(self, tanks: list[Tank], tank_game: TankGame):
        self.tank_game = tank_game
        self.tanks = tanks
        self.hud_image = pygame.image.load(resource_path("images/Angle.png"))
        self.font = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 24)
        self.font30 = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 30)
        self.font16 = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 16)
        self.self_impact_windows = SelfImpactWindows(self.tank_game)
        self.text_angle1 = None
        self.text_angle2 = None
        self.text_velocity1 = None
        self.text_velocity2 = None
        self.text_cannonball_info = None

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Esta función  permite mostrar en pantalla todo lo relacionado a la
        información de cada tanque tales como angulo y velocidad de disparo,
        puntaje, máxima altura, máxima distancia, también verifica si el tanque
        se suicidó para llamar a la función correspondiente. Además, si el modo
        desarrollador está activado muestra los FPS.
        """
        self.tanks[0].shoot_angle %= 2.0 * math.pi
        self.tanks[1].shoot_angle %= 2.0 * math.pi

        screen.blit(
            self.hud_image, (0, constants.WINDOWS_SIZE[1] - constants.HUD_HEIGHT)
        )

        if self.tank_game.cannonball is not None:
            draw_pos = (
                self.tank_game.cannonball.position.x,
                constants.WINDOWS_SIZE[1] - constants.HUD_HEIGHT,
            )
            pygame.draw.circle(screen, "#cc0000", draw_pos, 6)
            height = int(
                constants.WINDOWS_SIZE[1]
                - self.tank_game.cannonball.position.y
                - constants.HUD_HEIGHT
            )
            cannonball_height_text = self.font16.render(
                f"^{height}[m]",
                True,
                "white",
            )
            screen.blit(
                cannonball_height_text,
                (
                    draw_pos[0] - cannonball_height_text.get_rect().size[0] // 2,
                    draw_pos[1] + cannonball_height_text.get_rect().size[1] // 2,
                ),
            )

        if self.tank_game.last_state is not None:
            transparency = 128
            rect_surface = pygame.Surface((300, 70))
            rect_surface.set_alpha(transparency)
            rect_x1, rect_y1 = constants.H_MAX
            rect_x2, rect_y2 = constants.DISTANCE_MAX
            screen.blit(rect_surface, (rect_x1, rect_y1))
            screen.blit(rect_surface, (rect_x2, rect_y2))

            if self.tank_game.cannonball is not None:
                self.text_cannonball_info = self.font.render(
                    f"Maxima Altura: {self.tank_game.cannonball.get_max_height()} [m]",
                    True,
                    "white",
                )
                screen.blit(self.text_cannonball_info, pygame.Vector2(40, 675))

                distance = self.tank_game.cannonball.calculate_distance_to(
                    self.tanks[self.tank_game.actual_player].position
                )
                self.text_cannonball_info = self.font.render(
                    f"Distancia total: {int(distance)}[m]",
                    True,
                    "white",
                )
                screen.blit(self.text_cannonball_info, pygame.Vector2(1020, 675))

        self.text_angle1 = self.font30.render(
            f"{math.degrees(self.tanks[0].shoot_angle):.1f}°",
            True,
            "white",
        )
        if self.tanks[0].life >= self.tanks[1].life:
            color_score1 = "green"
        else:
            color_score1 = "red"

        text_score1 = self.font.render(
            f"Vida : {self.tanks[0].life} puntos de vida",
            True,
            color_score1,
        )
        screen.blit(text_score1, pygame.Vector2(100, 875))
        if self.tanks[1].life >= self.tanks[1].life:
            color_score2 = "green"
        else:
            color_score2 = "red"

        text_score2 = self.font.render(
            f"Vida: {self.tanks[1].life} puntos de vida",
            True,
            color_score2,
        )
        screen.blit(text_score2, pygame.Vector2(750, 875))

        self.text_angle2 = self.font30.render(
            f"{math.degrees(self.tanks[1].shoot_angle):.1f}°",
            True,
            "white",
        )

        self.text_velocity1 = self.font30.render(
            f"{int(self.tanks[0].shoot_velocity)} m/s",
            True,
            "white",
        )
        self.text_velocity2 = self.font30.render(
            f"{int(self.tanks[1].shoot_velocity)} m/s",
            True,
            "white",
        )

        screen.blit(
            self.text_angle1,
            (
                (constants.WINDOWS_SIZE[0] * 0.07),
                constants.WINDOWS_SIZE[1] - (constants.HUD_HEIGHT * 0.7),
            ),
        )
        screen.blit(
            self.text_angle2,
            (
                (constants.WINDOWS_SIZE[0] * 0.87),
                constants.WINDOWS_SIZE[1] - (constants.HUD_HEIGHT * 0.7),
            ),
        )
        screen.blit(
            self.text_velocity1,
            (
                (constants.WINDOWS_SIZE[0] * 0.21),
                constants.WINDOWS_SIZE[1] - (constants.HUD_HEIGHT * 0.7),
            ),
        )
        screen.blit(
            self.text_velocity2,
            (
                (constants.WINDOWS_SIZE[0] * 0.7),
                constants.WINDOWS_SIZE[1] - (constants.HUD_HEIGHT * 0.7),
            ),
        )

        if (
            self.tank_game.last_state is not None
            and self.tank_game.last_state.impact_type == ImpactType.SUICIDIO
        ):
            self.self_impact_windows.draw(screen)

        if constants.DEVELOPMENT_MODE:
            screen.blit(
                self.font.render(
                    f"FPS: {int(self.tank_game.fps)}",
                    True,
                    "black",
                ),
                (0, 0),
            )

    def show_instructions(self, screen: pygame.surface.Surface):
        """
        Esta función permite mostrar al inicio del juego una imagen con las
        instrucciones necesarias para el/los jugadores
        """
        screen.fill("#151f28")

        instructions = pygame.image.load(resource_path("images/instructions.png"))
        rect = instructions.get_rect()
        size = rect.size

        screen.blit(
            instructions,
            (
                constants.WINDOWS_SIZE[0] / 2 - size[0] / 2,
                constants.WINDOWS_SIZE[1] / 2 - size[1] / 2,
            ),
        )
        out_text = self.font.render(
            "Presione espacio para continuar",
            True,
            "white",
        )
        size = out_text.get_rect().size
        screen.blit(
            out_text,
            (constants.WINDOWS_SIZE[0] - size[0], constants.WINDOWS_SIZE[1] - size[1]),
        )


class WinnerScreen(Drawable):
    """
    Esta clase se encarga de dibujar en pantalla un mensaje anunciando el
    ganador, mostrando su puntaje y el correspondiente tanque para una mejor
    distinción.
    """

    def __init__(self, tank_game: TankGame):
        """
        Constructor que inicializa todas los elementos necesarios para monstrar
        el mensaje de victoria.
        """
        self.font = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 20)
        self.tank_game = tank_game
        self.pos_fuegos = pygame.Vector2
        self.text_winner_info = None
        self.text_winner_life = None
        self.text_life1 = None
        self.text_life2 = None
        self.font100 = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 150)
        self.font100.set_bold(True)
        self.font100.set_italic(True)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-5, -1)
        self.radio = 2

    def winner_mensaje(self, screen: pygame.surface.Surface):
        """
        Esta función crea el mensaje de ganador, haciendo una ventana que
        muestre toda la información que el ganador sacó de la partida,
        incluyendo su puntaje, y como adicional se dibuja el tanque del color
        ganador
        """
        if self.tank_game.winner is None:
            # Si no hay ganador, no se ejecuta
            return

        center = (360, 260)
        transparency = 220
        rect_surface = pygame.Surface((900, 500))
        rect_surface.fill("#64BA1E")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = constants.H_WINNER
        screen.blit(rect_surface, (rect_x1, rect_y1))
        self.text_winner_info = self.font100.render(
            "WINNER",
            True,
            "white",
        )
        screen.blit(self.text_winner_info, center)

        points = self.tank_game.tanks[self.tank_game.winner].life
        self.font.set_bold(True)
        self.text_winner_life = self.font.render(
            f"Vida: {points} puntos de vida",
            True,
            "white",
        )
        self.font.set_bold(False)
        screen.blit(self.text_winner_life, pygame.Vector2(550, 250))

        pygame.draw.rect(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
            pygame.Rect(
                constants.TANK_WINNER[0] - 25, constants.TANK_WINNER[1] - 10, 50, 35
            ),
        )
        pygame.draw.rect(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
            pygame.Rect(
                constants.TANK_WINNER[0] - 62.5,
                constants.TANK_WINNER[1] + 25,
                125,
                50,
            ),
        )
        pygame.draw.rect(
            screen,
            constants.GRAY,
            pygame.Rect(
                constants.TANK_WINNER[0] - 62.5,
                constants.TANK_WINNER[1] + 75,
                125,
                20,
            ),
        )

        for i in range(6):
            pygame.draw.circle(
                screen,
                constants.BLACK,
                (
                    constants.TANK_WINNER[0] - 60 + 25 * i,
                    constants.TANK_WINNER[1] + 90,
                ),
                15,
            )

        pygame.draw.line(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
            constants.TANK_WINNER,
            (530, 470),
            15,
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Función que en el caso de que haya un ganador y aún no se muestre en
        pantalla, redigirá hacia otra función donde el mensaje se creará y será
        presentado al usuario por medio de la interfaz.
        """
        if self.tank_game.winner is not None:
            self.winner_mensaje(screen)


class Proyectil150(Cannonball):
    pass


class ImpactType:
    """
    Clase encargada de definir el tipo de ambiente con lo que impactó la bala,
    a cada tipo se le asigna un número
    """

    TERRAIN = 0
    BORDER = 1
    TANK = 2
    SUICIDIO = 3


class Impact:
    """
    Clase encargada de encontrar la posición en la que la bala impacta y
    determinar mediante el atributo impact_type con qué impacta terreno, borde,
    tanque o si es un suicidio
    """

    position: pygame.Vector2
    impact_type: int

    def __init__(self, position: pygame.Vector2, impact_type: int) -> None:
        self.position = position
        self.impact_type = impact_type


class SelfImpactWindows(Drawable):
    """
    This class represents a warning that is drawable, used when a tank shoots
    itself. In this case there are no winners and be warned
    """

    def __init__(self, tank_game: TankGame):
        self.font = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 20)
        self.tank_game = tank_game
        self.pos_fuegos = pygame.Vector2
        self.text_winner_info = None
        self.text_winner_score = None
        self.text_score1 = None
        self.text_score2 = None
        self.font100 = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 60)
        self.font100.set_bold(True)
        self.font100.set_italic(True)

    def draw(self, screen: pygame.surface.Surface):
        """
        This function draws a message indicating self-impact, serving as an
        easter egg for the players.
        """
        center = (360, 260)
        transparency = 220
        rect_surface = pygame.Surface((900, 500))
        rect_surface.fill("#CCCCCC")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = constants.H_WINNER
        screen.blit(rect_surface, (rect_x1, rect_y1))
        self.text_winner_info = self.font100.render(
            "ES MALO EL SUICIDIO",
            True,
            "red",
        )
        screen.blit(self.text_winner_info, center)


class Menu(Drawable, Collidable):
    fontTitle: Font
    storm: SnowStorm
    box_size = (200, 100)
    box_pos: Optional[tuple[float, float]]
    botton_color: str
    hover_botton_color: str
    is_hover: bool

    def __init__(self):
        self.fontTitle = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 43)
        self.storm = SnowStorm()
        self.box_pos = None
        self.botton_color = "#2E3440"
        self.hover_botton_color = "#3b4252"
        self.is_hover = False

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("#434C5E")
        self.storm.draw(screen)

        size = screen.get_size()
        self.box_pos = ((size[0] - self.box_size[0]) / 2, size[1] / 2)

        self.fontTitle.set_bold(True)
        title = self.fontTitle.render("Tank Game", True, "#B48EAD")
        self.fontTitle.set_bold(False)
        screen.blit(title, ((size[0] - title.get_size()[0]) / 2, size[1] / 6))

        options_box = pygame.rect.Rect(
            *self.box_pos, self.box_size[0], self.box_size[1]
        )
        pygame.draw.rect(
            screen,
            self.botton_color if not self.is_hover else self.hover_botton_color,
            options_box,
            0,
            10,
        )

        play = self.fontTitle.render("Jugar", True, "#B48EAD")
        screen.blit(
            play,
            (
                self.box_pos[0] + self.box_size[0] / 2 - play.get_size()[0] / 2,
                self.box_pos[1] + self.box_size[1] / 2 - play.get_size()[1] / 2,
            ),
        )

    def tick(self, dt: float):
        self.storm.tick(dt)

    def collides_with(self, point: pygame.Vector2) -> bool:
        if self.box_pos == None:
            return False
        return (self.box_pos[0] <= point.x <= self.box_pos[0] + self.box_size[0]) and (
            self.box_pos[1] <= point.y <= self.box_pos[1] + self.box_size[1]
        )


class TankGame:
    """
    This class represents the complete game, it is responsible for maintaining the
    tanks, bullets, controlling user input, drawing, among others. It can be said that
    it is the central class of the project.
    """

    terrain: Terrain
    tanks: list[Tank]
    screen: pygame.Surface
    cannonball: Optional[Cannonball]
    map_size: tuple[int, int]
    running: bool
    actual_player: int
    winner: Optional[int]
    winner_msj: WinnerScreen
    last_state: Optional[Impact]
    select_Cannonball: Optional[SelectCannonball]
    show_screen: bool

    def __init__(self) -> None:
        """
        constructor that initializes each element within the game, in
        addition to starting the window itself of the game.
        """
        pygame.init()

        pygame.display.set_caption("TankGame!")
        icon = pygame.image.load(resource_path("images/tankIcon.png"))
        pygame.display.set_icon(icon)

        self.map_size = (
            constants.WINDOWS_SIZE[0] - 2 * constants.BORDER_PADDING,
            constants.WINDOWS_SIZE[1]
            - constants.HUD_HEIGHT
            - 2 * constants.BORDER_PADDING,
        )
        self.background = Background()
        self.snow_storm = SnowStorm()
        self.terrain = Terrain(self.map_size, constants.MOUNTAINS, constants.VALLEYS)
        self.fps = float(constants.FPS)
        self.winner_msj = WinnerScreen(self)
        self.winner = None
        self.running = True
        self.screen = pygame.display.set_mode(constants.WINDOWS_SIZE)
        self.clock = pygame.time.Clock()
        self.last_state = None
        self.show_screen = False
        self.cannonball = None
        self.menu = Menu()
        self.tanks = []
        self.actual_player = randint(0, 1)

        quart_of_windows = int(self.map_size[0] / 4)

        mid_point = randint(int(quart_of_windows), int(3 * quart_of_windows))

        tank1_x = randint(0, mid_point - quart_of_windows)
        tank2_x = randint(mid_point + quart_of_windows, self.map_size[0])

        player1 = Player("1", 0)
        player2 = Player("2", 0)

        self.tanks.append(
            Tank(
                pygame.Color(50, 50, 0),
                pygame.Vector2(
                    tank1_x,
                    self.map_size[1]
                    - self.terrain.ground_lines[
                        tank1_x // constants.TERRAIN_LINE_WIDTH - 1
                    ]
                    - 15,
                ),
                player1,
            )
        )

        self.tanks.append(
            Tank(
                pygame.Color(80, 50, 50),
                pygame.Vector2(
                    tank2_x,
                    self.map_size[1]
                    - self.terrain.ground_lines[
                        tank2_x // constants.TERRAIN_LINE_WIDTH - 1
                    ]
                    - 15,
                ),
                player2,
            )
        )

        self.hud = HUD(self.tanks, self)
        self.select_Cannonball = SelectCannonball(self)

    def render(self) -> None:
        """
        This method is responsible for drawing each element of the window, it
        also puts the execution to sleep for a while to make the game run at the
        fps, specified in the FPS constant
        """
        game_rect = pygame.surface.Surface(self.map_size)

        self.background.draw(game_rect)
        self.snow_storm.draw(game_rect)
        self.terrain.draw(game_rect)

        for tank in self.tanks:
            tank.draw(game_rect)

        if self.cannonball is not None:
            self.cannonball.draw(game_rect)
        if self.winner is not None:
            self.winner_msj.draw(game_rect)

        self.screen.fill(constants.HUD_BACKGROUND)

        if self.last_state is not None and self.cannonball is not None:
            self.cannonball.draw_trajectory(game_rect)

        self.screen.blit(
            game_rect, (constants.BORDER_PADDING, constants.BORDER_PADDING)
        )

        self.hud.draw(self.screen)
        self.snow_storm.tick(1.0 / (self.fps + 0.1))
        if self.show_screen:
            self.select_Cannonball.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(constants.FPS)
        self.fps = self.clock.get_fps()

    def check_running(self):
        """
        This method checks if the player has sent the signal to close the window and
        stops the execution if this is the case, it is also responsible for cleaning
        any position that has been left unused.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def process_input(self) -> None:
        """
        This method is responsible for reading from the keyboard what the user wants
        to do, modifying the attributes of the tanks or creating the cannonball.
        :return:
        """
        playing_tank = self.tanks[self.actual_player]

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_DOWN]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle += math.radians(1) * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_angle += math.radians(0.1) * (
                    constants.FPS / self.fps
                )

        if keys_pressed[pygame.K_UP]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle -= math.radians(1) * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_angle -= math.radians(0.1) * (
                    constants.FPS / self.fps
                )

        if keys_pressed[pygame.K_RIGHT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity += 1 * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_velocity += 0.1 * (constants.FPS / self.fps)

            playing_tank.shoot_velocity = min(
                constants.SHOOT_MAX_SPEED, playing_tank.shoot_velocity
            )

        if keys_pressed[pygame.K_LEFT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity -= 1 * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_velocity -= 0.1 * (constants.FPS / self.fps)

            if playing_tank.shoot_velocity < 1:
                playing_tank.shoot_velocity = 1

        if keys_pressed[pygame.K_SPACE] and not self.show_screen:
            self.cannonball = playing_tank.shoot()

        if (
            keys_pressed[pygame.K_TAB]
            and not self.show_screen
            and self.show_screen == 0
        ):
            self.show_screen = True

        if (
            keys_pressed[pygame.K_1]
            or keys_pressed[pygame.K_2]
            or keys_pressed[pygame.K_3]
        ) and self.show_screen:
            if keys_pressed[pygame.K_1]:
                self.tanks[self.actual_player].actual = CannonballType.MM60
            elif keys_pressed[pygame.K_2]:
                self.tanks[self.actual_player].actual = CannonballType.MM80
            elif keys_pressed[pygame.K_3]:
                self.tanks[self.actual_player].actual = CannonballType.MM105
            self.show_screen = False

    @property
    def process_cannonball_trajectory(self) -> Optional[Impact]:
        """
        This method is responsible for moving the cannonball and seeing what happens,
        in case there is a terminal event, it stops the execution
        :return:
        """
        if self.cannonball is None:
            return None

        self.cannonball.tick((1.0 / self.fps) * constants.X_SPEED)

        if (
            self.cannonball.position.x < 0
            or self.cannonball.position.x > self.map_size[0]
        ):
            return Impact(self.cannonball.position, ImpactType.BORDER)

        if self.terrain.collides_with(self.cannonball.position):
            other_player = (self.actual_player + 1) % 2
            if self.tanks[other_player].life == 0:
                self.winner = self.actual_player
                self.running = False
            elif self.tanks[self.actual_player].life == 0:
                self.winner = other_player
                self.running = False
            return Impact(self.cannonball.position, ImpactType.TERRAIN)

        for tank in self.tanks:
            if self.cannonball is None:
                return
            other_player = (self.actual_player + 1) % 2
            if tank.collides_with(
                self.cannonball.position, self.tanks[self.actual_player].actual
            ):
                actual_radius_position = self.calculate_distance(self.actual_player)

                if actual_radius_position > constants.TANK_RADIO:
                    other_radius_position = self.calculate_distance(other_player)
                    if other_radius_position < constants.TANK_RADIO:
                        self.explotion()
                        return Impact(self.cannonball.position, ImpactType.TANK)
                else:
                    return Impact(self.cannonball.position, ImpactType.SUICIDIO)

        return None

    def explotion(self):
        color_explotion = "#B71C1C"
        particles = [
            (random.gauss(0, 0.5), random.uniform(0, 2 * math.pi)) for i in range(50)
        ]
        other_player = (self.actual_player + 1) % 2
        for i in range(50):
            for speed, angle in particles:
                distance = i * speed
                x = self.tanks[other_player].position.x + distance * math.cos(angle)
                y = (
                    self.tanks[other_player].position.y
                    + distance * math.sin(angle)
                    - 180
                )
                self.screen.set_at((int(x), int(y)), color_explotion)
            pygame.display.flip()

    def calculate_distance(self, player: int):
        actual_radius = math.sqrt(
            ((self.tanks[player].position.x - self.cannonball.position.x) ** 2)
            + ((self.tanks[player].position.y - self.cannonball.position.y) ** 2)
        )
        return actual_radius

    def wait_release_space(self) -> None:
        """
        This method waits until the actual player releases the space key, because
        if we do not wait until the release, the player could shoot a very short
        trajectory, and they accidentally shoot as the other player.
        :return: None
        """
        while pygame.key.get_pressed()[pygame.K_SPACE]:
            self.check_running()
            self.render()

    def cannonball_travel(self) -> None:
        """
        This function is responsible for drawing the projectile's parabolic path,
        making it advance, and then drawing it.
        """
        while self.running and self.last_state is None:
            self.check_running()
            self.last_state = self.process_cannonball_trajectory
            self.render()

    def life_tank(self, point: pygame.Vector2, tank: Tank, cannonball_type: int):
        """
        Esta función se encarga de quitar vida al tanque según la bala que impactó
        """
        if cannonball_type == 0:
            if (
                math.sqrt(
                    (point.x - tank.position.x) ** 2 + (point.y - tank.position.y) ** 2
                )
                <= constants.TANK_RADIO + 10
            ):
                tank.life = tank.life - 30
                if tank.life < 0:
                    tank.life = 0

        elif cannonball_type == 1:
            if (
                math.sqrt(
                    (point.x - tank.position.x) ** 2 + (point.y - tank.position.y) ** 2
                )
                <= constants.TANK_RADIO + 20
            ):
                tank.life = tank.life - 40
                if tank.life < 0:
                    tank.life = 0
        elif cannonball_type == 2:
            if (
                math.sqrt(
                    (point.x - tank.position.x) ** 2 + (point.y - tank.position.y) ** 2
                )
                <= constants.TANK_RADIO + 30
            ):
                tank.life = tank.life - 50
                if tank.life < 0:
                    tank.life = 0

    def wait_on_space(self) -> None:
        """
        This function will pause most of the game logic but won't completely
        block the execution. Updates of the background or similar elements will
        be displayed, but the game won't progress to menus or actions.
        """
        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()

    def check_last_state(self) -> None:
        """
        This function is responsible for checking what happened in the last shot
        and modifying the class fields to adapt to the outcome.
        """
        if self.last_state is not None:
            other_player = (self.actual_player + 1) % 2
            self.life_tank(
                self.last_state.position,
                self.tanks[other_player],
                self.tanks[self.actual_player].actual,
            )

            self.tanks[self.actual_player].player.score(
                self.last_state, self.tanks[other_player].position
            )

        if (
            self.last_state is not None
            and self.last_state.impact_type != ImpactType.BORDER
        ) and self.cannonball is not None:
            self.cannonball.kill()
        # if self.last_state is not None: # Lo movi, que piensan
        # self.terrain_destruction()

    def terrain_destruction(self):
        radius = self.cannonball.radius_damage
        if self.last_state.impact_type != ImpactType.BORDER:
            j = 0
            for i in range(
                int(self.last_state.position.x) - radius,
                int(self.last_state.position.x) + radius,
            ):
                if i <= self.last_state.position.x:
                    self.terrain.ground_lines[i] -= radius / 2 - j
                    j -= 1
                else:
                    self.terrain.ground_lines[i] -= radius / 2 - j
                    j += 1

    def start_menu(self):
        while self.running:
            self.check_running()
            self.menu.draw(self.screen)
            self.menu.tick((1.0 / (self.fps + 0.1)))

            ms = pygame.mouse.get_pos()

            self.menu.is_hover = self.menu.collides_with(pygame.Vector2(*ms))

            if pygame.mouse.get_pressed()[0] and self.menu.is_hover:
                break

            pygame.display.flip()
            self.clock.tick(constants.FPS)
            self.fps = self.clock.get_fps()

    def start(self) -> None:
        """
        Esta función muestra las instrucciones básicas para después dar paso al
        juego como tal. Se encarga de gestionar la situación actual, como cual
        jugador es el turno, el ángulo del cañon o si se ha decidido disparar,
        donde en cuyo caso se comprobará si la bala sigue avanzando o si ha
        impactado con algo.
        """
        self.start_menu()

        self.hud.show_instructions(self.screen)
        pygame.display.flip()

        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.clock.tick(constants.FPS)

        self.wait_release_space()

        while self.running:
            self.check_running()

            # Select the angle
            while self.running and self.cannonball is None:
                self.check_running()
                self.process_input()
                self.render()

            self.cannonball_travel()

            if (
                self.last_state is not None
                and self.last_state.impact_type == ImpactType.SUICIDIO
            ):
                break
            self.terrain_destruction()

            self.wait_release_space()
            self.wait_on_space()

            self.check_last_state()

            self.cannonball = None
            self.last_state = None

            self.wait_release_space()
            self.actual_player = (self.actual_player + 1) % 2  # Swap actual player
            self.render()

            are_tanks_without_live = False
            for tank in self.tanks:
                if tank.life == 0:
                    self.winner = (self.actual_player + 1) % 2
                    self.running = False
                    are_tanks_without_live = True
                    break

            if are_tanks_without_live:
                break

        self.running = True
        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()


def main():
    """
    From this function the program is started, creating the only instance of
    TankGame that exists...
    """
    tank_game = TankGame()
    tank_game.start()


if __name__ == "__main__":
    main()
