import random

import pygame

from caches import font_cache
import constants
from draw import Drawable


class WinnerScreen(Drawable):
    """
    Esta clase se encarga de dibujar en pantalla un mensaje anunciando el
    ganador, mostrando su puntaje y el correspondiente tanque para una mejor
    distinción.
    """

    def __init__(self, tank_game):
        """
        Constructor que inicializa todas los elementos necesarios para monstrar
        el mensaje de victoria.
        """
        self.font = font_cache["Roboto.ttf", 20]
        self.tank_game = tank_game
        self.text_winner_info = None
        self.text_winner_life = None
        self.text_winner_score = None
        self.text_life1 = None
        self.text_life2 = None
        self.font100 = font_cache["Roboto.ttf", 150]
        self.font100.set_bold(True)
        self.font100.set_italic(True)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-5, -1)
        random.normalvariate()
        self.radio = 2

    def winner_mensaje(self, screen: pygame.surface.Surface):
        """
        Esta función crea el mensaje de ganador, haciendo una ventana que
        muestre toda la información que el ganador sacó de la partida,
        incluyendo su puntaje, y como adicional se dibuja el tanque del color
        ganador
        """
        if self.tank_game.winner is None:
            # Si no hay ganador, no se ejecuta
            return

        center = (360, 120)
        transparency = 220
        rect_surface = pygame.Surface((900, 400))
        rect_surface.fill("#64BA1E")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = constants.H_WINNER
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
        position_winner_life = pygame.Vector2(550, 120)
        screen.blit(self.text_winner_life, position_winner_life)
        points = self.tank_game.tanks[self.tank_game.winner].player.points
        self.font.set_bold(True)
        self.text_winner_life = self.font.render(
            f"Puntaje: {points} puntos ",
            True,
            "white",
        )
        self.font.set_bold(False)
        position_winner_score = pygame.Vector2(560, 270)
        screen.blit(self.text_winner_life, position_winner_score)
        pygame.draw.rect(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
            pygame.Rect(
                constants.TANK_WINNER[0] - 25, constants.TANK_WINNER[1] - 10, 50, 35
            ),
        )
        pygame.draw.rect(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
            pygame.Rect(
                constants.TANK_WINNER[0] - 62.5,
                constants.TANK_WINNER[1] + 25,
                125,
                50,
            ),
        )
        pygame.draw.rect(
            screen,
            constants.GRAY,
            pygame.Rect(
                constants.TANK_WINNER[0] - 62.5,
                constants.TANK_WINNER[1] + 75,
                125,
                20,
            ),
        )

        for i in range(6):
            pygame.draw.circle(
                screen,
                constants.BLACK,
                (
                    constants.TANK_WINNER[0] - 60 + 25 * i,
                    constants.TANK_WINNER[1] + 90,
                ),
                15,
            )

        pygame.draw.line(
            screen,
            self.tank_game.tanks[self.tank_game.winner].color,
            constants.TANK_WINNER,
            (550, 300),
            15,
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Función que en el caso de que haya un ganador y aún no se muestre en
        pantalla, redigirá hacia otra función donde el mensaje se creará y será
        presentado al usuario por medio de la interfaz.
        """
        if self.tank_game.winner is not None:
            self.winner_mensaje(screen)
