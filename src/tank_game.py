import random
from random import randint

import pygame
from caches import audio_cache
from context import Context
from exit_requested import ExitRequested, RestartRequested
from player import Player
from round import Round
from menu import Menu
import constants
from menu import MenuStatus
from option_menu import OptionMenu
from option_menu import OptionMenuStatus

class TankGame:
    players: list[Player]

    def __init__(self, context: Context) -> None:
        """
        constructor that initializes each element within the game, in
        addition to starting the window itself of the game.
        """
        self.context = context
        self.players = []
        self.menu = Menu(self.context.screen)
        self.menu_option = OptionMenu(self.context.screen)

    def create_player(self):
        # TODO: crear un menu para que ingrese el nombre, y un color
        self.players.append(
            Player(
                str(random.randint(0, 1000)),
                pygame.Color(randint(1, 200), randint(1, 200), randint(1, 200)),
            )
        )

    def game_brief(self):
        pass

    def start_menu(self):
        """This method takes care of the menu music and the start button click."""
        soundtrack = audio_cache["sounds/inicio.mp3"]
        soundtrack.play()
        i = 0
        while True:
            if self.menu.show_menu() == MenuStatus.start:
                soundtrack.stop()
                click = audio_cache["sounds/click.mp3"]
                click.play()
                break
            if self.menu.show_menu() == MenuStatus.options:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                if self.menu_option.start_option_menu() == OptionMenuStatus.CONTINUE:
                    click = audio_cache["sounds/click.mp3"]
                    click.play()
                    continue

            pygame.display.flip()
            self.context.clock.tick(constants.FPS)
            self.context.fps = self.context.clock.get_fps()

    def start(self) -> None:
        soundtrack = audio_cache["sounds/inGame.mp3"]
        while True:
            try:
                self.start_menu()
                soundtrack.play()
                print("empezo partida", self.context.map_size)
                for _ in range(self.context.number_of_players):
                    self.create_player()

                for i in range(self.context.number_of_rounds):
                    print(f"round {i}")
                    current_round = Round(self.players)
                    current_round.start()

                self.game_brief()

                print("termino")
            except ExitRequested:
                break
            except RestartRequested:
                pass

            self.players = []
            soundtrack.stop()
