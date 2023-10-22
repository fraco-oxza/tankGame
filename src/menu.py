from typing import Optional

import pygame
from pygame.font import Font

from caches import font_cache
from caches import image_cache
from collidable import Collidable
from draw import Drawable
from snow_storm import SnowStorm
import constants


class Menu(Drawable, Collidable):
    fontTitle: Font
    storm: SnowStorm
    box_size = (200, 100)
    box_pos: Optional[tuple[float, float]]
    botton_color: str
    hover_botton_color: str
    is_hover: bool

    def __init__(self, storm: SnowStorm):
        self.fontTitle = font_cache["Roboto.ttf", 43]
        image_size = pygame.Vector2(
            constants.WINDOWS_SIZE[0], constants.WINDOWS_SIZE[1]
        )
        self.image = pygame.transform.scale(image_cache["images/Play.png"], image_size)
        self.storm = storm
        self.box_pos = None
        self.botton_color = "#2E3440"
        self.hover_botton_color = "#3b4252"
        self.is_hover = False
        self.sky_rect = self.image.get_rect()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.sky_rect.topleft)
        transparency = 150
        rect_surface = pygame.Surface(
            (constants.WINDOWS_SIZE[0], constants.WINDOWS_SIZE[1])
        )
        rect_surface.fill("#000000")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = (0, 0)
        screen.blit(rect_surface, (rect_x1, rect_y1))
        self.storm.draw(screen)

        size = screen.get_size()
        self.box_pos = ((size[0] - self.box_size[0]) / 2, size[1] / 2)

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
        self.storm.tick(dt)

    def collides_with(self, point: pygame.Vector2) -> bool:
        if self.box_pos is None:
            return False
        return (self.box_pos[0] <= point.x <= self.box_pos[0] + self.box_size[0]) and (
            self.box_pos[1] <= point.y <= self.box_pos[1] + self.box_size[1]
        )
