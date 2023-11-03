from typing import Optional
import pygame
from caches import font_cache, image_cache
from context import instance
from inputs import check_running
from caches import audio_cache
import constants


class PositionTableButton:
    VOLVER_A_JUGAR = 1


class PositionTable:
    table: pygame.Vector2
    screen: pygame.Surface

    def __init__(self, screen: pygame.Surface):
        print(instance.windows_size[0])
        print(instance.windows_size[1])
        self.table = pygame.Vector2(
            instance.windows_size[0] / 1.5, instance.windows_size[1] / 12
        )
        self.button_position = pygame.Vector2(
            instance.windows_size[0] / 4.26, instance.windows_size[1] / 8
        )
        self.font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.fontTittle = font_cache["Roboto.ttf", int(instance.windows_size[0] / 35)]
        self.screen = screen
        self.round = None
        self.color = "#2E3440"
        self.color1 = "#2E3440"
        self.hover_color = "#3b4252"
        self.sobre = 0

    def draw_blocks(self):
        while True:
            check_running()
            image_size = pygame.Vector2(
                instance.windows_size[0], instance.windows_size[1]
            )
            self.image = pygame.transform.scale(
                image_cache["images/Tablero.png"], image_size
            )
            self.sky_rect = self.image.get_rect()
            self.screen.blit(self.image, self.sky_rect.topleft)
            transparency = 150
            rect_surface = pygame.Surface(
                (instance.windows_size[0], instance.windows_size[1])
            )
            rect_surface.fill("#000000")
            rect_surface.set_alpha(transparency)
            rect_x1, rect_y1 = (0, 0)
            self.screen.blit(rect_surface, (rect_x1, rect_y1))
            msj = self.fontTittle.render("Tabla de posiciones", True, "#ffffff")
            self.screen.blit(
                msj, (instance.windows_size[0] / 2.61, instance.windows_size[1] / 36)
            )
            deads = self.font.render("Jugador", True, "#ffffff")
            self.screen.blit(
                deads, (instance.windows_size[0] / 3.2, instance.windows_size[1] / 8)
            )
            deads = self.font.render("Asesinatos cometidos", True, "#ffffff")
            self.screen.blit(
                deads, (instance.windows_size[0] / 1.82, instance.windows_size[1] / 8)
            )
            sum = 0
            self.bubble_sort()
            for i in range(len(instance.players)):
                sf = self.generate_surface(str(instance.players[i].deads))
                self.position_box(sf, sum)
                sf_number = self.ranking(i)
                self.position_number(sf_number, sum)
                sf_tank = self.tank(i)
                self.position_tank(sf_tank, sum)
                sum += instance.windows_size[1] / 10.28
            self.screen.blit(
                self.button(),
                (instance.windows_size[0] / 2.56, instance.windows_size[1] / 1.2),
            )
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            self.handle_input(mouse)
            if pygame.mouse.get_pressed()[0]:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                if self.sobre == 1:
                    return PositionTableButton.VOLVER_A_JUGAR
            pygame.display.flip()

    def show_positions(self):
        return self.draw_blocks()

    def generate_surface(self, mensaje: str):
        """
        Function responsible for creating the surface that represents the button,
        in addition to writing the message of each button in the center of each surface
        """
        sf = pygame.Surface(self.table)
        box_size = sf.get_size()
        sf.fill(self.color)
        end = self.font.render(mensaje, True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 4)
        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 1.5 - end.get_size()[0] / 2,
                box_pos[1] / 1.2,
            ),
        )
        return sf

    def position_box(self, sf: pygame.surface.Surface, sum):
        self.screen.blit(
            sf, (instance.windows_size[0] / 5.12, instance.windows_size[1] / 4.8 + sum)
        )

    def position_tank(self, sf: pygame.surface.Surface, sum):
        self.screen.blit(
            sf, (instance.windows_size[0] / 3.12, instance.windows_size[1] / 4.8 + sum)
        )

    def position_number(self, sf: pygame.surface.Surface, sum):
        self.screen.blit(
            sf, (instance.windows_size[0] / 4.92, instance.windows_size[1] / 4.8 + sum)
        )

    def button(self):
        sf = pygame.Surface(self.button_position)
        box_size = sf.get_size()
        end = self.font.render("Volver a Jugar", True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 2.5)
        sf.fill(self.color1)

        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 2 - end.get_size()[0] / 2,
                box_pos[1] / 1.2,
            ),
        )
        return sf

    def handle_input(self, mouse: pygame.Vector2):
        """
        Function responsible for identifying which button the user pressed by clicking on one of the buttons.
        It is also responsible for changing the color of the button when the mouse passes over a button,
        otherwise it remains in its original color
        """
        restart_pos = (instance.windows_size[0] / 2.56, instance.windows_size[1] / 1.2)
        if restart_pos[0] < mouse.x < (
            restart_pos[0] + self.button_position[0]
        ) and restart_pos[1] < mouse.y < (restart_pos[1] + self.button_position[1]):
            self.color1 = self.hover_color
            self.sobre = 1
        else:
            self.color1 = "#2E3440"

    def tank(self, j):
        width = instance.windows_size[0] / 18.28
        height = instance.windows_size[1] / 13
        sf = pygame.Surface((width, height))
        sf.fill(self.color)
        pygame.draw.rect(
            sf,
            instance.players[j].color,
            pygame.Rect(
                width / 3 + width / 9.16,
                height / 1.5 - height / 13.33,
                width / 6.6,
                height / 11.42,
            ),
        )
        pygame.draw.rect(
            sf,
            instance.players[j].color,
            pygame.Rect(
                width / 3,
                height / 1.5,
                width / 2.64,
                height / 8,
            ),
        )
        pygame.draw.rect(
            sf,
            constants.GRAY,
            pygame.Rect(
                width / 3,
                height / 1.5 + height / 8,
                width / 2.64,
                height / 20,
            ),
        )

        for i in range(6):
            pygame.draw.circle(
                sf,
                constants.BLACK,
                (
                    width / 3 + width / 13.2 * i,
                    height / 1.5 + height / 5.71,
                ),
                width / 26.66,
            )

        pygame.draw.line(
            sf,
            instance.players[j].color,
            ((width / 3 + width / 5.68), height / 1.5 - height / 15.38),
            ((width / 3 - width / 16.5), height / 1.5 - height / 5.71),
            int(width / 20.625),
        )

        return sf

    def ranking(self, i):
        width = instance.windows_size[0] / 18.28
        height = instance.windows_size[1] / 13
        sf = pygame.Surface((width, height))
        sf.fill(self.color)
        box_size = sf.get_size()
        end = self.font.render(f"{i + 1}°", True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 2.5)

        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 2 - end.get_size()[0] / 2,
                box_pos[1] / 1.2,
            ),
        )
        return sf

    def bubble_sort(self):
        for i in range(len(instance.players)):
            for j in range(len(instance.players) - 1):
                if instance.players[j].deads < instance.players[j + 1].deads:
                    temp = instance.players[j].deads
                    instance.players[j].deads = instance.players[j + 1].deads
                    instance.players[j + 1].deads = temp
