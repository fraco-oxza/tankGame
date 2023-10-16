import pygame

from caches import font_cache
from cannonballs import CannonballType
import constants
from draw import Drawable


class WarnningWindows(Drawable):
    """
    This class represents a warning
    """

    num_seleccionado: int
    quantity: list[int]

    def __init__(self, tank_game):
        self.tank_game = tank_game
        self.quantity = None
        self.num_seleccionado = None
        self.font = font_cache["Roboto.ttf", 20]
        self.font2 = font_cache["Roboto.ttf", 12]
        self.font100 = font_cache["Roboto.ttf", 60]
        self.font.set_bold(True)
        self.font50 = font_cache["Roboto.ttf", 15]
        self.size = (constants.WINDOWS_SIZE[0] / 3.6, constants.WINDOWS_SIZE[1] / 7.2)

    def get_backround(self) -> pygame.Surface:
        rect_surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        rect_surface = rect_surface.convert_alpha()

        pygame.draw.rect(
            rect_surface,
            "#232323",
            pygame.Rect(0, 0, *self.size),
            0,
            border_bottom_left_radius=10,
            border_bottom_right_radius=10,
        )
        image = image_cache["images/warning.png"]
        rect_surface.blit(image, (10, 10))

        return rect_surface

    def quantity_mm_60(self):
        if self.quantity[self.num_seleccionado] == 0:
            return False
        return True

    def quantity_mm_80(self):
        if self.quantity[self.num_seleccionado] == 0:
            return False
        return True

    def quantity_mm_105(self):
        if self.quantity[self.num_seleccionado] == 0:
            return False
        return True

    def draw(self, screen: pygame.surface.Surface):
        self.num_seleccionado = self.tank_game.tanks[
            self.tank_game.actual_player
        ].actual
        self.quantity = self.tank_game.tanks[self.tank_game.actual_player].available
        if self.num_seleccionado == CannonballType.MM60 and not self.quantity_mm_60():
            sf = self.get_backround()
            self.font100 = self.font.render(
                f"No quedan balas de 60MM",
                True,
                "white",
            )
            sf.blit(self.font100, (100, 20))
            self.font50 = self.font2.render(
                f"Seleccione alguna bala diferente",
                True,
                "white",
            )

            sf.blit(self.font50, (100, 50))

            self.font50 = self.font2.render(
                f"con los números 2 o 3",
                True,
                "white",
            )
            sf.blit(self.font50, (100, 65))

            screen.blit(sf, (constants.WINDOWS_SIZE[0] / 2 - sf.get_size()[0] / 2, 0))
        if self.num_seleccionado == CannonballType.MM80 and not self.quantity_mm_80():
            sf = self.get_backround()
            self.font100 = self.font.render(
                f"No quedan balas de 80MM",
                True,
                "white",
            )
            sf.blit(self.font100, (100, 20))
            self.font50 = self.font2.render(
                f"Seleccione alguna bala diferente",
                True,
                "white",
            )

            sf.blit(self.font50, (100, 50))

            self.font50 = self.font2.render(
                f"con los números 1 o 3",
                True,
                "white",
            )
            sf.blit(self.font50, (100, 65))

            screen.blit(sf, (constants.WINDOWS_SIZE[0] / 2 - sf.get_size()[0] / 2, 0))

        if self.num_seleccionado == CannonballType.MM105 and not self.quantity_mm_105():
            sf = self.get_backround()
            self.font100 = self.font.render(
                f"No quedan balas de 105MM",
                True,
                "white",
            )
            sf.blit(self.font100, (100, 20))
            self.font50 = self.font2.render(
                f"Seleccione alguna bala diferente",
                True,
                "white",
            )

            sf.blit(self.font50, (100, 50))

            self.font50 = self.font2.render(
                f"con los números 2 o 3",
                True,
                "white",
            )
            sf.blit(self.font50, (100, 65))

            screen.blit(sf, (constants.WINDOWS_SIZE[0] / 2 - sf.get_size()[0] / 2, 0))
