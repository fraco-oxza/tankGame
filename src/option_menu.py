from typing import Optional

import pygame

import constants
from caches import font_cache, image_cache
from context import instance
from inputs import check_running


class OptionMenu:
    box_size = pygame.Vector2
    box_pos: Optional[tuple[float, float]]
    button_color1: str
    button_color2: str
    button_color3: str
    hover_botton_color: str
    button_position = pygame.Vector2
    sobre: Optional[int]

    def __init__(self, screen: pygame.Surface):
        self.button_reset_position = pygame.Vector2(instance.windows_size[0] / 25, instance.windows_size[1] / 15)
        self.font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.button_color1 = "#73726E"
        self.button_color2 = "#73726E"
        self.button_color3 = "#73726E"
        self.button_color4 = "#73726E"
        self.button_color5 = "#73726E"
        self.button_color6 = "#73726E"
        self.button_color7 = "#73726E"
        self.button_color8 = "#73726E"
        self.button_color9 = "#73726E"
        self.button_color10 = "#73726E"
        self.button_color11 = "#73726E"
        self.hover_botton_color = constants.DarkGreen
        self.screen = screen
        self.sobre = None
        self.clock = pygame.time.Clock()
        image_size = pygame.Vector2(
            instance.windows_size[0], instance.windows_size[1]
        )
        self.image = pygame.transform.scale(
            image_cache["images/options.png"], image_size
        )
        self.sky_rect = self.image.get_rect()
        self.quantity_players = 2

    def render(self):
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
            self.screen.blit(self.paint_left(1), (370, 130))
            self.screen.blit(self.paint_left(2), (370, 225))
            self.screen.blit(self.paint_left(3), (370, 315))
            self.screen.blit(self.paint_left(4), (370, 405))
            self.screen.blit(self.paint_left(5), (370, 495))
            self.screen.blit(self.paint_right(6), (840, 130))
            self.screen.blit(self.paint_right(7), (840, 225))
            self.screen.blit(self.paint_right(8), (840, 315))
            self.screen.blit(self.paint_right(9), (840, 405))
            self.screen.blit(self.paint_right(10), (840, 495))
            msj = self.font.render("Tamaño de la Pantalla", True, "#ffffff")
            self.screen.blit(msj
                             ,
                             (
                                 520, 115,
                             ),
                             )
            msj = self.font.render("Cantidad de Jugadores", True, "#ffffff")
            self.screen.blit(msj
                             ,
                             (
                                 515, 210,
                             ),
                             )
            msj = self.font.render("Cantidad de Bots", True, "#ffffff")
            self.screen.blit(msj
                             ,
                             (
                                 545, 305,
                             ),
                             )
            msj = self.font.render("Número de Rondas", True, "#ffffff")
            self.screen.blit(msj
                             ,
                             (
                                 535, 395,
                             ),
                             )
            msj = self.font.render("Efectos de Entorno", True, "#ffffff")
            self.screen.blit(msj
                             ,
                             (
                                 535, 485,
                             ),
                             )
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            self.handle_input(mouse)
            msj = self.font.render(f"{self.quantity_players}", True, "#ffffff")
            self.screen.blit(msj
                             ,
                             (
                                 620, 245,
                             ),
                             )
            if pygame.mouse.get_pressed()[0]:
                self.selection()
            self.clock.tick(constants.FPS)
            pygame.display.flip()

    def handle_input(self, mouse: pygame.Vector2):
        """
        Function responsible for identifying which button the user pressed by clicking on one of the buttons.
        It is also responsible for changing the color of the button when the mouse passes over a button,
        otherwise it remains in its original color
        """
        button_left_1 = (
            370,
            130,
        )
        if button_left_1[0] < mouse.x < (
                button_left_1[0] + self.button_reset_position[0]
        ) and button_left_1[1] < mouse.y < (
                button_left_1[1] + self.button_reset_position[1]
        ):
            self.button_color1 = self.hover_botton_color
            self.sobre = 1
        else:
            self.button_color1 = "#73726E"
        button_left_2 = (370, 225)
        if button_left_2[0] < mouse.x < (
                button_left_2[0] + self.button_reset_position[0]
        ) and button_left_2[1] < mouse.y < (button_left_2[1] + self.button_reset_position[1]):
            self.button_color2 = self.hover_botton_color
            self.sobre = 2
        else:
            self.button_color2 = "#73726E"
        button_left_3 = (370, 315)
        if button_left_3[0] < mouse.x < (
                button_left_3[0] + self.button_reset_position[0]
        ) and button_left_3[1] < mouse.y < (button_left_3[1] + self.button_reset_position[1]):
            self.button_color3 = self.hover_botton_color
            self.sobre = 3
        else:
            self.button_color3 = "#73726E"
        button_left_4 = (370, 405)
        if button_left_4[0] < mouse.x < (
                button_left_4[0] + self.button_reset_position[0]
        ) and button_left_4[1] < mouse.y < (button_left_4[1] + self.button_reset_position[1]):
            self.button_color4 = self.hover_botton_color
            self.sobre = 4
        else:
            self.button_color4 = "#73726E"
        button_left_5 = (370, 495)
        if button_left_5[0] < mouse.x < (
                button_left_5[0] + self.button_reset_position[0]
        ) and button_left_5[1] < mouse.y < (button_left_5[1] + self.button_reset_position[1]):
            self.button_color5 = self.hover_botton_color
            self.sobre = 5
        else:
            self.button_color5 = "#73726E"
        button_left_6 = (840, 130)
        if button_left_6[0] < mouse.x < (
                button_left_6[0] + self.button_reset_position[0]
        ) and button_left_6[1] < mouse.y < (button_left_6[1] + self.button_reset_position[1]):
            self.button_color6 = self.hover_botton_color
            self.sobre = 6
        else:
            self.button_color6 = "#73726E"
        button_left_7 = (840, 225)
        if button_left_7[0] < mouse.x < (
                button_left_7[0] + self.button_reset_position[0]
        ) and button_left_7[1] < mouse.y < (button_left_7[1] + self.button_reset_position[1]):
            self.button_color7 = self.hover_botton_color
            self.sobre = 7
        else:
            self.button_color7 = "#73726E"
        button_left_8 = (840, 315)
        if button_left_8[0] < mouse.x < (
                button_left_8[0] + self.button_reset_position[0]
        ) and button_left_8[1] < mouse.y < (button_left_8[1] + self.button_reset_position[1]):
            self.button_color8 = self.hover_botton_color
            self.sobre = 8
        else:
            self.button_color8 = "#73726E"
        button_left_9 = (840, 405)
        if button_left_9[0] < mouse.x < (
                button_left_9[0] + self.button_reset_position[0]
        ) and button_left_9[1] < mouse.y < (button_left_9[1] + self.button_reset_position[1]):
            self.button_color9 = self.hover_botton_color
            self.sobre = 9
        else:
            self.button_color9 = "#73726E"
        button_left_10 = (840, 495)
        if button_left_10[0] < mouse.x < (
                button_left_10[0] + self.button_reset_position[0]
        ) and button_left_10[1] < mouse.y < (button_left_10[1] + self.button_reset_position[1]):
            self.button_color10 = self.hover_botton_color
            self.sobre = 10
        else:
            self.button_color10 = "#73726E"
        button_left_11 = (370, 495)
        if button_left_11[0] < mouse.x < (
                button_left_11[0] + self.button_reset_position[0]
        ) and button_left_11[1] < mouse.y < (button_left_11[1] + self.button_reset_position[1]):
            self.button_color11 = self.hover_botton_color
            self.sobre = 11
        else:
            self.button_color11 = "#73726E"

    def paint_left(self, index: int):
        """
        Function responsible for creating the surface that represents the button,
        in addition to writing the message of each button in the center of each surface
        """
        sf = pygame.Surface(self.button_reset_position)
        if index == 1:
            sf.fill(self.button_color1)
        elif index == 2:
            sf.fill(self.button_color2)
        elif index == 3:
            sf.fill(self.button_color3)
        elif index == 4:
            sf.fill(self.button_color4)
        elif index == 5:
            sf.fill(self.button_color5)
        pygame.draw.polygon(sf, "#ffffff", [(40, 10), (10, 25), (40, 40)])

        return sf

    def paint_right(self, index: int):
        """
        Function responsible for creating the surface that represents the button,
        in addition to writing the message of each button in the center of each surface
        """
        sf = pygame.Surface(self.button_reset_position)
        if index == 6:
            sf.fill(self.button_color6)
        elif index == 7:
            sf.fill(self.button_color7)
        elif index == 8:
            sf.fill(self.button_color8)
        elif index == 9:
            sf.fill(self.button_color9)
        elif index == 10:
            sf.fill(self.button_color10)
        elif index == 11:
            sf.fill(self.button_color11)
        pygame.draw.polygon(sf, "#ffffff", [(10, 10), (40, 25), (10, 40)])

        return sf

    def selection(self):
        if self.sobre == 2:
            if self.quantity_players > 2:
                self.quantity_players -= 1
        if self.sobre == 7:
            if self.quantity_players < 20:
                self.quantity_players += 1
        self.clock.tick(constants.FPS / 15)
