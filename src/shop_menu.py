from typing import Optional
import time
import pygame
from pygame.font import Font

import constants
from caches import audio_cache
from caches import font_cache
from caches import image_cache
from cannonballs import CannonballType
from context import instance
from inputs import check_running
from tank import Tank


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
    Ammo60 = 0
    Ammo80 = 0
    Ammo105 = 0

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
        self.ammunition = {}
        self.Ammo60 = 0
        self.Ammo80 = 0
        self.Ammo105 = 0
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
        self.money_player = None

    def generate_shop(self, tank: Tank, i):
        self.money_player = tank.player.money
        contador60mm = 0
        contador80mm = 0
        contador105mm = 0
        while True:
            check_running()
            self.screen.blit(self.image, self.image_rect.topleft)
            self.screen.blit(self.cannonball_buttons("$1000"), (460, 180))
            self.screen.blit(self.cannonball_buttons("$2500"), (460, 247))
            self.screen.blit(self.cannonball_buttons("$4000"), (460, 315))
            self.screen.blit(self.reset_shopping("Reset"), (805, 178))
            self.screen.blit(self.buy_ammo("Buy"), (765, 395))
            money = self.principal_font.render(f"${self.money_player}", True, "#ffffff")
            quantity60mm = self.money_font.render(f"{contador60mm}", True, "#ffffff")
            quantity80mm = self.money_font.render(f"{contador80mm}", True, "#ffffff")
            quantity105mm = self.money_font.render(f"{contador105mm}", True, "#ffffff")
            self.screen.blit(quantity60mm, (700, 185))
            self.screen.blit(quantity80mm, (700, 255))
            self.screen.blit(quantity105mm, (700, 320))
            self.screen.blit(money, (580, 120))
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            self.handle_input(mouse)
            if pygame.mouse.get_pressed()[0]:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                if self.upon == 1:
                    if self.money_player >= 1000:
                        self.money_player -= 1000
                        self.Ammo60 += 1
                        contador60mm += 1
                        instance.players[i].money -= 1000
                        print(self.Ammo60)
                if self.upon == 2:
                    if self.money_player >= 2500:
                        self.money_player -= 2500
                        self.Ammo80 += 1
                        contador80mm += 1
                        instance.players[i].money -= 2500
                        print(self.Ammo80)
                if self.upon == 3:
                    if self.money_player >= 4000:
                        self.money_player -= 4000
                        self.Ammo105 += 1
                        contador105mm += 1
                        instance.players[i].money -= 4000
                        print(self.Ammo105)
                if self.upon == 4:
                    self.money_player = tank.player.money
                    self.Ammo60 = 0
                    self.Ammo80 = 0
                    self.Ammo105 = 0
                if self.upon == 5:
                    self.ammunition = {
                        CannonballType.MM60: self.Ammo60,
                        CannonballType.MM80: self.Ammo80,
                        CannonballType.MM105: self.Ammo105,
                    }
                    tank.player.ammunition = self.ammunition
                    return ShopStatus.BUY
            self.clock.tick(constants.FPS / 7)
            pygame.display.flip()

    def start_shop(self, tank: Tank, i):
        return self.generate_shop(tank, i)

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

    def show_buy(self, tank: Tank):
        transparency = 220
        rect_surface = pygame.Surface(
            (instance.windows_size[0] / 1.22, instance.windows_size[1] / 1.8)
        )
        rect_surface.fill("#000000")
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = (
            instance.windows_size[0] / 10.66,
            instance.windows_size[1] / 12,
        )
        self.screen.blit(rect_surface, (rect_x1, rect_y1))
        pygame.draw.rect(
            self.screen,
            tank.color,
            pygame.Rect(
                instance.windows_size[0] / 1.96 - instance.windows_size[0] / 51.2,
                instance.windows_size[1] / 2.05 - instance.windows_size[1] / 72,
                instance.windows_size[0] / 25.6,
                instance.windows_size[1] / 20.57,
            ),
        )
        pygame.draw.rect(
            self.screen,
            tank.color,
            pygame.Rect(
                instance.windows_size[0] / 1.96 - instance.windows_size[0] / 20.48,
                instance.windows_size[1] / 2.05 + instance.windows_size[1] / 28.8,
                instance.windows_size[0] / 10.24,
                instance.windows_size[1] / 14.4,
            ),
        )
        pygame.draw.rect(
            self.screen,
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
                self.screen,
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
            self.screen,
            tank.color,
            (instance.windows_size[0] / 1.96, instance.windows_size[1] / 2.05),
            (instance.windows_size[0] / 2.32, instance.windows_size[1] / 2.4),
            int(instance.windows_size[0] / 51.2),
        )
        pygame.display.flip()
