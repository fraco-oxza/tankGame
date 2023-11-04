import math
import random

from constants import EPSILON


class Wind:
    __velocity: float
    __target_velocity: float
    __min_velocity: int
    __max_velocity: int

    def __init__(self) -> None:
        self.__min_velocity = 1
        self.__max_velocity = 10
        self.__velocity = self.__target_velocity = self.__min_velocity

    @property
    def velocity(self) -> float:
        return self.__velocity

    def tick(self, dt: float) -> None:
        if abs(self.__velocity - self.__target_velocity) < EPSILON:
            self.__target_velocity = float(
                random.randint(
                    self.__min_velocity - self.__max_velocity,
                    self.__max_velocity - self.__min_velocity,
                )
            )

            if self.__target_velocity < 0.0:
                self.__target_velocity -= self.__min_velocity
            else:
                self.__target_velocity += self.__min_velocity

        velocity_diff = self.__target_velocity - self.__velocity
        self.__velocity += math.tanh(velocity_diff) * dt
