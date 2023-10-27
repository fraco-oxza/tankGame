import random
from random import randint

import pygame

from context import Context
from exit_requested import ExitRequested, RestartRequested
from player import Player
from round import Round


class TankGame:
    players: list[Player]

    def __init__(self, context: Context) -> None:
        """
        constructor that initializes each element within the game, in
        addition to starting the window itself of the game.
        """
        self.context = context
        self.players = []

    def main_menu(self):
        pass

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

    def start(self) -> None:
        while True:
            try:
                print("empezo partida", self.context.map_size)
                self.main_menu()

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
