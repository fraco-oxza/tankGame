from typing import Optional

import pygame
from pygame.font import Font

import constants
from caches import font_cache, audio_cache, image_cache
from snow_storm import SnowStorm


class InGameMenuStatus:
    EXIT = 0
    CONTINUE = 1
    RESTART = 2


class InGameMenu:
    fontExit: Font
    fontBack: Font
    fontRestart: Font
    storm: SnowStorm
    box_size = pygame.Vector2
    box_pos: Optional[tuple[float, float]]
    botton_color1: str
    botton_color2: str
    botton_color3: str
    hover_botton_color: str
    button_reset_position = pygame.Vector2
    sobre: Optional[int]

    def __init__(self, screen: pygame.Surface, storm: SnowStorm):
        self.button_reset_position = pygame.Vector2(300, 48)
        self.fontExit = font_cache["Roboto.ttf", 25]
        self.fontRestart = font_cache["Roboto.ttf", 25]
        self.fontBack = font_cache["Roboto.ttf", 25]
        self.storm = storm
        self.botton_color1 = "#73726E"
        self.botton_color2 = "#73726E"
        self.botton_color3 = "#73726E"
        self.hover_botton_color = "#736868"
        self.screen = screen
        self.sobre = None
        self.clock = pygame.time.Clock()
        image_size = pygame.Vector2(
            constants.WINDOWS_SIZE[0], constants.WINDOWS_SIZE[1]
        )
        self.image = pygame.transform.scale(
            image_cache["images/Control.png"], image_size
        )
        self.sky_rect = self.image.get_rect()

    def tick(self, dt: float):
        self.storm.tick(dt)

    def render(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return InGameMenuStatus.EXIT

            self.screen.blit(self.image, self.sky_rect.topleft)
            transparency = 150
            rect_surface = pygame.Surface(
                (constants.WINDOWS_SIZE[0], constants.WINDOWS_SIZE[1])
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
            self.storm.draw(self.screen)
            self.screen.blit(
                self.restart("Reiniciar Partida"),
                (constants.WINDOWS_SIZE[0] // 2.6, constants.WINDOWS_SIZE[1] / 2.37),
            )
            self.screen.blit(
                self.restart("Salir"),
                (constants.WINDOWS_SIZE[0] // 2.6, constants.WINDOWS_SIZE[1] / 2),
            )
            self.screen.blit(
                self.restart("Volver"),
                (constants.WINDOWS_SIZE[0] // 2.6, constants.WINDOWS_SIZE[1] / 2.9),
            )

            self.storm.tick(1.0 / constants.FPS)
            self.clock.tick(constants.FPS)
            pygame.display.flip()

    def handle_input(self, mouse: pygame.Vector2):
        restart_pos = (
            constants.WINDOWS_SIZE[0] // 2.6,
            constants.WINDOWS_SIZE[1] / 2.37,
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
        exit_pos = (constants.WINDOWS_SIZE[0] // 2.6, constants.WINDOWS_SIZE[1] / 2)
        if exit_pos[0] < mouse.x < (
            exit_pos[0] + self.button_reset_position[0]
        ) and exit_pos[1] < mouse.y < (exit_pos[1] + self.button_reset_position[1]):
            self.botton_color2 = self.hover_botton_color
            self.sobre = 2
        else:
            self.botton_color2 = "#73726E"
        back_pos = (constants.WINDOWS_SIZE[0] // 2.6, constants.WINDOWS_SIZE[1] / 2.9)
        if back_pos[0] < mouse.x < (
            back_pos[0] + self.button_reset_position[0]
        ) and back_pos[1] < mouse.y < (back_pos[1] + self.button_reset_position[1]):
            self.botton_color3 = self.hover_botton_color
            self.sobre = 3
        else:
            self.botton_color3 = "#73726E"

    def start_menu(self) -> int:
        return self.render()

    def restart(self, mensaje: str):
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
