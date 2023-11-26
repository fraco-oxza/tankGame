import pygame
from pygame.time import Clock

import constants
import player
from effects import AmbientEffect


class Context:
    """
    this class is responsible for save the info about the general game.
    """

    rounds: int
    screen: pygame.surface.Surface
    number_of_players: int
    number_of_bots: int
    number_of_rounds: int
    __windows_size: tuple[int, int]
    map_size: tuple[int, int]
    __fps: float
    clock: pygame.time.Clock
    players: list[player.Player]
    type_of_effect: AmbientEffect

    def __init__(self) -> None:
        self.windows_size = constants.DEFAULT_WINDOWS_SIZE
        self.screen = pygame.display.set_mode(self.__windows_size)
        self.number_of_players = constants.DEFAULT_NUMBER_OF_PLAYERS
        self.number_of_rounds = constants.DEFAULT_ROUNDS
        self.number_of_bots = constants.DEFAULT_NUMBER_OF_BOTS
        self.type_of_effect = constants.DEFAULT_TYPE_EFFECT
        self.__fps = float(constants.FPS)
        self.clock = Clock()
        self.players = []

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
        self.aspect_ratio = self.windows_size[0] / self.windows_size[1]
        self.hud_height = self.windows_size[1] / 3.6
        self.border_padding = self.windows_size[1] // 36
        self.map_size = (
            new_size[0] - 2 * self.border_padding,
            int(new_size[1] - self.hud_height - 2 * self.border_padding),
        )
        self.screen = pygame.display.set_mode(new_size)


instance = Context()
