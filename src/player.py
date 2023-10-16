import pygame

import constants
from impact import Impact, ImpactType


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
        elif impact.impact_type == ImpactType.SUICIDIO:
            self.points += 5000
