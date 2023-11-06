from typing import Optional

import pygame
from pygame.font import Font

from caches import audio_cache
from caches import font_cache
from caches import image_cache
from context import instance
from inputs import check_running
import constants
from player import Player


class ShopStatus:
    C60AMMO = 1
    C80AMMO = 2
    C105AMMO = 3
    RESTART = 4
    BUY = 5


class Shop:
    money_font: Font
    c60_button_color: str
    c80_button_color: str
    c105_button_color: str
    reset_button_color: str
    buy_button_color: str
    hover_button_color: str
    upon: Optional[int]

    def __init__(self, screen: pygame.surface):
        self.clock = pygame.time.Clock()
        self.button_reset_position = pygame.Vector2(
            instance.windows_size[0] / 17, instance.windows_size[1] / 15
        )
        self.ammo_button_reset_position = pygame.Vector2(
            instance.windows_size[0] / 12, instance.windows_size[1] / 18
        )
        self.buy_button_reset_position = pygame.Vector2(
            instance.windows_size[0] / 10, instance.windows_size[1] / 20
        )
        self.money_font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.principal_font = font_cache[
            "Roboto.ttf", int(instance.windows_size[0] / 40)
        ]
        self.c60_button_color = "#A4947A"
        self.c80_button_color = "#A4947A"
        self.c105_button_color = "#A4947A"
        self.reset_button_color = "#A4947A"
        self.buy_button_color = "#A4947A"
        self.hover_button_color = "#8F8069"
        self.upon = None
        self.screen = screen
        image_size = pygame.Vector2(instance.windows_size[0], instance.windows_size[1])
        self.image = pygame.transform.scale(
            image_cache["images/shopmenu.png"], image_size
        )
        self.image_rect = self.image.get_rect()
        self.money_player = 0

    def generate_shop(self, player: Player):
        while True:
            check_running()
            self.money_player = player.money
            self.screen.blit(self.image, self.image_rect.topleft)
            self.screen.blit(self.cannonball_buttons("$1000"), (460, 180))
            self.screen.blit(self.cannonball_buttons("$2500"), (460, 247))
            self.screen.blit(self.cannonball_buttons("$4000"), (460, 315))
            self.screen.blit(self.reset_shopping("Reset"), (805, 178))
            self.screen.blit(self.buy_ammo("Buy"), (765, 395))
            money = self.principal_font.render(f"${self.money_player}", True, "#ffffff")
            self.screen.blit(money, (580, 120))
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            self.handle_input(mouse)
            if pygame.mouse.get_pressed()[0]:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                if self.upon == 1:
                    pass
                if self.upon == 2:
                    pass
                if self.upon == 3:
                    pass
                if self.upon == 4:
                    pass
                if self.upon == 5:
                    return ShopStatus.BUY
            self.clock.tick(constants.FPS)
            pygame.display.flip()

    def start_shop(self, player: Player):
        return self.generate_shop(player)

    def handle_input(self, mouse: pygame.Vector2):
        reset_position = (805, 178)
        if reset_position[0] < mouse.x < (
            reset_position[0] + self.button_reset_position[0]
        ) and reset_position[1] < mouse.y < (
            reset_position[1] + self.button_reset_position[1]
        ):
            self.reset_button_color = self.hover_button_color
            self.upon = 4
        else:
            self.reset_button_color = "#A4947A"
        buy_position = (765, 395)
        if buy_position[0] < mouse.x < (
            buy_position[0] + self.buy_button_reset_position[0]
        ) and buy_position[1] < mouse.y < (
            buy_position[1] + self.buy_button_reset_position[1]
        ):
            self.buy_button_color = self.hover_button_color
            self.upon = 5
        else:
            self.buy_button_color = "#A4947A"
        cannonball60mm_position = (460, 180)
        if cannonball60mm_position[0] < mouse.x < (
            cannonball60mm_position[0] + self.ammo_button_reset_position[0]
        ) and cannonball60mm_position[1] < mouse.y < (
            cannonball60mm_position[1] + self.ammo_button_reset_position[1]
        ):
            self.c60_button_color = self.hover_button_color
            self.upon = 1
        else:
            self.c60_button_color = "#A4947A"
        cannonball80mm_position = (460, 247)
        if cannonball80mm_position[0] < mouse.x < (
            cannonball80mm_position[0] + self.ammo_button_reset_position[0]
        ) and cannonball80mm_position[1] < mouse.y < (
            cannonball80mm_position[1] + self.ammo_button_reset_position[1]
        ):
            self.c80_button_color = self.hover_button_color
            self.upon = 2
        else:
            self.c80_button_color = "#A4947A"
        cannonball105mm_position = (460, 315)
        if cannonball105mm_position[0] < mouse.x < (
            cannonball105mm_position[0] + self.ammo_button_reset_position[0]
        ) and cannonball105mm_position[1] < mouse.y < (
            cannonball105mm_position[1] + self.ammo_button_reset_position[1]
        ):
            self.c105_button_color = self.hover_button_color
            self.upon = 3
        else:
            self.c105_button_color = "#A4947A"

    def cannonball_buttons(self, message: str):
        """
        Function responsible for creating the surface that represents the button,
        in addition to writing the message of each button in the center of each surface
        """
        sf = pygame.Surface(self.ammo_button_reset_position)
        box_size = sf.get_size()
        end = self.money_font.render(message, True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 4)
        if message == "$1000":
            sf.fill(self.c60_button_color)
        elif message == "$2500":
            sf.fill(self.c80_button_color)
        elif message == "$4000":
            sf.fill(self.c105_button_color)

        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 2 - end.get_size()[0] / 2,
                box_pos[1] / 1.2,
            ),
        )
        return sf

    def reset_shopping(self, message: str):
        sf = pygame.Surface(self.button_reset_position)
        box_size = sf.get_size()
        end = self.money_font.render(message, True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 4)
        sf.fill(self.reset_button_color)

        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 2 - end.get_size()[0] / 2,
                box_pos[1] / 1.2,
            ),
        )
        return sf

    def buy_ammo(self, message: str):
        sf = pygame.Surface(self.buy_button_reset_position)
        box_size = sf.get_size()
        end = self.money_font.render(message, True, "#ffffff")
        box_pos = ((box_size[0] - box_size[0]) / 3, box_size[1] / 4)
        sf.fill(self.buy_button_color)

        sf.blit(
            end,
            (
                box_pos[0] + box_size[0] / 2 - end.get_size()[0] / 2,
                box_pos[1] / 3,
            ),
        )
        return sf
