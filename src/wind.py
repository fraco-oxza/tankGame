import math
import random

import constants


class Wind:
    """
    This class is responsible for changing the wind speed and direction over
    time.
    """

    __velocity: float
    __target_velocity: float
    __min_velocity: int
    __max_velocity: int

    def __init__(self) -> None:
        """Initialize the class with the default values"""
        self.__min_velocity = 1
        self.__max_velocity = 10
        self.__velocity = self.__target_velocity = self.__min_velocity

    @property
    def velocity(self) -> float:
        """Return the current velocity"""
        return self.__velocity

    def is_changing(self) -> bool:
        """Return whether the wind is changing"""
        return abs(self.__target_velocity - self.__velocity) > constants.EPSILON

    def change_speed(self):
        """Change the speed of the wind"""
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

    def tick(self, dt: float) -> None:
        """
        This function is responsible for advancing the wind and changing its
        speed.
        """
        velocity_diff = self.__target_velocity - self.__velocity
        self.__velocity += (
            constants.WIND_SPEED_CHANGE_SCALE * math.tanh(velocity_diff) * dt
        )
