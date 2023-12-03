from typing import Optional

import pygame
from pygame.font import Font

import constants
from caches import audio_cache
from caches import font_cache
from caches import image_cache
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

    def __init__(self, screen: pygame.surface.Surface):
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

    def draw_shop(self, contador60mm, contador80mm, contador105mm):
        self.screen.blit(self.image, self.image_rect.topleft)
        self.screen.blit(
            self.cannonball_buttons("$1000"),
            (instance.windows_size[0] / 2.78, instance.windows_size[1] / 4),
        )
        self.screen.blit(
            self.cannonball_buttons("$2500"),
            (instance.windows_size[0] / 2.78, instance.windows_size[1] / 2.91),
        )
        self.screen.blit(
            self.cannonball_buttons("$4000"),
            (instance.windows_size[0] / 2.78, instance.windows_size[1] / 2.28),
        )
        self.screen.blit(
            self.reset_shopping("Reset"),
            (instance.windows_size[0] / 1.59, instance.windows_size[1] / 4.04),
        )
        self.screen.blit(
            self.buy_ammo("Comprar"),
            (instance.windows_size[0] / 1.67, instance.windows_size[1] / 1.82),
        )
        money = self.principal_font.render(f"${self.money_player}", True, "#ffffff")
        quantity60mm = self.money_font.render(f"{contador60mm}", True, "#ffffff")
        quantity80mm = self.money_font.render(f"{contador80mm}", True, "#ffffff")
        quantity105mm = self.money_font.render(f"{contador105mm}", True, "#ffffff")
        self.screen.blit(
            quantity60mm,
            (instance.windows_size[0] / 1.82, instance.windows_size[1] / 3.89),
        )
        self.screen.blit(
            quantity80mm,
            (instance.windows_size[0] / 1.82, instance.windows_size[1] / 2.82),
        )
        self.screen.blit(
            quantity105mm,
            (instance.windows_size[0] / 1.82, instance.windows_size[1] / 2.25),
        )
        self.screen.blit(
            money, (instance.windows_size[0] / 2.20, instance.windows_size[1] / 6)
        )
        pygame.display.flip()

    def generate_shop(self, tank: Tank):
        self.money_player = tank.player.money
        contador60mm = 0
        contador80mm = 0
        contador105mm = 0

        self.draw_shop(contador60mm, contador80mm, contador105mm)
        self.show_buy(tank)

        while True:
            self.money_player = tank.player.money
            check_running()

            self.draw_shop(contador60mm, contador80mm, contador105mm)

            mouse = pygame.Vector2(pygame.mouse.get_pos())
            self.handle_input(mouse)
            if pygame.mouse.get_pressed()[0]:
                click = audio_cache["sounds/click.mp3"]
                click.play()
                if self.upon == 1 and self.money_player >= 1000:
                    self.money_player -= 1000
                    self.Ammo60 += 1
                    contador60mm += 1
                    tank.player.money -= 1000
                if self.upon == 2 and self.money_player >= 2500:
                    self.money_player -= 2500
                    self.Ammo80 += 1
                    contador80mm += 1
                    tank.player.money -= 2500
                if self.upon == 3 and self.money_player >= 4000:
                    self.money_player -= 4000
                    self.Ammo105 += 1
                    contador105mm += 1
                    tank.player.money -= 4000
                if self.upon == 4:
                    tank.player.money = (
                        tank.player.money
                        + self.Ammo60 * 1000
                        + self.Ammo80 * 2500
                        + self.Ammo105 * 4000
                    )
                    self.money_player = (
                        tank.player.money
                        + self.Ammo60 * 1000
                        + self.Ammo80 * 2500
                        + self.Ammo105 * 4000
                    )
                    contador60mm = 0
                    contador80mm = 0
                    contador105mm = 0
                    self.Ammo60 = contador60mm
                    self.Ammo80 = contador80mm
                    self.Ammo105 = contador105mm
                if self.upon == 5:
                    tank.available[0] += self.Ammo60
                    tank.available[1] += self.Ammo80
                    tank.available[2] += self.Ammo105
                    self.Ammo60 = 0
                    self.Ammo80 = 0
                    self.Ammo105 = 0
                    return ShopStatus.BUY
            self.clock.tick(constants.FPS / 12)

    def start_shop(self, tank: Tank):
        return self.generate_shop(tank)

    def handle_input(self, mouse: pygame.Vector2):
        reset_position = (
            instance.windows_size[0] / 1.59,
            instance.windows_size[1] / 4.04,
        )
        if reset_position[0] < mouse.x < (
            reset_position[0] + self.button_reset_position[0]
        ) and reset_position[1] < mouse.y < (
            reset_position[1] + self.button_reset_position[1]
        ):
            self.reset_button_color = self.hover_button_color
            self.upon = 4
        else:
            self.reset_button_color = "#A4947A"
        buy_position = (
            instance.windows_size[0] / 1.67,
            instance.windows_size[1] / 1.82,
        )
        if buy_position[0] < mouse.x < (
            buy_position[0] + self.buy_button_reset_position[0]
        ) and buy_position[1] < mouse.y < (
            buy_position[1] + self.buy_button_reset_position[1]
        ):
            self.buy_button_color = self.hover_button_color
            self.upon = 5
        else:
            self.buy_button_color = "#A4947A"
        cannonball60mm_position = (
            instance.windows_size[0] / 2.78,
            instance.windows_size[1] / 4,
        )
        if cannonball60mm_position[0] < mouse.x < (
            cannonball60mm_position[0] + self.ammo_button_reset_position[0]
        ) and cannonball60mm_position[1] < mouse.y < (
            cannonball60mm_position[1] + self.ammo_button_reset_position[1]
        ):
            self.c60_button_color = self.hover_button_color
            self.upon = 1
        else:
            self.c60_button_color = "#A4947A"
        cannonball80mm_position = (
            instance.windows_size[0] / 2.78,
            instance.windows_size[1] / 2.91,
        )
        if cannonball80mm_position[0] < mouse.x < (
            cannonball80mm_position[0] + self.ammo_button_reset_position[0]
        ) and cannonball80mm_position[1] < mouse.y < (
            cannonball80mm_position[1] + self.ammo_button_reset_position[1]
        ):
            self.c80_button_color = self.hover_button_color
            self.upon = 2
        else:
            self.c80_button_color = "#A4947A"
        cannonball105mm_position = (
            instance.windows_size[0] / 2.78,
            instance.windows_size[1] / 2.28,
        )
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
        transparency = 200
        rect_surface = pygame.Surface(
            (instance.windows_size[0] / 1.22, instance.windows_size[1] / 1.15)
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
        buy_now = self.money_font.render(
            "Compre ya sus balas al por menor", True, "#ffffff"
        )
        self.screen.blit(
            buy_now,
            (instance.windows_size[0] / 2.72, instance.windows_size[1] / 1.44),
        )
        best = self.principal_font.render("Tienda Los Manqueques", True, "#ffffff")
        self.screen.blit(
            best,
            (instance.windows_size[0] / 2.56, instance.windows_size[1] / 10.28),
        )
        press_to_continue = self.money_font.render(
            "Presione espacio para continuar", True, "#ffffff"
        )
        self.screen.blit(
            press_to_continue,
            (instance.windows_size[0] / 1.6, instance.windows_size[1] / 1.10),
        )
        pygame.display.flip()

        while True:
            check_running()
            keys_pressed = pygame.key.get_pressed()
            if not keys_pressed[pygame.K_SPACE]:
                break
            instance.clock.tick(constants.FPS)
            instance.fps = instance.clock.get_fps()

        while True:
            check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                return
            instance.clock.tick(constants.FPS)
            instance.fps = instance.clock.get_fps()
