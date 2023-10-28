import pygame
from pygame.time import Clock

import constants


class Context:
    """
    this class is responsible for save the info about the general game.
    """

    rounds: int
    screen: pygame.surface.Surface
    number_of_players: int
    number_of_rounds: int
    __windows_size: tuple[int, int]
    map_size: tuple[int, int]
    __fps: float
    clock: pygame.time.Clock

    def __init__(self) -> None:
        print("se ha creado un contexto")
        self.rounds = constants.DEFAULT_ROUNDS
        self.windows_size = constants.WINDOWS_SIZE
        self.screen = pygame.display.set_mode(self.__windows_size)
        self.number_of_players = constants.DEFAULT_NUMBER_OF_PLAYERS
        self.number_of_rounds = constants.DEFAULT_ROUNDS
        self.number_of_bots = constants.DEFAULT_NUMBER_OF_BOTS
        self.type_of_effect = constants.DEFAULT_TYPE_EFFECT
        self.__fps = float(constants.FPS)
        self.clock = Clock()

    @property
    def fps(self) -> float:
        return self.__fps

    @fps.setter
    def fps(self, val):
        self.__fps = max(0.1, val)

    @property
    def windows_size(self) -> tuple[int, int]:
        return self.__windows_size

    @windows_size.setter
    def windows_size(self, new_size: tuple[int, int]) -> None:
        self.__windows_size = new_size
        self.map_size = (
            new_size[0] - 2 * constants.BORDER_PADDING,
            new_size[1] - constants.HUD_HEIGHT - 2 * constants.BORDER_PADDING,
        )
        self.screen = pygame.display.set_mode(new_size)


instance = Context()
