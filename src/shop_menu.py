from typing import Optional

import pygame
from pygame.font import Font

from caches import audio_cache
from caches import font_cache
from caches import image_cache
from context import instance


class ShopStatus:
    C60AMMO: 1
    C80AMMO: 2
    C105AMMO: 3
    RESTART: 4
    BUY: 5


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
        self.button_reset_position = pygame.Vector2(
            instance.windows_size[0] / 17, instance.windows_size[1] / 15
        )
        self.ammo_button_reset_position = pygame.Vector2(
            instance.windows_size[0] / 7.5, instance.windows_size[1] / 15
        )
        self.buy_button_reset_position = pygame.Vector2(
            instance.windows_size[0] / 10, instance.windows_size[1] / 15
        )
        self.money_font = font_cache["Roboto.ttf", int(instance.windows_size[0] / 51.2)]
        self.c60_button_color = "#FFFFFF"
        self.c80_button_color = "#FFFFFF"
        self.c105_button_color = "#FFFFFF"
        self.reset_button_color = "#FFFFFF"
        self.buy_button_color = "#FFFFFF"
        self.hover_button_color = "#000000"
        self.upon = None
        self.screen = screen
        image_size = pygame.Vector2(instance.windows_size[0], instance.windows_size[1])
        self.image = pygame.transform.scale(
            image_cache["images/shopmenu.png"], image_size
        )
        self.image_rect = self.image.get_rect()

    def generate_shop(self):
        self.screen.blit(self.image, self.image_rect.topleft)
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
                pass
            self.screen.blit(self.cannonball_buttons("$1000"), (615, 180))
            self.screen.blit(self.cannonball_buttons("$2500"), (615, 240))
            self.screen.blit(self.cannonball_buttons("$4000"), (615, 310))
            self.screen.blit(self.reset_shopping("Reset"), (805, 180))
            self.screen.blit(self.buy_ammo("Buy"), (765, 395))

    def start_shop(self):
        return self.generate_shop()

    def handle_input(self, mouse: pygame.Vector2):
        pass

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
                box_pos[1] / 1.2,
            ),
        )
        return sf
