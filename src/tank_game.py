from random import shuffle

import pygame
from pygame.font import Font

import constants
from caches import audio_cache, image_cache, font_cache
from context import Context
from exit_requested import ExitRequested, RestartRequested
from final_winner import FinalWinner
from menu import Menu, MenuStatus
from option_menu import OptionMenu
from option_menu import OptionMenuStatus
from player import Player
from positions_table import PositionTable
from round import Round


class TankGame:
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
        self.shop_menu = None
        self.finalWinner = FinalWinner()

    def create_players(self):
        """This method creates each player giving them different colors."""
        colors = self.create_different_colors(self.context.number_of_players)
        for color in colors:
            self.context.players.append(
                Player(
                    color,
                )
            )

    @staticmethod
    def create_different_colors(n: int) -> list[pygame.Color]:
        """This method creates a random color and returns it."""
        red = [
            *map(
                lambda val: int(((val / n) * 255 + (((val + 1) / n) * 255)) / 2),
                range(n),
            )
        ]
        green = [
            *map(
                lambda val: int(((val / n) * 255 + (((val + 1) / n) * 255)) / 2),
                range(n),
            )
        ]
        blue = [
            *map(
                lambda val: int(((val / n) * 255 + (((val + 1) / n) * 255)) / 2),
                range(n),
            )
        ]

        shuffle(red)
        shuffle(green)
        shuffle(blue)

        colors = []
        for r, g, b in zip(red, blue, green):
            colors.append(pygame.Color(r, g, b))

        return colors

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
                    self.replace()
            if show_instructions:
                self.show_instructions(self.context.screen)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    break

            pygame.display.flip()
            self.context.clock.tick(constants.FPS)
            self.context.fps = self.context.clock.get_fps()

    def replace(self):
        """This method replaces the default configuration with the new one."""
        self.context.number_of_players = self.menu_option.quantity_players
        for j, item in enumerate(self.screen_resolution):
            if j == self.menu_option.index_screen_resolution:
                self.context.windows_size = item
        self.context.number_of_bots = self.menu_option.quantity_bots
        self.context.number_of_rounds = self.menu_option.quantity_rounds
        self.context.type_of_effect = self.menu_option.index_environment_effects

    def start(self) -> None:
        """This method start the game covers the entire process."""
        soundtrack = audio_cache["sounds/inGame.mp3"]
        try:
            self.start_menu()
            while True:
                try:
                    soundtrack.play()

                    self.create_players()

                    for _ in range(self.context.number_of_rounds):
                        for player in self.context.players:
                            player.money += 10000
                        current_round = Round()
                        current_round.start()

                    self.finalWinner.final_winner()
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_SPACE]:
                        self.position_table = PositionTable(self.context.screen)
                        self.position_table.show_positions()

                except RestartRequested:
                    pass

                self.context.players.clear()
                soundtrack.stop()

        except ExitRequested:
            return
