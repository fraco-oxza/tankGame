import pygame

import constants
from caches import font_cache
from caches import image_cache
from cannonballs import CannonballType
from draw import Drawable


class WarningWindows(Drawable):
    """This class represents a warning"""

    num_seleccionado: int
    quantity: list[int]

    def __init__(self, tank_game):
        self.tank_game = tank_game
        self.quantity = []
        self.num_seleccionado = 0
        self.font = font_cache["Roboto.ttf", 20]
        self.font2 = font_cache["Roboto.ttf", 12]
        self.font100 = font_cache["Roboto.ttf", 60]
        self.font.set_bold(True)
        self.font50 = font_cache["Roboto.ttf", 15]
        self.size = (constants.WINDOWS_SIZE[0] / 3.6, constants.WINDOWS_SIZE[1] / 7.2)

    def get_background(self) -> pygame.Surface:
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

        missing_caliber = None
        alternatives = None
        if self.num_seleccionado == CannonballType.MM60 and not self.quantity_mm_60():
            missing_caliber = "60MM"
            alternatives = "2 o 3"
        if self.num_seleccionado == CannonballType.MM80 and not self.quantity_mm_80():
            missing_caliber = "80MM"
            alternatives = "1 o 3"
        if self.num_seleccionado == CannonballType.MM105 and not self.quantity_mm_105():
            missing_caliber = "105MM"
            alternatives = "2 o 3"

        if missing_caliber is None:
            # En este caso no faltan balas, por lo tanto no se muestra la advertencia
            return

        sf = self.get_background()
        self.font100 = self.font.render(
            f"No quedan balas de {missing_caliber}",
            True,
            "white",
        )
        sf.blit(self.font100, (100, 20))
        self.font50 = self.font2.render(
            "Seleccione alguna bala diferente",
            True,
            "white",
        )

        sf.blit(self.font50, (100, 50))

        self.font50 = self.font2.render(
            f"con los números {alternatives}",
            True,
            "white",
        )
        sf.blit(self.font50, (100, 65))

        screen.blit(sf, (constants.WINDOWS_SIZE[0] / 2 - sf.get_size()[0] / 2, 0))
