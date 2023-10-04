import math
from os import listdir

import pygame


class Speedometer:
    size: int
    min: int
    max: int
    actual: int

    def __init__(self, size: int):
        self.min = 0
        self.max = 400
        self.inc = 5
        self.start_angle = math.radians(200)
        self.end_angle = math.radians(-20)
        self.font = pygame.font.Font("./resources/fonts/Roboto.ttf", 30)
        self.font.set_bold(True)
        print(self.start_angle)
        print(self.end_angle)
        self.size = size

    def draw(self) -> pygame.Surface:
        surface = pygame.Surface((self.size, self.size))

        pygame.draw.circle(surface, "#464646", (250, 250), 250, 40)
        pygame.draw.circle(surface, "#232323", (250, 250), 210)

        angle = (self.end_angle - self.start_angle) / (self.max - self.min)
        for i in range(self.min, self.max + 1, self.inc):
            x, y = 250, 250
            a = self.start_angle + (i - self.min) * angle
            ax, ay = math.cos(a), math.sin(a)
            if i % 100 == 0:
                pygame.draw.line(
                    surface,
                    "#cccccc",
                    (x + (x - 70) * ax, y - (y - 70) * ay),
                    (x + (x - 40) * ax, y - (y - 40) * ay),
                    2,
                )
                if a > math.radians(90):
                    num = self.font.render(f"{i}", True, "#ffffff")
                    surface.blit(
                        num,
                        (x + (x - 70) * ax, y - (y - 70) * ay),
                    )
                elif a == math.radians(90):
                    num = self.font.render(f"{i}", True, "#ffffff")
                    surface.blit(
                        num,
                        (
                            x + (x - 70) * ax - num.get_size()[0] / 2,
                            y - (y - 70) * ay,
                        ),
                    )
                else:
                    num = self.font.render(f"{i}", True, "#ffffff")
                    surface.blit(
                        num,
                        (x + (x - 70) * ax - num.get_size()[0], y - (y - 70) * ay),
                    )

            else:
                pygame.draw.line(
                    surface,
                    "#cccccc",
                    (x + (x - 60) * ax, y - (y - 60) * ay),
                    (x + (x - 40) * ax, y - (y - 40) * ay),
                    2,
                )

        self.font.set_bold(False)
        sp = self.font.render("Shoot Speed", True, "#ffffff")
        self.font.set_bold(True)

        surface.blit(sp, (250 - sp.get_size()[0] / 2, 350))

        pygame.draw.line(
            surface,
            "red",
            (250, 250),
            (
                250 + 60 * math.cos(self.start_angle + angle * self.actual),
                250 - 60 * math.sin(self.start_angle + angle * self.actual),
            ),
            16,
        )
        pygame.draw.line(
            surface,
            "red",
            (
                250 + 60 * math.cos(self.start_angle + angle * self.actual),
                250 - 60 * math.sin(self.start_angle + angle * self.actual),
            ),
            (
                250 + 140 * math.cos(self.start_angle + angle * self.actual),
                250 - 140 * math.sin(self.start_angle + angle * self.actual),
            ),
            10,
        )
        pygame.draw.circle(surface, "red", (250, 250), 10)

        return surface
