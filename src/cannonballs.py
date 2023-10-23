import math
import sys
from abc import abstractmethod

import pygame

import constants
from draw import Drawable


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
        self.radius_damage = CannonballType

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
        lista trajectory dibuja un círculo.
        """
        for point in self.trajectory:
            pygame.draw.circle(screen, "#000000", (point.x, point.y), 1)

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        raise NotImplementedError

    def get_max_height(self) -> int:
        """
        Esta función se encarga de retornar la altura máxima del lanzamiento de
        la bala
        """
        return constants.MAP_SIZE[1] - self.max_height

    def calculate_distance_to(self, tank_position: pygame.Vector2) -> int:
        """
        Esta función se encarga de retornar la distancia máxima entre la bala y
        el tanque que la lanzó
        """
        return (
            (self.position.x - tank_position.x) ** 2
            + (self.position.y - tank_position.y) ** 2
        ) ** (1 / 2)


class CannonballType:
    """
    function that identifies what type of cannonball the user chose
    """

    MM60 = 0
    MM80 = 1
    MM105 = 2


class Cannonball105mm(Cannonball):
    """
    This class represents the 105mm cannonball, with its available quantity and damage attributes
    """

    damage: int
    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 50
        self.radius_damage = 30
        self.units_available = 3

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function is responsible for drawing the bullet chosen by the user
        """
        travel_angle = math.atan2(self.velocity.y, self.velocity.x)
        angle_x = math.cos(travel_angle)
        angle_y = math.sin(travel_angle)
        tail_x = self.position.x + 20 * angle_x
        tail_y = self.position.y - 20 * angle_y
        middle_x = tail_x + 5 * angle_x
        middle_y = tail_y - 5 * angle_y
        pygame.draw.line(
            screen,
            "gray",
            (self.position.x, self.position.y),
            (tail_x, tail_y),
            4,
        )
        pygame.draw.line(
            screen,
            "yellow",
            (tail_x, tail_y),
            (middle_x, middle_y),
            4,
        )
        pygame.draw.circle(
            screen,
            "black",
            (self.position.x, self.position.y),
            12,
        )


class Cannonball60mm(Cannonball):
    """
    This class represents the 60mm cannonball, with its available quantity and damage attributes
    """

    damage: int
    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 30
        self.radius_damage = 10
        self.units_available = 3

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function is responsible for drawing the bullet chosen by the user
        """
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
    """
    This class represents the 80mm cannonball, with its available quantity and damage attributes
    """

    damage: int
    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 40
        self.radius_damage = 20
        self.units_available = 10

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function is responsible for drawing the bullet chosen by the user
        """
        travel_angle = math.atan2(self.velocity.y, self.velocity.x)
        angle_x = math.cos(travel_angle)
        angle_y = math.sin(travel_angle)

        tail_x = self.position.x - 25 * angle_x
        tail_y = self.position.y - 25 * angle_y

        vertex1 = (self.position.x, self.position.y)
        vertex2 = (self.position.x + 10, self.position.y)
        vertex3 = (self.position.x + 5, self.position.y - 10)

        pygame.draw.line(
            screen,
            constants.DarkGreen,
            (self.position.x, self.position.y),
            (tail_x, tail_y),
            10,
        )

        sep_start = (self.position.x - 10 * angle_x, self.position.y - 10 * angle_y)
        sep_end = (self.position.x - 15 * angle_x, self.position.y - 15 * angle_y)

        pygame.draw.line(screen, "yellow", sep_start, sep_end, 10)

        cola = (tail_x - 10 * angle_x, tail_y - 10 * angle_y)

        pygame.draw.line(screen, "orange", (tail_x, tail_y), cola, 4)
        pygame.draw.polygon(screen, constants.DarkGreen, [vertex1, vertex2, vertex3])
