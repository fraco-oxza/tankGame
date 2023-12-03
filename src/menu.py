from typing import Optional

import pygame
from pygame.font import Font

from caches import font_cache
from caches import image_cache
from caches import audio_cache
from exit_requested import ExitRequested
from context import instance


class MenuStatus:
    nothing = 0
    start = 1
    options = 2


class Menu:
    """
    This class is in charge of displaying everything related to the main menu on the screen
    when you enter the game.
    """

    fontTitle: Font
    box_size = (instance.windows_size[0] / 6.4, instance.windows_size[1] / 7.2)
    box_pos: Optional[tuple[float, float]]
    botton_color: str
    hover_botton_color: str
    is_hover: bool
    prev: bool

    def __init__(self, screen: pygame.surface.Surface):
        self.fontTitle = font_cache["Roboto.ttf", int(instance.windows_size[0] / 29.76)]
        self.box_pos = None
        self.box_pos_options = None
        self.button_color1 = "#2E3440"
        self.button_color2 = "#2E3440"
        self.hover_botton_color = "#3b4252"
        self.is_hover = False
        self.upon = None
        self.screen = screen
        self.prev = False
        image_size = pygame.Vector2(instance.windows_size[0], instance.windows_size[1])
        self.image = pygame.transform.scale(image_cache["images/Play.png"], image_size)
        self.sky_rect = self.image.get_rect()

    def render(self) -> int:
        """
        Function responsible for creating and displaying the new surface on the screen,
        which is responsible for loading the background image and drawing the start button
        """
        self.screen.blit(self.image, self.sky_rect.topleft)
        transparency = 150
        rect_surface = pygame.Surface(
            (instance.windows_size[0], instance.windows_size[1])
        )
        rect_surface.fill("#000000")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = (0, 0)
        self.screen.blit(rect_surface, (rect_x1, rect_y1))

        size = self.screen.get_size()
        self.box_pos = ((size[0] - self.box_size[0]) / 2, (5 / 8) * size[1])
        self.box_pos_options = ((size[0] - self.box_size[0]) / 2, (6.5 / 8) * size[1])
        self.fontTitle.set_bold(True)
        title = self.fontTitle.render("Tank Game", True, "#ffffff")
        self.fontTitle.set_bold(False)
        self.screen.blit(title, ((size[0] - title.get_size()[0]) / 2, size[1] / 6))

        box = pygame.rect.Rect(*self.box_pos, self.box_size[0], self.box_size[1])
        option_box = pygame.rect.Rect(
            *self.box_pos_options, self.box_size[0], self.box_size[1]
        )
        pygame.draw.rect(
            self.screen,
            self.button_color1,
            box,
            0,
            10,
        )
        pygame.draw.rect(
            self.screen,
            self.button_color2,
            option_box,
            0,
            10,
        )
        play = self.fontTitle.render("Jugar", True, "#FFFFFF")
        self.screen.blit(
            play,
            (
                self.box_pos[0] + self.box_size[0] / 2 - play.get_size()[0] / 2,
                self.box_pos[1] + self.box_size[1] / 2 - play.get_size()[1] / 2,
            ),
        )
        options = self.fontTitle.render("Opciones", True, "#FFFFFF")
        self.screen.blit(
            options,
            (
                self.box_pos_options[0]
                + self.box_size[0] / 2
                - options.get_size()[0] / 2,
                self.box_pos_options[1]
                + self.box_size[1] / 2
                - options.get_size()[1] / 2,
            ),
        )

        self.handle_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise ExitRequested
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                if self.upon == 1:
                    return MenuStatus.start
                if self.upon == 2:
                    return MenuStatus.options
        return MenuStatus.nothing

    def show_menu(self):
        return self.render()

    def handle_input(self):
        """
        Function responsible for identifying which button the user pressed by clicking on one of the buttons.
        It is also responsible for changing the color of the button when the mouse passes over a button,
        otherwise it remains in its original color
        """
        mouse = pygame.Vector2(pygame.mouse.get_pos())
        if (self.box_pos[0] <= mouse.x <= self.box_pos[0] + self.box_size[0]) and (
            self.box_pos[1] <= mouse.y <= self.box_pos[1] + self.box_size[1]
        ):
            self.button_color1 = self.hover_botton_color
            self.upon = 1
        else:
            self.button_color1 = "#2E3440"
        if (
            self.box_pos_options[0]
            <= mouse.x
            <= self.box_pos_options[0] + self.box_size[0]
        ) and (
            self.box_pos_options[1]
            <= mouse.y
            <= self.box_pos_options[1] + self.box_size[1]
        ):
            self.button_color2 = self.hover_botton_color
            self.upon = 2

        else:
            self.button_color2 = "#2E3440"
