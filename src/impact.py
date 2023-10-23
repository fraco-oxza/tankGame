import pygame

class ImpactType:
    """
    Class in charge of defining the type of environment with which the bullet impacted,
    each type is assigned a number
    """

    TERRAIN = 0
    BORDER = 1
    TANK = 2
    SUICIDIO = 3


class Impact:
    """
    Class in charge of finding the position in which the bullet hits and
    determine through the impact_type attribute what terrain, edge,
    tank or if it is a suicide
    """

    position: pygame.Vector2
    impact_type: int

    def __init__(self, position: pygame.Vector2, impact_type: int) -> None:
        self.position = position
        self.impact_type = impact_type
