from typing import Optional

import pygame
from pygame.font import Font

import constants
from caches import font_cache, audio_cache, image_cache
from context import instance
from inputs import check_running


class InGameMenuStatus:
    """
    This class is responsible, through numbers, for identifying what type of
    option the user chooses.
    """

    EXIT = 0
    CONTINUE = 1
    RESTART = 2


class InGameMenu:
    """
    This class is responsible for loading the background image and drawing all
    the buttons that are in the menu (return, restart game and return) when the
    user presses the esc option on the keyboard.
    """

    fontExit: Font
    fontBack: Font
    fontRestart: Font
    box_size = pygame.Vector2
    box_pos: Optional[tuple[float, float]]
    botton_color1: str
    botton_color2: str
    botton_color3: str
    hover_botton_color: str
    button_reset_position = pygame.Vector2
    sobre: Optional[int]

    def __init__(self, screen: pygame.Surface):
        self.button_reset_position = pygame.Vector2(
            instance.windows_size[0] / 4.26, instance.windows_size[1] / 15
        )
        self.fontExit = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.fontRestart = font_cache[
            "Roboto.ttf", int(instance.windows_size[0] / 51.2)
        ]
        self.fontBack = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.botton_color1 = "#73726E"
        self.botton_color2 = "#73726E"
        self.botton_color3 = "#73726E"
        self.hover_botton_color = "#736868"
        self.screen = screen
        self.sobre = None
        self.clock = instance.clock
        image_size = pygame.Vector2(instance.windows_size[0], instance.windows_size[1])
        self.image = pygame.transform.scale(
            image_cache["images/Control.png"], image_size
        )
        self.sky_rect = self.image.get_rect()

    def render(self):
        """
        Function responsible for loading the image and the transparency over it
        while any of the button options are not pressed. It is also responsible
        for calling the function that draws the buttons on the screen and
        loading the snow that is drawn on the screen
        """
        while True:
            check_running()
            self.screen.blit(self.image, self.sky_rect.topleft)
            transparency = 150
            rect_surface = pygame.Surface(
                (instance.windows_size[0], instance.windows_size[1])
            )
            rect_surface.fill("#000000")
            rect_surface.set_alpha(transparency)
            rect_x1, rect_y1 = (0, 0)
            self.screen.blit(rect_surface, (rect_x1, rect_y1))
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            self.handle_input(mouse)
            if pygame.mouse.get_pressed()[0]:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                if self.sobre == 1:
                    return InGameMenuStatus.RESTART
                if self.sobre == 2:
                    return InGameMenuStatus.EXIT
                if self.sobre == 3:
                    return InGameMenuStatus.CONTINUE
            self.screen.blit(
                self.restart("Reiniciar Partida"),
                (instance.windows_size[0] // 2.6, instance.windows_size[1] / 2.37),
            )
            self.screen.blit(
                self.restart("Salir"),
                (instance.windows_size[0] // 2.6, instance.windows_size[1] / 2),
            )
            self.screen.blit(
                self.restart("Volver"),
                (instance.windows_size[0] // 2.6, instance.windows_size[1] / 2.9),
            )

            self.clock.tick(constants.FPS)
            pygame.display.flip()

    def handle_input(self, mouse: pygame.Vector2):
        """
        Function responsible for identifying which button the user pressed by
        clicking on one of the buttons. It is also responsible for changing the
        color of the button when the mouse passes over a button, otherwise it
        remains in its original color
        """
        restart_pos = (
            instance.windows_size[0] // 2.6,
            instance.windows_size[1] / 2.37,
        )
        if restart_pos[0] < mouse.x < (
            restart_pos[0] + self.button_reset_position[0]
        ) and restart_pos[1] < mouse.y < (
            restart_pos[1] + self.button_reset_position[1]
        ):
            self.botton_color1 = self.hover_botton_color
            self.sobre = 1
        else:
            self.botton_color1 = "#73726E"
        exit_pos = (instance.windows_size[0] // 2.6, instance.windows_size[1] / 2)
        if exit_pos[0] < mouse.x < (
            exit_pos[0] + self.button_reset_position[0]
        ) and exit_pos[1] < mouse.y < (exit_pos[1] + self.button_reset_position[1]):
            self.botton_color2 = self.hover_botton_color
            self.sobre = 2
        else:
            self.botton_color2 = "#73726E"
        back_pos = (instance.windows_size[0] // 2.6, instance.windows_size[1] / 2.9)
        if back_pos[0] < mouse.x < (
            back_pos[0] + self.button_reset_position[0]
        ) and back_pos[1] < mouse.y < (back_pos[1] + self.button_reset_position[1]):
            self.botton_color3 = self.hover_botton_color
            self.sobre = 3
        else:
            self.botton_color3 = "#73726E"

    def start_menu(self) -> int:
        """
        function responsible for calling the render function that is responsible
        for displaying the entire menu screen
        """
        return self.render()

    def restart(self, mensaje: str):
        """
        Function responsible for creating the surface that represents the button,
        in addition to writing the message of each button in the center of each surface
        """
        sf = pygame.Surface(self.button_reset_position)
        box_size = sf.get_size()
        end = self.fontRestart.render(mensaje, True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 4)
        if mensaje == "Reiniciar Partida":
            sf.fill(self.botton_color1)
        elif mensaje == "Salir":
            sf.fill(self.botton_color2)
        elif mensaje == "Volver":
            sf.fill(self.botton_color3)

        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 2 - end.get_size()[0] / 2,
                box_pos[1] / 1.2,
            ),
        )
        return sf
