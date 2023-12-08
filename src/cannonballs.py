import math
import sys
from abc import abstractmethod

import pygame

import constants
import context
from draw import Drawable


class Cannonball(Drawable):
    """
    This class represents a cannonball in motion, provides
    functionalities to update your position, draw your trajectory and
    get information.
    """

    damage: int
    radius: float
    position: pygame.Vector2
    velocity: pygame.Vector2
    trajectory: list[pygame.Vector2]
    max_height: float
    max_distance: int
    is_alive: bool

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        self.position = position
        self.velocity = velocity
        self.max_height = sys.maxsize
        self.max_distance = sys.maxsize
        self.is_alive = True
        self.trajectory = []
        self.radius_damage = 0

    def tick(self, dt: float, gravity: float):
        """
        This function updates the position of the bullet for each interval
        of time, its purpose is to simulate the movement and behavior of the
        parable drawn by the cannonball.
        """
        self.position += self.velocity * dt
        self.velocity[1] += gravity * dt

        if self.position.y < self.max_height:
            self.max_height = self.position.y

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
        This function "deactivates" the cannonball to indicate that it is no longer in
        use, for this removes the trajectory attribute of the object and sets the
        life status in False
        """
        del self.trajectory
        self.is_alive = False

    def draw_trajectory(self, screen: pygame.surface.Surface):
        """
        This function draws the trajectory of the bullet, for each point on the
        trajectory list draws a circle.
        """
        for point in self.trajectory:
            pygame.draw.circle(screen, "#000000", (point.x, point.y), 1)

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        """This function is responsible for drawing the bullet chosen by the user"""
        raise NotImplementedError

    def get_max_height(self) -> int:
        """
        This function is responsible for returning the maximum launch height of
        the bullet
        """
        return int(context.instance.map_size[1] - self.max_height)

    def calculate_distance_to(self, tank_position: pygame.Vector2) -> int:
        """
        This function is responsible for returning the maximum distance between
        the bullet and the tank that launched it
        """
        return (
            (self.position.x - tank_position.x) ** 2
            + (self.position.y - tank_position.y) ** 2
        ) ** (1 / 2)


class CannonballType:
    """function that identifies what type of cannonball the user chose"""

    MM60 = 0
    MM80 = 1
    MM105 = 2


class Cannonball105mm(Cannonball):
    """
    This class represents the 105mm cannonball, with its available quantity and
    damage attributes
    """

    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 50
        self.radius_damage = 30
        self.units_available = 3
        self.radius = 30

    def draw(self, screen: pygame.surface.Surface) -> None:
        """This function is responsible for drawing the bullet chosen by the user"""
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
    This class represents the 60mm cannonball, with its available quantity and
    damage attributes
    """

    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 30
        self.radius_damage = 10
        self.units_available = 3
        self.radius = 10

    def draw(self, screen: pygame.surface.Surface) -> None:
        """This function is responsible for drawing the bullet chosen by the user"""
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
    This class represents the 80mm cannonball, with its available quantity and
    damage attributes
    """

    radius_damage: int
    units_available: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.damage = 40
        self.radius_damage = 20
        self.units_available = 10
        self.radius = 20

    def draw(self, screen: pygame.surface.Surface) -> None:
        """This function is responsible for drawing the bullet chosen by the user"""
        travel_angle = math.atan2(self.velocity.y, self.velocity.x)
        angle_x = math.cos(travel_angle)
        angle_y = math.sin(travel_angle)

        tail_x = self.position.x - 25 * angle_x
        tail_y = self.position.y - 25 * angle_y

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
