import pygame
from caches import font_cache, image_cache
from context import instance
from inputs import check_running
from caches import audio_cache
import constants
from tank import Tank


class FinalWinner:
    def __init__(self):
        self.instance = instance
        self.font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.tanks = instance.players

    def final_winner(self):
        self.sort_tanks()
        tank = self.tanks[0]
        while True:
            if not self.check_tie():
                screen = self.instance.screen
                background = image_cache["images/finalWinner.jpg"]
                background = pygame.transform.scale(background, self.instance.windows_size)
                rect = background.get_rect()
                size = rect.size
                screen.blit(
                    background,
                    (
                        self.instance.windows_size[0] / 2 - size[0] / 2,
                        self.instance.windows_size[1] / 2 - size[1] / 2,
                    ),
                )
                out_text = self.font.render(
                    "Presione espacio para ver la tabla de posiciones",
                    True,
                    "white",
                )
                size = out_text.get_rect().size
                screen.blit(
                    out_text,
                    (
                        self.instance.windows_size[0] - size[0],
                        self.instance.windows_size[1] - size[1],
                    ),
                )
                pygame.draw.rect(
                    screen,
                    tank.color,
                    pygame.Rect(
                        instance.windows_size[0] / 1.96 - instance.windows_size[0] / 51.2,
                        instance.windows_size[1] / 2.05 - instance.windows_size[1] / 72,
                        instance.windows_size[0] / 25.6,
                        instance.windows_size[1] / 20.57,
                    ),
                )
                pygame.draw.rect(
                    screen,
                    tank.color,
                    pygame.Rect(
                        instance.windows_size[0] / 1.96 - instance.windows_size[0] / 20.48,
                        instance.windows_size[1] / 2.05 + instance.windows_size[1] / 28.8,
                        instance.windows_size[0] / 10.24,
                        instance.windows_size[1] / 14.4,
                    ),
                )
                pygame.draw.rect(
                    screen,
                    constants.GRAY,
                    pygame.Rect(
                        instance.windows_size[0] / 1.96 - instance.windows_size[0] / 20.48,
                        instance.windows_size[1] / 2.05 + instance.windows_size[1] / 9.6,
                        instance.windows_size[0] / 10.24,
                        instance.windows_size[0] / 64,
                    ),
                )

                for i in range(6):
                    pygame.draw.circle(
                        screen,
                        constants.BLACK,
                        (
                            instance.windows_size[0] / 1.96
                            - instance.windows_size[0] / 21.33
                            + instance.windows_size[0] / 51.2 * i,
                            instance.windows_size[1] / 2.05 + instance.windows_size[1] / 8,
                        ),
                        instance.windows_size[0] / 85.33,
                    )

                pygame.draw.line(
                    screen,
                    tank.color,
                    (instance.windows_size[0] / 1.96, instance.windows_size[1] / 2.05),
                    (instance.windows_size[0] / 2.32, instance.windows_size[1] / 2.4),
                    int(instance.windows_size[0] / 51.2),
                )

            pygame.display.flip()
            check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                return
            instance.clock.tick(constants.FPS)
            instance.fps = instance.clock.get_fps()

    def sort_tanks(self):
        self.tanks = sorted(self.tanks, key=lambda player: player.deads, reverse=True)

    def check_tie(self):
        self.sort_tanks()
        equals = False
        if self.tanks[0].deads == self.tanks[1].deads:
            equals = True
        return equals
