import random
import pygame

from caches import font_cache
import constants

from draw import Drawable
from context import instance


class WinnerScreen(Drawable):
    """
    This class is responsible for drawing a message on the screen announcing the
    winner, showing his score and the corresponding tank for better
    distinction.
    """

    def __init__(self, tank_game):
        """
        Constructor that initializes all the elements needed to demonstrate
        the message of victory.
        """
        self.font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 64)]
        self.tank_game = tank_game
        self.text_winner_info = None
        self.text_winner_life = None
        self.text_winner_score = None
        self.text_life1 = None
        self.text_life2 = None
        self.font100 = font_cache["Roboto.ttf", int(instance.windows_size[0] // 8.53)]
        self.font100.set_bold(True)
        self.font100.set_italic(True)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-5, -1)
        self.radio = 2

    def winner_mensaje(self, screen: pygame.surface.Surface):
        """
        This function creates the winner message, making a window that
        show all the information that the winner got from the game,
        including your score, and as an additional color tank is drawn
        winner
        """
        if self.tank_game.winner is None:
            # Si no hay ganador, no se ejecuta
            return

        center = (instance.windows_size[0] / 3.55, instance.windows_size[1] / 6)
        transparency = 220
        rect_surface = pygame.Surface(
            (instance.windows_size[0] / 1.22, instance.windows_size[1] / 1.8)
        )
        rect_surface.fill("#64BA1E")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = (
            instance.windows_size[0] / 10.66,
            instance.windows_size[1] / 12,
        )
        screen.blit(rect_surface, (rect_x1, rect_y1))
        self.text_winner_info = self.font100.render(
            "WINNER",
            True,
            "white",
        )
        screen.blit(self.text_winner_info, center)

        life = self.tank_game.tanks[self.tank_game.winner].life
        self.font.set_bold(True)
        self.text_winner_life = self.font.render(
            f"Vida: {life} puntos de vida",
            True,
            "white",
        )
        self.font.set_bold(False)
        position_winner_life = pygame.Vector2(
            instance.windows_size[0] / 2.32, instance.windows_size[1] / 6
        )
        screen.blit(self.text_winner_life, position_winner_life)
        pygame.draw.rect(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
            pygame.Rect(
                instance.windows_size[0] / 1.96 - instance.windows_size[0] / 51.2,
                instance.windows_size[1] / 2.05 - instance.windows_size[1] / 72,
                instance.windows_size[0] / 25.6,
                instance.windows_size[1] / 20.57,
            ),
        )
        pygame.draw.rect(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
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
            self.tank_game.tanks[self.tank_game.winner].color,
            (instance.windows_size[0] / 1.96, instance.windows_size[1] / 2.05),
            (instance.windows_size[0] / 2.32, instance.windows_size[1] / 2.4),
            int(instance.windows_size[0] / 51.2),
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Function that in the event that there is a winner, and it is not yet shown in
        screen, it will redirect to another function where the message will be created and
        presented to the user through the interface.
        """
        if self.tank_game.winner is not None:
            self.winner_mensaje(screen)
