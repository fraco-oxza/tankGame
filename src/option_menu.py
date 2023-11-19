from typing import Optional

import pygame

import constants
from caches import font_cache, image_cache
from context import instance
from effects import AmbientEffect
from inputs import check_running


class OptionMenuStatus:
    CONTINUE = 1


class OptionMenu:
    box_size = pygame.Vector2
    box_pos: Optional[tuple[float, float]]
    hover_botton_color: str
    button_position = pygame.Vector2
    sobre: Optional[int]

    def __init__(self, screen: pygame.Surface):
        self.secondary_buttons = pygame.Vector2(
            instance.windows_size[0] / 25, instance.windows_size[1] / 15
        )
        self.principal_button_size = pygame.Vector2(
            instance.windows_size[0] / 7.11, instance.windows_size[1] / 3.42
        )
        self.font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.button_color1 = "#46575E"
        self.button_color2 = "#46575E"
        self.button_color3 = "#46575E"
        self.button_color4 = "#46575E"
        self.button_color5 = "#46575E"
        self.button_color6 = "#46575E"
        self.button_color7 = "#46575E"
        self.button_color8 = "#46575E"
        self.button_color9 = "#46575E"
        self.button_color10 = "#46575E"
        self.button_color11 = "#A4715C"
        self.hover_botton_color = "#2A2E37"
        self.hover_botton_color_continue = "#9F705C"
        self.screen = screen
        self.sobre = None
        self.clock = pygame.time.Clock()
        image_size = pygame.Vector2(instance.windows_size[0], instance.windows_size[1])
        self.image = pygame.transform.scale(
            image_cache["images/options.png"], image_size
        )
        self.sky_rect = self.image.get_rect()
        self.quantity_players = instance.number_of_players
        self.quantity_bots = instance.number_of_bots
        self.quantity_rounds = instance.number_of_rounds
        self.environment_effects = [
            "Ninguno",
            "Gravedad",
            "Viento",
            "Gravedad y Viento",
        ]
        self.index_environment_effects = instance.type_of_effect
        # self.screen_resolution = ["800 X 800", "1366 X 768", "1600 x 900", "1280 X 720", "1920 X 1080"]
        self.screen_resolution = [
            (800, 800),
            (1280, 720),
            (1366, 768),
            (1600, 900),
            (1920, 1080),
        ]
        self.index_screen_resolution = self.screen_resolution.index(
            instance.windows_size
        )

    def render(self):
        while True:
            check_running()
            self.screen.blit(self.image, self.sky_rect.topleft)

            self.screen.blit(
                self.paint_left(1),
                (instance.windows_size[0] / 3.45, instance.windows_size[1] / 5.53),
            )
            self.screen.blit(
                self.paint_left(2),
                (instance.windows_size[0] / 3.45, instance.windows_size[1] / 3.2),
            )
            self.screen.blit(
                self.paint_left(3),
                (instance.windows_size[0] / 3.45, instance.windows_size[1] / 2.28),
            )
            self.screen.blit(
                self.paint_left(4),
                (instance.windows_size[0] / 3.45, instance.windows_size[1] / 1.77),
            )
            self.screen.blit(
                self.paint_left(5),
                (instance.windows_size[0] / 3.45, instance.windows_size[1] / 1.45),
            )
            self.screen.blit(
                self.paint_right(6),
                (instance.windows_size[0] / 1.52, instance.windows_size[1] / 5.53),
            )
            self.screen.blit(
                self.paint_right(7),
                (instance.windows_size[0] / 1.52, instance.windows_size[1] / 3.2),
            )
            self.screen.blit(
                self.paint_right(8),
                (instance.windows_size[0] / 1.52, instance.windows_size[1] / 2.28),
            )
            self.screen.blit(
                self.paint_right(9),
                (instance.windows_size[0] / 1.52, instance.windows_size[1] / 1.77),
            )
            self.screen.blit(
                self.paint_right(10),
                (instance.windows_size[0] / 1.52, instance.windows_size[1] / 1.45),
            )
            self.screen.blit(
                self.principal_button(11),
                (instance.windows_size[0] / 1.25, instance.windows_size[1] / 2.21),
            )
            msj = self.font.render("Tamaño de la Pantalla", True, "#ffffff")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.46,
                    instance.windows_size[1] / 6.26,
                ),
            )
            msj = self.font.render("Cantidad de Jugadores", True, "#ffffff")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.48,
                    instance.windows_size[1] / 3.42,
                ),
            )
            msj = self.font.render("Cantidad de Bots", True, "#ffffff")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.34,
                    instance.windows_size[1] / 2.36,
                ),
            )
            msj = self.font.render("Número de Rondas", True, "#ffffff")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.39,
                    instance.windows_size[1] / 1.82,
                ),
            )
            msj = self.font.render("Efectos de Entorno", True, "#ffffff")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.39,
                    instance.windows_size[1] / 1.48,
                ),
            )

            msj = self.font.render(f"{self.quantity_players}", True, "#8ACAC0")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.06,
                    instance.windows_size[1] / 2.93,
                ),
            )
            msj = self.font.render(f"{self.quantity_bots}", True, "#8ACAC0")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.06,
                    instance.windows_size[1] / 2.14,
                ),
            )
            msj = self.font.render(f"{self.quantity_rounds}", True, "#8ACAC0")
            self.screen.blit(
                msj,
                (
                    instance.windows_size[0] / 2.06,
                    instance.windows_size[1] / 1.69,
                ),
            )
            msj = self.font.render(
                f"{self.environment_effects[self.index_environment_effects.value]}",
                True,
                "#8ACAC0",
            )
            if self.index_environment_effects.value < len(self.environment_effects) - 1:
                self.screen.blit(
                    msj,
                    (
                        instance.windows_size[0] / 2.20,
                        instance.windows_size[1] / 1.39,
                    ),
                )
            else:
                self.screen.blit(
                    msj,
                    (
                        instance.windows_size[0] / 2.37,
                        instance.windows_size[1] / 1.39,
                    ),
                )
            x, y = self.screen_resolution[self.index_screen_resolution]
            msj = self.font.render(f"{x} X {y}", True, "#8ACAC0")
            if self.index_screen_resolution == 0:
                self.screen.blit(
                    msj,
                    (
                        instance.windows_size[0] / 2.16,
                        instance.windows_size[1] / 4.8,
                    ),
                )
            else:
                self.screen.blit(
                    msj,
                    (instance.windows_size[0] / 2.24, instance.windows_size[1] / 4.8),
                )
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            self.handle_input(mouse)
            if pygame.mouse.get_pressed()[0]:
                self.selection()
                if self.sobre == 11:
                    return OptionMenuStatus.CONTINUE
            self.clock.tick(constants.FPS)
            pygame.display.flip()

    def start_option_menu(self):
        return self.render()

    def handle_input(self, mouse: pygame.Vector2):
        """
        Function responsible for identifying which button the user pressed by
        clicking on one of the buttons. It is also responsible for changing the
        color of the button when the mouse passes over a button, otherwise it
        remains in its original color
        """
        button_left_1 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 5.53,
        )
        if button_left_1[0] < mouse.x < (
            button_left_1[0] + self.secondary_buttons[0]
        ) and button_left_1[1] < mouse.y < (
            button_left_1[1] + self.secondary_buttons[1]
        ):
            self.button_color1 = self.hover_botton_color
            self.sobre = 1
        else:
            self.button_color1 = "#46575E"
        button_left_2 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 3.2,
        )
        if button_left_2[0] < mouse.x < (
            button_left_2[0] + self.secondary_buttons[0]
        ) and button_left_2[1] < mouse.y < (
            button_left_2[1] + self.secondary_buttons[1]
        ):
            self.button_color2 = self.hover_botton_color
            self.sobre = 2
        else:
            self.button_color2 = "#46575E"
        button_left_3 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 2.28,
        )
        if button_left_3[0] < mouse.x < (
            button_left_3[0] + self.secondary_buttons[0]
        ) and button_left_3[1] < mouse.y < (
            button_left_3[1] + self.secondary_buttons[1]
        ):
            self.button_color3 = self.hover_botton_color
            self.sobre = 3
        else:
            self.button_color3 = "#46575E"
        button_left_4 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 1.77,
        )
        if button_left_4[0] < mouse.x < (
            button_left_4[0] + self.secondary_buttons[0]
        ) and button_left_4[1] < mouse.y < (
            button_left_4[1] + self.secondary_buttons[1]
        ):
            self.button_color4 = self.hover_botton_color
            self.sobre = 4
        else:
            self.button_color4 = "#46575E"
        button_left_5 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 1.45,
        )
        if button_left_5[0] < mouse.x < (
            button_left_5[0] + self.secondary_buttons[0]
        ) and button_left_5[1] < mouse.y < (
            button_left_5[1] + self.secondary_buttons[1]
        ):
            self.button_color5 = self.hover_botton_color
            self.sobre = 5
        else:
            self.button_color5 = "#46575E"
        button_left_6 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 5.53,
        )
        if button_left_6[0] < mouse.x < (
            button_left_6[0] + self.secondary_buttons[0]
        ) and button_left_6[1] < mouse.y < (
            button_left_6[1] + self.secondary_buttons[1]
        ):
            self.button_color6 = self.hover_botton_color
            self.sobre = 6
        else:
            self.button_color6 = "#46575E"
        button_left_7 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 3.2,
        )
        if button_left_7[0] < mouse.x < (
            button_left_7[0] + self.secondary_buttons[0]
        ) and button_left_7[1] < mouse.y < (
            button_left_7[1] + self.secondary_buttons[1]
        ):
            self.button_color7 = self.hover_botton_color
            self.sobre = 7
        else:
            self.button_color7 = "#46575E"
        button_left_8 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 2.28,
        )
        if button_left_8[0] < mouse.x < (
            button_left_8[0] + self.secondary_buttons[0]
        ) and button_left_8[1] < mouse.y < (
            button_left_8[1] + self.secondary_buttons[1]
        ):
            self.button_color8 = self.hover_botton_color
            self.sobre = 8
        else:
            self.button_color8 = "#46575E"
        button_left_9 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 1.77,
        )
        if button_left_9[0] < mouse.x < (
            button_left_9[0] + self.secondary_buttons[0]
        ) and button_left_9[1] < mouse.y < (
            button_left_9[1] + self.secondary_buttons[1]
        ):
            self.button_color9 = self.hover_botton_color
            self.sobre = 9
        else:
            self.button_color9 = "#46575E"
        button_left_10 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 1.45,
        )
        if button_left_10[0] < mouse.x < (
            button_left_10[0] + self.secondary_buttons[0]
        ) and button_left_10[1] < mouse.y < (
            button_left_10[1] + self.secondary_buttons[1]
        ):
            self.button_color10 = self.hover_botton_color
            self.sobre = 10
        else:
            self.button_color10 = "#46575E"
        button_left_11 = (
            instance.windows_size[0] / 1.25,
            instance.windows_size[1] / 2.21,
        )
        if button_left_11[0] < mouse.x < (
            button_left_11[0] + self.principal_button_size[0]
        ) and button_left_11[1] < mouse.y < (
            button_left_11[1] + self.principal_button_size[1]
        ):
            self.button_color11 = self.hover_botton_color_continue
            self.sobre = 11
        else:
            self.button_color11 = "#A4715C"

    def paint_left(self, index: int):
        sf = pygame.Surface(self.secondary_buttons)
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
        pygame.draw.polygon(
            sf,
            "#ffffff",
            [
                (instance.windows_size[0] / 32, instance.windows_size[1] / 72),
                (instance.windows_size[0] / 128, instance.windows_size[1] / 28.8),
                (instance.windows_size[0] / 32, instance.windows_size[1] / 18),
            ],
        )

        return sf

    def paint_right(self, index: int):
        sf = pygame.Surface(self.secondary_buttons)
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
        pygame.draw.polygon(
            sf,
            "#ffffff",
            [
                (instance.windows_size[0] / 128, instance.windows_size[1] / 72),
                (instance.windows_size[0] / 32, instance.windows_size[1] / 28.8),
                (instance.windows_size[0] / 128, instance.windows_size[1] / 18),
            ],
        )

        return sf

    def principal_button(self, index: int):
        sf = pygame.Surface(self.principal_button_size)
        if index == 11:
            sf.fill(self.button_color11)
        box_size = sf.get_size()
        end = self.font.render("Continuar", True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 4)
        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 2 - end.get_size()[0] / 2,
                box_pos[1] / 0.6,
            ),
        )
        return sf

    def selection(self):
        if self.sobre == 1 and self.index_screen_resolution > 0:
            self.index_screen_resolution -= 1
        if (
            self.sobre == 6
            and self.index_screen_resolution < len(self.screen_resolution) - 1
        ):
            self.index_screen_resolution += 1
        if self.sobre == 2 and self.quantity_players > 2:
            self.quantity_players -= 1
        if self.sobre == 7 and self.quantity_players < 6:
            self.quantity_players += 1
        if self.sobre == 3 and self.quantity_bots > 0:
            self.quantity_bots -= 1
        if (
            self.sobre == 8
            and self.quantity_bots < self.quantity_players
        ):
            self.quantity_bots += 1
        if self.sobre == 4 and self.quantity_rounds > 1:
            self.quantity_rounds -= 1
        if self.sobre == 9 and self.quantity_rounds < 20:
            self.quantity_rounds += 1
        if (
            self.sobre == 5
            and self.index_environment_effects.value > 0
        ):
            self.index_environment_effects = AmbientEffect(
                self.index_environment_effects.value - 1
            )
        if (
            self.sobre == 10
            and self.index_environment_effects.value < len(self.environment_effects) - 1
        ):
            self.index_environment_effects = AmbientEffect(
                self.index_environment_effects.value + 1
            )
        self.clock.tick(constants.FPS / 15)
