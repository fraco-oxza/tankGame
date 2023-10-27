from typing import Optional

import pygame
from pygame.font import Font

from caches import font_cache
from caches import image_cache
from collidable import Collidable
from draw import Drawable
from snow_storm import SnowStorm
import constants
from context import instance


class Menu(Drawable, Collidable):
    """
    This class is in charge of displaying everything related to the main menu on the screen
    when you enter the game.
    """

    fontTitle: Font
    storm: SnowStorm
    box_size = (instance.windows_size[0] / 6.4, instance.windows_size[1] / 7.2)
    box_pos: Optional[tuple[float, float]]
    botton_color: str
    hover_botton_color: str
    is_hover: bool

    def __init__(self, storm: SnowStorm):
        self.fontTitle = font_cache["Roboto.ttf", int(instance.windows_size[0] / 29.76)]
        image_size = pygame.Vector2(instance.windows_size[0], instance.windows_size[1])
        self.image = pygame.transform.scale(image_cache["images/Play.png"], image_size)
        self.storm = storm
        self.box_pos = None
        self.botton_color = "#2E3440"
        self.hover_botton_color = "#3b4252"
        self.is_hover = False
        self.sky_rect = self.image.get_rect()

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Function responsible for creating and displaying the new surface on the screen,
        which is responsible for loading the background image and drawing the start button
        """
        screen.blit(self.image, self.sky_rect.topleft)
        transparency = 150
        rect_surface = pygame.Surface(
            (instance.windows_size[0], instance.windows_size[1])
        )
        rect_surface.fill("#000000")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = (0, 0)
        screen.blit(rect_surface, (rect_x1, rect_y1))
        self.storm.draw(screen)

        size = screen.get_size()
        self.box_pos = ((size[0] - self.box_size[0]) / 2, (3 / 4) * size[1])

        self.fontTitle.set_bold(True)
        title = self.fontTitle.render("Tank Game", True, "#ffffff")
        self.fontTitle.set_bold(False)
        screen.blit(title, ((size[0] - title.get_size()[0]) / 2, size[1] / 6))

        options_box = pygame.rect.Rect(
            *self.box_pos, self.box_size[0], self.box_size[1]
        )
        pygame.draw.rect(
            screen,
            self.botton_color if not self.is_hover else self.hover_botton_color,
            options_box,
            0,
            10,
        )

        play = self.fontTitle.render("Jugar", True, "#FFFFFF")
        screen.blit(
            play,
            (
                self.box_pos[0] + self.box_size[0] / 2 - play.get_size()[0] / 2,
                self.box_pos[1] + self.box_size[1] / 2 - play.get_size()[1] / 2,
            ),
        )

    def tick(self, dt: float):
        """Function that is responsible for drawing the snow"""
        self.storm.tick(dt)

    def collides_with(self, point: pygame.Vector2) -> bool:
        """
        The "point" parameter is the position that the mouse has on the user, this function is responsible
        for returning true or false depending on the case. If the mouse position is over the start button
        and it is clicked, it returns true, otherwise false
        """
        if self.box_pos is None:
            return False
        return (self.box_pos[0] <= point.x <= self.box_pos[0] + self.box_size[0]) and (
            self.box_pos[1] <= point.y <= self.box_pos[1] + self.box_size[1]
        )
