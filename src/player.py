import pygame

import constants
from impact import Impact, ImpactType


class Player:
    """
    This class is responsible for assigning the score obtained per shot to each player,
    through the calculation of the distance with the bullet launched and the tank in
    aim
    """

    name: str
    points: int

    def __init__(self, name: str, points: int):
        self.name = name
        self.points = points

    def score(self, impact: Impact, tank_position: pygame.Vector2):
        """
        Method that is responsible for assigning the score by calculating the
        distance when the bullet falls with the target tank, while the bullet
        The closer it lands, the more points are assigned to the player.
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
        elif impact.impact_type == ImpactType.SUICIDIO:
            self.points += 5000
