from __future__ import annotations

import math
import os
import random
import sys
from abc import abstractmethod
from random import randint
from typing import Optional

import pygame

import constants


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
        raise NotImplementedError


class Drawable:
    """
    Clase que contiene un método abstracto que se pasa a través de Override a
    otras clases, donde se crearán elementos visuales que serán mostrados por
    medio de la interfaz.
    """

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        raise NotImplementedError


class Background(Drawable):
    """
    This class represents the game background, which loads an image and creates
    animations of falling snow with wind.
    """

    sky_image: pygame.Surface
    snowflakes: list[pygame.Vector2]
    wind: float
    wind_target: float

    def __init__(self):
        """
        Initialize the class by loading the images and creating the snowflakes.
        """

        image_size = pygame.Vector2(
            constants.WINDOWS_SIZE[0], (9 / 16) * constants.WINDOWS_SIZE[0]
        )
        self.sky_image = pygame.transform.scale(
            pygame.image.load(resource_path("images/sky.jpg")), image_size
        )
        self.sky_rect = self.sky_image.get_rect()
        self.snowflakes = []
        for _ in range(constants.SNOWFLAKES):
            self.add_random_snowflake()
        self.wind = 0
        self.wind_target = 0

    def add_random_snowflake(self):
        """
        Add a snowflake at a random valid position within the map.
        """
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
            if snowflake.y > (constants.WINDOWS_SIZE[1] - constants.HUD_HEIGHT):
                snowflake.y -= constants.WINDOWS_SIZE[1] - constants.HUD_HEIGHT

            # Corner case sides
            if snowflake.x > constants.WINDOWS_SIZE[0]:
                snowflake.x -= constants.WINDOWS_SIZE[0]
            elif snowflake.x < 0:
                snowflake.x += constants.WINDOWS_SIZE[0]

            if abs(self.wind - self.wind_target) < 1e-9:
                self.wind_target = (random.random() - 0.5) * 10.0

            wind_diff = self.wind_target - self.wind
            self.wind += math.tanh(wind_diff) * dt * 1e-3

            snowflake.x += self.wind

    def draw_snowflakes(self, screen: pygame.surface.Surface):
        """
        This function draws each snowflake present in the list of snowflakes.
        """
        for snowflake in self.snowflakes:
            pygame.draw.circle(screen, "#ffffff", snowflake, 1)

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function is responsible for drawing the background and the
        snowflakes.
        """
        screen.blit(self.sky_image, self.sky_rect.topleft)
        self.draw_snowflakes(screen)


class Terrain(Drawable, Collidable):
    """
    Esta clase representa al terreno, permite generar y dibujarlo aleatoriamente
    por cada partida, además comprueba colisiones con este
    """

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
        segment_size = constants.WINDOWS_SIZE[0] // deformations
        segment_start = 0
        segment_end = segment_size
        deformations_index = [*range(deformations)]
        random.shuffle(deformations_index)
        valleys = deformations_index[0:valley]

        for i in range(deformations):
            start = segment_start + randint(3 * (-segment_size // 4), segment_size // 3)
            end = segment_end + randint(-segment_size // 3, 3 * (segment_size // 4))

            start = max(start, 0)
            end = min(end, constants.WINDOWS_SIZE[0] - 1)

            if i in valleys:
                deep = randint(constants.SEA_LEVEL // 4, constants.SEA_LEVEL // 2)
                self.valley(start, end, deep)
            else:
                max_height = (
                    constants.WINDOWS_SIZE[1]
                    - constants.HUD_HEIGHT
                    - constants.SEA_LEVEL
                )
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

    def __init__(self, mountains: int, valleys: int):
        self.ground_lines = [constants.SEA_LEVEL] * (
            constants.WINDOWS_SIZE[0] // constants.TERRAIN_LINE_WIDTH
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
                    constants.WINDOWS_SIZE[1] - line - constants.HUD_HEIGHT,
                    constants.TERRAIN_LINE_WIDTH,
                    20,
                ),
            )
            if line >= 20:
                pygame.draw.rect(
                    screen,
                    "#c8dfe2",
                    pygame.Rect(
                        i * constants.TERRAIN_LINE_WIDTH,
                        constants.WINDOWS_SIZE[1] - line - constants.HUD_HEIGHT + 20,
                        constants.TERRAIN_LINE_WIDTH,
                        40,
                    ),
                )
            else:
                continue

            if line >= 60:
                pygame.draw.rect(
                    screen,
                    "#50707f",
                    pygame.Rect(
                        i * constants.TERRAIN_LINE_WIDTH,
                        constants.WINDOWS_SIZE[1] - line - constants.HUD_HEIGHT + 60,
                        constants.TERRAIN_LINE_WIDTH,
                        60,
                    ),
                )
            else:
                continue

            if line >= 120:
                pygame.draw.rect(
                    screen,
                    "#415c6b",
                    pygame.Rect(
                        i * constants.TERRAIN_LINE_WIDTH,
                        constants.WINDOWS_SIZE[1] - line - constants.HUD_HEIGHT + 120,
                        constants.TERRAIN_LINE_WIDTH,
                        120,
                    ),
                )
            else:
                continue

            if line >= 240:
                pygame.draw.rect(
                    screen,
                    "#2e4957",
                    pygame.Rect(
                        i * constants.TERRAIN_LINE_WIDTH,
                        constants.WINDOWS_SIZE[1] - line - constants.HUD_HEIGHT + 240,
                        constants.TERRAIN_LINE_WIDTH,
                        line - 240,
                    ),
                )

    def collides_with(self, point: pygame.Vector2) -> bool:
        """
        Esta función se encarga de verificar si la posición de la bala colisionó
        o no con el terreno, esto lo hace comparando la altura del terreno en la
        línea correspondiente al punto con la coordenada del cañón
        """
        line_index = int(point.x) // constants.TERRAIN_LINE_WIDTH

        return point.y > (constants.WINDOWS_SIZE[1] - self.ground_lines[line_index])


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
            pygame.draw.circle(
                screen, "#000000", (point.x, point.y - constants.HUD_HEIGHT), 1
            )

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Esta función se encarga de dibujar la trayectoria con la figura de misil
        de la bala, y si está vivo, dibuja un efecto de fuego
        """
        travel_angle = math.atan2(self.velocity.y, self.velocity.x)
        angle_x = math.cos(travel_angle)
        angle_y = math.sin(travel_angle)
        tail_x = self.position.x - 10 * angle_x
        tail_y = self.position.y - 10 * angle_y - constants.HUD_HEIGHT

        pygame.draw.line(
            screen,
            "#4b5320",
            (self.position.x, self.position.y - constants.HUD_HEIGHT),
            (tail_x, tail_y),
            4,
        )

        if self.is_alive:
            fire_x = tail_x - 6 * angle_x
            fire_y = tail_y - 6 * angle_y
            pygame.draw.line(screen, "#fbb741", (tail_x, tail_y), (fire_x, fire_y), 6)

    def get_max_height(self) -> int:
        """
        esta función se encarga de retornar la altura máxima del lanzamiento de
        la bala
        """
        return constants.WINDOWS_SIZE[1] - self.max_height - constants.HUD_HEIGHT

    def calculate_distance_to(self, tank_position: pygame.Vector2) -> int:
        """
        esta función se encarga de retornar la distancia máxima entre la bala y
        el tanque que la lanzó
        """
        return (
            (self.position.x - tank_position.x) ** 2
            + (self.position.y - tank_position.y) ** 2
        ) ** (1 / 2)


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

    def __init__(self, color: pygame.Color, position: pygame.Vector2, player: Player):
        self.player = player
        self.color = color
        self.position = position
        self.shoot_angle = 3.0 * math.pi / 4.0  # rad
        self.shoot_velocity = 145  # m/s

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
                (self.position.x, self.position.y - constants.HUD_HEIGHT),
                constants.TANK_RADIO,
            )
        cannon_angle_x = math.cos(self.shoot_angle)
        cannon_angle_y = math.sin(self.shoot_angle)
        cannon_x = self.position.x + 20 * cannon_angle_x
        cannon_y = self.position.y - 20 * cannon_angle_y - constants.HUD_HEIGHT
        muzzle_x = cannon_x + 5 * cannon_angle_x
        muzzle_y = cannon_y - 5 * cannon_angle_y

        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.position.x - 5, self.position.y - 2 - constants.HUD_HEIGHT, 10, 7
            ),
        )
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.position.x - 12.5,
                self.position.y + 5 - constants.HUD_HEIGHT,
                25,
                10,
            ),
        )
        pygame.draw.rect(
            screen,
            constants.GRAY,
            pygame.Rect(
                self.position.x - 12.5,
                self.position.y + 15 - constants.HUD_HEIGHT,
                25,
                4,
            ),
        )

        # decoration IN PROCESS, IS UGLY NOW
        for i in range(6):
            pygame.draw.circle(
                screen,
                constants.BLACK,
                (
                    self.position.x - 12 + 5 * i,
                    self.position.y + 18 - constants.HUD_HEIGHT,
                ),
                3,
            )

        # cannon
        pygame.draw.line(
            screen,
            self.color,
            (self.position.x, self.position.y - constants.HUD_HEIGHT),
            (cannon_x, cannon_y),
            4,
        )
        pygame.draw.line(
            screen, self.color, (cannon_x, cannon_y), (muzzle_x, muzzle_y), 6
        )

    def collides_with(self, point: pygame.Vector2) -> bool:
        """
        Esta función se encarga de revisar si el tanque fue golpeado por la bala
        del cañón retornado True o False según corresponda
        """
        if ((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2) ** (
            1 / 2
        ) <= constants.TANK_RADIO:
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

        return Cannonball(pygame.Vector2(new_x, new_y), pygame.Vector2(v_x, v_y))


class HUD(Drawable):
    """
    Esta clase es responsable de mostrar elementos relacionados con la
    información en pantalla que no es parte del terreno o del juego en sí
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
                self.tank_game.cannonball.draw_trajectory(screen)

        self.text_angle1 = self.font30.render(
            f"{math.degrees(self.tanks[0].shoot_angle):.1f}°",
            True,
            "white",
        )
        if self.tanks[0].player.points >= self.tanks[1].player.points:
            color_score1 = "green"
        else:
            color_score1 = "red"

        text_score1 = self.font.render(
            f"Puntaje: {self.tanks[0].player.points} puntos",
            True,
            color_score1,
        )
        screen.blit(text_score1, pygame.Vector2(100, 875))
        if self.tanks[1].player.points >= self.tanks[1].player.points:
            color_score2 = "green"
        else:
            color_score2 = "red"

        text_score2 = self.font.render(
            f"Puntaje: {self.tanks[1].player.points} puntos",
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
        self.text_winner_score = None
        self.text_score1 = None
        self.text_score2 = None
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

        points = self.tank_game.tanks[self.tank_game.winner].player.points
        self.font.set_bold(True)
        self.text_winner_score = self.font.render(
            f"Puntaje: {points} puntos",
            True,
            "white",
        )
        self.font.set_bold(False)
        screen.blit(self.text_winner_score, pygame.Vector2(550, 250))

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
    old_cannonballs: list[Cannonball]
    running: bool
    actual_player: int
    winner: Optional[int]
    winner_msj: WinnerScreen
    last_state: Optional[Impact]

    def __init__(self) -> None:
        """
        constructor that initializes each element within the game, in
        addition to starting the window itself of the game.
        """
        pygame.init()

        pygame.display.set_caption("TankGame!")
        icon = pygame.image.load(resource_path("images/tankIcon.png"))
        pygame.display.set_icon(icon)

        self.background = Background()
        self.terrain = Terrain(constants.MOUNTAINS, constants.VALLEYS)
        self.fps = float(constants.FPS)
        self.winner_msj = WinnerScreen(self)
        self.winner = None
        self.running = True
        self.screen = pygame.display.set_mode(constants.WINDOWS_SIZE)
        self.clock = pygame.time.Clock()
        self.last_state = None

        self.cannonball = None
        self.tanks = []
        self.old_cannonballs = []
        self.actual_player = randint(0, 1)

        quart_of_windows = int(constants.WINDOWS_SIZE[0] / 4)

        mid_point = randint(int(quart_of_windows), int(3 * quart_of_windows))

        tank1_x = randint(0, mid_point - quart_of_windows)
        tank2_x = randint(mid_point + quart_of_windows, constants.WINDOWS_SIZE[0])

        player1 = Player("1", 0)
        player2 = Player("2", 0)

        self.tanks.append(
            Tank(
                pygame.Color(50, 50, 0),
                pygame.Vector2(
                    tank1_x,
                    constants.WINDOWS_SIZE[1]
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
                    constants.WINDOWS_SIZE[1]
                    - self.terrain.ground_lines[
                        tank2_x // constants.TERRAIN_LINE_WIDTH - 1
                    ]
                    - 15,
                ),
                player2,
            )
        )

        self.hud = HUD(self.tanks, self)

    def render(self) -> None:
        """
        This method is responsible for drawing each element of the window, it
        also puts the execution to sleep for a while to make the game run at the
        fps, specified in the FPS constant
        """
        self.background.draw(self.screen)
        self.terrain.draw(self.screen)

        for tank in self.tanks:
            tank.draw(self.screen)

        for old_cannonball in self.old_cannonballs:
            old_cannonball.draw(self.screen)

        if self.cannonball is not None:
            self.cannonball.draw(self.screen)
        if self.winner is not None:
            self.winner_msj.draw(self.screen)
        self.hud.draw(self.screen)
        self.background.tick(1.0 / (self.fps + 0.1))

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

        if keys_pressed[pygame.K_SPACE]:
            self.cannonball = playing_tank.shoot()

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
            or self.cannonball.position.x > constants.WINDOWS_SIZE[0]
        ):
            return Impact(self.cannonball.position, ImpactType.BORDER)

        if self.terrain.collides_with(self.cannonball.position):
            return Impact(self.cannonball.position, ImpactType.TERRAIN)

        for tank in self.tanks:
            if tank.collides_with(self.cannonball.position):
                self.running = False
                actual_radius_position = (
                    (
                        (
                            self.tanks[self.actual_player].position.x
                            - self.cannonball.position.x
                        )
                        ** 2
                    )
                    + (
                        (
                            (
                                self.tanks[self.actual_player].position.y
                                - self.cannonball.position.y
                            )
                            ** 2
                        )
                    )
                ) ** 0.5

                if actual_radius_position > constants.TANK_RADIO:
                    self.winner = self.actual_player
                    return Impact(self.cannonball.position, ImpactType.TANK)
                return Impact(self.cannonball.position, ImpactType.SUICIDIO)

        return None

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

    def start(self) -> None:
        """
        Esta función muestra las instrucciones básicas para después dar paso al
        juego como tal. Se encarga de gestionar la situación actual, como cual
        jugador es el turno, el ángulo del cañon o si se ha decidido disparar,
        donde en cuyo caso se comprobará si la bala sigue avanzando o si ha
        impactado con algo.
        """
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

            # Travel of the cannonball
            while self.running and self.last_state is None:
                self.check_running()
                self.last_state = self.process_cannonball_trajectory()
                self.render()

            if (
                self.last_state is not None
                and self.last_state.impact_type == ImpactType.SUICIDIO
            ):
                break

            self.wait_release_space()

            while self.running:
                self.check_running()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_SPACE]:
                    break
                self.render()

            if self.last_state is not None:
                other_player = (self.actual_player + 1) % 2
                self.tanks[self.actual_player].player.score(
                    self.last_state, self.tanks[other_player].position
                )

            if (
                self.last_state is not None
                and self.last_state.impact_type != ImpactType.BORDER
            ) and self.cannonball is not None:
                self.cannonball.kill()
                self.old_cannonballs.append(self.cannonball)

            self.cannonball = None
            self.last_state = None

            self.wait_release_space()
            self.actual_player = (self.actual_player + 1) % 2  # Swap actual player
            self.render()

        self.running = True
        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()


def main():
    tank_game = TankGame()
    tank_game.start()


if __name__ == "__main__":
    main()
