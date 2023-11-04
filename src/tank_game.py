import random
from random import randint

import pygame
from pygame.font import Font
from caches import audio_cache, image_cache, font_cache
from context import Context
from exit_requested import ExitRequested, RestartRequested
from player import Player
from round import Round
from menu import Menu
import constants
from menu import MenuStatus
from option_menu import OptionMenu
from option_menu import OptionMenuStatus
from positions_table import PositionTable
from positions_table import PositionTableButton


class TankGame:
    players: list[Player]
    context: Context
    menu: Menu
    menu_option: OptionMenu
    screen_resolution: list[tuple[int, int]]
    font: Font

    def __init__(self, context: Context) -> None:
        """
        constructor that initializes each element within the game, in
        addition to starting the window itself of the game.
        """
        self.context = context
        self.players = []
        self.menu = Menu(self.context.screen)
        self.menu_option = OptionMenu(self.context.screen)
        self.screen_resolution = [
            (800, 800),
            (1280, 720),
            (1366, 768),
            (1600, 900),
            (1920, 1080),
        ]
        self.font = font_cache["Roboto.ttf", int(self.context.windows_size[0] // 53.33)]
        self.position_table = PositionTable(self.context.screen)

    def create_player(self):
        # TODO: crear un menu para que ingrese el nombre, y un color
        self.context.players.append(
            Player(
                str(random.randint(0, 1000)),
                pygame.Color(randint(1, 200), randint(1, 200), randint(1, 200)),
            )
        )

    def game_brief(self):
        pass

    def show_instructions(self, screen: pygame.surface.Surface):
        """
        This function allows you to display an image at the start of the game with the
        necessary instructions for the players
        """
        screen.fill("#3C0384")

        instructions = image_cache["images/instructions.png"]
        instructions = pygame.transform.scale(instructions, self.context.windows_size)
        rect = instructions.get_rect()
        size = rect.size

        screen.blit(
            instructions,
            (
                self.context.windows_size[0] / 2 - size[0] / 2,
                self.context.windows_size[1] / 2 - size[1] / 2,
            ),
        )
        out_text = self.font.render(
            "Presione espacio para continuar",
            True,
            "white",
        )
        size = out_text.get_rect().size
        screen.blit(
            out_text,
            (
                self.context.windows_size[0] - size[0],
                self.context.windows_size[1] - size[1],
            ),
        )
        pygame.display.flip()

    def start_menu(self):
        """This method takes care of the menu music and the start button click."""
        soundtrack = audio_cache["sounds/inicio.mp3"]
        soundtrack.play()
        i = 0
        show_instructions = False
        while True:
            menu = self.menu.show_menu()
            if menu == MenuStatus.start:
                soundtrack.stop()
                click = audio_cache["sounds/click.mp3"]
                click.play()
                show_instructions = True

            if menu == MenuStatus.options:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                self.menu_option = OptionMenu(self.context.screen)
                if self.menu_option.start_option_menu() == OptionMenuStatus.CONTINUE:
                    click = audio_cache["sounds/click.mp3"]
                    click.play()
                    self.Replace()
            if show_instructions:
                self.show_instructions(self.context.screen)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    break

            pygame.display.flip()
            self.context.clock.tick(constants.FPS)
            self.context.fps = self.context.clock.get_fps()

    def Replace(self):
        self.context.number_of_players = self.menu_option.quantity_players
        for j in range(len(self.screen_resolution)):
            if j == self.menu_option.index_screen_resolution:
                self.context.windows_size = self.screen_resolution[j]
        self.context.number_of_bots = self.menu_option.quantity_bots
        self.context.number_of_rounds = self.menu_option.quantity_rounds
        self.context.type_of_effect = self.menu_option.index_environment_effects

    def start(self) -> None:
        soundtrack = audio_cache["sounds/inGame.mp3"]
        while True:
            try:
                self.start_menu()
                soundtrack.play()
                print("empezo partida", self.context.map_size)
                for _ in range(self.context.number_of_players + self.context.number_of_bots):
                    self.create_player()
                for i in range(self.context.number_of_rounds):
                    print(f"round {i}")
                    current_round = Round()
                    current_round.start()

                self.game_brief()
                print("termino")
                self.position_table = PositionTable(self.context.screen)
                if (
                    self.position_table.show_positions()
                    == PositionTableButton.VOLVER_A_JUGAR
                ):
                    pass
            except ExitRequested:
                break
            except RestartRequested:
                pass

            self.players = []
            soundtrack.stop()
