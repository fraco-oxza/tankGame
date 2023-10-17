from typing import Optional

import pygame
from pygame.font import Font

from caches import font_cache, audio_cache
import constants
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

    def __init__(self, screen: pygame.Surface):
        self.button_reset_position = pygame.Vector2(200, 100)
        self.fontExit = font_cache["Roboto.ttf", 25]
        self.fontRestart = font_cache["Roboto.ttf", 25]
        self.fontBack = font_cache["Roboto.ttf", 25]
        self.storm = SnowStorm()
        self.botton_color1 = "#2E3440"
        self.botton_color2 = "#2E3440"
        self.botton_color3 = "#2E3440"
        self.hover_botton_color = "#3b4252"
        self.screen = screen
        self.sobre = None
        self.clock = pygame.time.Clock()
        self.box_size = (200, 100)

    def tick(self, dt: float):
        self.storm.tick(dt)

    def render(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return InGameMenuStatus.EXIT

            self.screen.fill("#434C5E")
            size = self.screen.get_size()
            self.box_pos = ((size[0] - self.box_size[0]) / 2, size[1] / 2)
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
                (constants.WINDOWS_SIZE[0] // 4, constants.WINDOWS_SIZE[1] / 2.5),
            )
            self.screen.blit(
                self.restart("Salir"),
                (constants.WINDOWS_SIZE[0] // 2.3, constants.WINDOWS_SIZE[1] / 2.5),
            )
            self.screen.blit(
                self.restart("Volver"),
                (constants.WINDOWS_SIZE[0] // 1.6, constants.WINDOWS_SIZE[1] / 2.5),
            )

            self.storm.tick(1.0 / constants.FPS)
            self.clock.tick(constants.FPS)
            pygame.display.flip()

    def handle_input(self, mouse: pygame.Vector2):
        restart_pos = (constants.WINDOWS_SIZE[0] // 4, constants.WINDOWS_SIZE[1] / 2)
        if restart_pos[0] < mouse.x < (restart_pos[0] + 200) and restart_pos[
            1
        ] - self.button_reset_position[1] < mouse.y < (
            restart_pos[1] + self.button_reset_position[1]
        ):
            self.botton_color1 = self.hover_botton_color
            self.sobre = 1
        else:
            self.botton_color1 = "#2E3440"
        exit_pos = (constants.WINDOWS_SIZE[0] // 2.3, constants.WINDOWS_SIZE[1] / 2)
        if exit_pos[0] < mouse.x < (exit_pos[0] + 200) and exit_pos[
            1
        ] - self.button_reset_position[1] < mouse.y < (
            exit_pos[1] + self.button_reset_position[1]
        ):
            self.botton_color2 = self.hover_botton_color
            self.sobre = 2
        else:
            self.botton_color2 = "#2E3440"
        back_pos = (constants.WINDOWS_SIZE[0] // 1.6, constants.WINDOWS_SIZE[1] / 2)
        if back_pos[0] < mouse.x < (back_pos[0] + 200) and back_pos[
            1
        ] - self.button_reset_position[1] < mouse.y < (
            back_pos[1] + +self.button_reset_position[1]
        ):
            self.botton_color3 = self.hover_botton_color
            self.sobre = 3
        else:
            self.botton_color3 = "#2E3440"

    def start_menu(self) -> int:
        return self.render()

    def restart(self, mensaje: str):
        sf = pygame.Surface(self.button_reset_position)
        box_size = sf.get_size()
        end = self.fontRestart.render(mensaje, True, "#B48EAD")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 2.5)
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
