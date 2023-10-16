import pygame


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
