import pygame
from caches import font_cache
from caches import image_cache
from cannonballs import CannonballType
from draw import Drawable
from context import instance


class WarningWindows(Drawable):
    """
    This class represents a warning when the current cannonball does not have
    ammunition. It disappears when another cannonball is selected.
    """

    num_seleccionado: int
    quantity: list[int]

    def __init__(self, tank_game):
        """
        This constructor loads the fonts that will be used, and It sets the size
        of the warning box based on the screen size. It saves the tank_game
        instance inside the object to know the quantity of ammunition
        available and the current cannonball.
        """
        self.tank_game = tank_game
        self.quantity = []
        self.num_seleccionado = 0
        self.font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 64)]
        self.font2 = font_cache["Roboto.ttf", int(instance.windows_size[0] / 106.66)]
        self.font100 = font_cache["Roboto.ttf", int(instance.windows_size[0] / 21.33)]
        self.font.set_bold(True)
        self.font50 = font_cache["Roboto.ttf", int(instance.windows_size[0] / 85.33)]
        self.size = (instance.windows_size[0] / 3.6, instance.windows_size[1] / 7.2)

    def get_background(self) -> pygame.Surface:
        """
        This method creates the warning surface. Then It draws the
        background and return the surface.
        """
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
        rect_surface.blit(
            image, (instance.windows_size[0] / 128, instance.windows_size[1] / 72)
        )

        return rect_surface

    def is_current_cannonball_available(self):
        """This method asks if the current cannonball has ammunition available"""
        return self.quantity[self.num_seleccionado] > 0

    def draw(self, screen: pygame.surface.Surface):
        """
        This method creates a different screen with the warning. Then It puts
        this new screen onto the center of the main screen.
        """
        self.num_seleccionado = self.tank_game.tanks[
            self.tank_game.actual_player
        ].actual
        self.quantity = self.tank_game.get_current_tank().player.ammunition

        if self.is_current_cannonball_available():
            # In this case there are cannonballs available, so is not necessary
            # to display the warning.
            return

        missing_caliber = None
        alternatives = None

        if self.num_seleccionado == CannonballType.MM60:
            missing_caliber = "60MM"
            alternatives = "2 o 3"
        if self.num_seleccionado == CannonballType.MM80:
            missing_caliber = "80MM"
            alternatives = "1 o 3"
        if self.num_seleccionado == CannonballType.MM105:
            missing_caliber = "105MM"
            alternatives = "1 o 2"

        sf = self.get_background()
        self.font100 = self.font.render(
            f"No quedan balas de {missing_caliber}",
            True,
            "white",
        )
        sf.blit(
            self.font100,
            (instance.windows_size[0] / 12.8, instance.windows_size[1] / 36),
        )
        self.font50 = self.font2.render(
            "Seleccione alguna bala diferente",
            True,
            "white",
        )
        if instance.windows_size[0] > 1000:
            sf.blit(
                self.font50,
                (instance.windows_size[0] / 12.8, instance.windows_size[1] / 14.4),
            )
        else:
            sf.blit(
                self.font50,
                (instance.windows_size[0] / 9, instance.windows_size[1] / 14.4),
            )
        self.font50 = self.font2.render(
            f"con los números {alternatives}",
            True,
            "white",
        )
        if instance.windows_size[0] > 1000:
            sf.blit(
                self.font50,
                (instance.windows_size[0] / 12.8, instance.windows_size[1] / 11.07),
            )
        else:
            sf.blit(
                self.font50,
                (instance.windows_size[0] / 8, instance.windows_size[1] / 11.07),
            )

        screen.blit(sf, (instance.windows_size[0] / 2 - sf.get_size()[0] / 2, 0))
