import pygame

import constants
from caches import font_cache, image_cache
from context import instance
from inputs import check_running


def draw_tank(screen, tank):
    """
    This method draws the winning tank on the screen.
    The position and size of each tank element are calculated in relation to the dimensions of the game window.
    """
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


class FinalWinner:
    """
    This class is responsible for presenting the final winner or tie screen.
    """

    def __init__(self):
        self.instance = instance
        self.font = font_cache["Roboto.ttf", int(self.instance.windows_size[0] / 51.2)]
        self.tanks = self.instance.players

    def final_winner(self):
        """
        This method shows the winner or tie window after sorting them.
        """
        self.sort_tanks()
        tank = self.tanks[0]
        while True:
            if not self.check_tie():
                screen = self.instance.screen
                background = image_cache["images/finalWinner.jpg"]
                self.tabla_posiciones(background, screen)
                draw_tank(screen, tank)
            else:
                screen = self.instance.screen
                background = image_cache["images/tie.jpg"]
                self.tabla_posiciones(background, screen)

            pygame.display.flip()
            check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                return
            instance.clock.tick(constants.FPS)
            instance.fps = instance.clock.get_fps()

    def tabla_posiciones(self, background, screen):
        """
        This method displays a text on the screen to go to the leaderboard and Scale the image.
        """
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

    def sort_tanks(self):
        """
        This method orders the tanks from those who committed the most murders to those who committed the least.
        """
        self.tanks = sorted(self.tanks, key=lambda player: player.murders, reverse=True)

    def check_tie(self):
        """
        This method checks if there is a tie
        """
        return self.tanks[0].murders == self.tanks[1].murders
