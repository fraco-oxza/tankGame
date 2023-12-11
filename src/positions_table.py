import pygame

import constants
from caches import audio_cache, font_cache, image_cache
from context import instance
from inputs import check_running
from exit_requested import ExitRequested


class PositionTableButton:
    SALIR = 1


class PositionTable:
    """
    class in charge of displaying the leaderboard at the end of the game, the
    leaderboard is made based on the deaths committed by each of the players
    and the more deaths a player makes, the higher he will be on the
    leaderboard
    """

    table: pygame.Vector2
    screen: pygame.Surface

    def __init__(self, screen: pygame.Surface):
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
        image_size = pygame.Vector2(instance.windows_size[0], instance.windows_size[1])
        self.image = pygame.transform.scale(
            image_cache["images/Tablero.png"], image_size
        )
        self.sky_rect = self.image.get_rect()

    def draw_blocks(self):
        """
        function responsible for displaying all the players on the screen in
        their respective position on the table. Shows the leaderboard until the
        player presses "return to play"
        """
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
            msj = self.fontTittle.render("Tabla de posiciones", True, "#ffffff")
            self.screen.blit(
                msj, (instance.windows_size[0] / 2.61, instance.windows_size[1] / 36)
            )
            deads = self.font.render("Jugador", True, "#ffffff")
            self.screen.blit(
                deads, (instance.windows_size[0] / 3.2, instance.windows_size[1] / 8)
            )
            murders = self.font.render("Asesinatos cometidos", True, "#ffffff")
            self.screen.blit(
                murders, (instance.windows_size[0] / 1.82, instance.windows_size[1] / 8)
            )
            accumulated = 0
            sort_players()
            for k, item in enumerate(instance.players):
                sf = self.generate_surface(str(item.murders))
                self.position_box(sf, accumulated)
                sf_number = self.ranking(k)
                self.position_number(sf_number, accumulated)
                sf_tank = self.tank(k)
                self.position_tank(sf_tank, accumulated)
                accumulated += instance.windows_size[1] / 10.28
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
                    raise ExitRequested
            pygame.display.flip()

    def show_positions(self):
        """
        function in charge of executing the draw_blocks function that is in
        charge of displaying the entire leaderboard and executing the logic
        behind it
        """
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

    def position_box(self, sf: pygame.surface.Surface, val):
        """
        function in charge of showing the containers in which the position in
        which the player and the player's tank will go
        """
        self.screen.blit(
            sf, (instance.windows_size[0] / 5.12, instance.windows_size[1] / 4.8 + val)
        )

    def position_tank(self, sf: pygame.surface.Surface, val):
        """
        function responsible for showing the tank in its respective position
        within the table
        """
        self.screen.blit(
            sf, (instance.windows_size[0] / 3.12, instance.windows_size[1] / 4.8 + val)
        )

    def position_number(self, sf: pygame.surface.Surface, val):
        """function responsible for drawing the leaderboard number"""
        self.screen.blit(
            sf, (instance.windows_size[0] / 4.92, instance.windows_size[1] / 4.8 + val)
        )

    def button(self):
        """
        function responsible for displaying the "play again" button.
        When this is pressed, the leaderboard stops displaying
        """
        sf = pygame.Surface(self.button_position)
        box_size = sf.get_size()
        end = self.font.render("Salir", True, "#ffffff")
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
        Function responsible for identifying which button the user pressed by
        clicking on one of the buttons. It is also responsible for changing the
        color of the button when the mouse passes over a button, otherwise it
        remains in its original color
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
        """
        function responsible for drawing the tanks, so that they are shown in their
        respective position within the table
        """
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
        """
        function behind the logic that shows the place where you were after
        playing against the other players
        """
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


def sort_players():
    """
    function that orders the list of players from largest to smallest based on
    the deaths they committed during the game. It is ordered from highest to
    lowest so that when the entire table is shown, the player who committed the
    most deaths is highest in the table.
    """
    instance.players = sorted(
        instance.players, key=lambda player: player.murders, reverse=True
    )
