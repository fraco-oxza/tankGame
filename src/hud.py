import math
from typing import Optional

import pygame

import constants
from caches import font_cache, image_cache
from context import instance
from draw import Drawable
from effects import AmbientEffect
from speedometer import Speedometer
from tank import Tank
from wind import Wind


class HUD(Drawable):
    """
    This class is responsible for displaying elements related to the
    information on screen that is not part of the terrain or the game itself.
    """

    tanks: list[Tank]
    left = 100
    top = instance.windows_size[1] - int((3 / 5) * instance.windows_size[1] / 3.6)
    width = 160
    height = 50
    color: dict[int, int]

    def __init__(self, tanks: list[Tank], tank_game, gravity, wind: Optional[Wind]):
        self.tank_game = tank_game
        self.tanks = tanks
        self.hud_image = image_cache["images/Angle.png"]
        self.speedometer = Speedometer(
            int(
                ((2.7 / 5) if instance.windows_size[1] < 1000 else (3 / 5))
                * instance.windows_size[1]
                / 3.6
            )
        )
        self.font = font_cache["Roboto.ttf", int(instance.windows_size[0] // 53.33)]
        self.font30 = font_cache["Roboto.ttf", int(instance.windows_size[0] // 42.6)]
        self.font16 = font_cache["Roboto.ttf", int(instance.windows_size[0] // 80)]
        self.font12 = font_cache["Roboto.ttf", int(instance.windows_size[0] // 106.6)]
        self.text_angle1 = None
        self.text_angle2 = None
        self.text_velocity1 = None
        self.text_velocity2 = None
        self.text_cannonball_info = None
        self.color = tanks[self.tank_game.actual_player].available
        if instance.type_of_effect in [
            AmbientEffect.GRAVITY_AND_WIND,
            AmbientEffect.GRAVITY,
        ]:
            self.actual_gravity = gravity
        if wind is not None:
            self.actual_wind = wind

    def draw_shoot_info(self, screen: pygame.surface.Surface) -> None:
        """
        This method is responsible for drawing on the HUD all the information about
        the bullet such as the maximum distance traveled or the maximum height reached.
        """
        transparency = 128
        rect_surface = pygame.Surface(
            (instance.windows_size[0] / 4.26, instance.windows_size[1] / 14.4)
        )
        rect_surface.set_alpha(transparency)
        if instance.windows_size[0] != instance.windows_size[1]:
            rect_x1, rect_y1 = (
                instance.windows_size[0] / 64,
                instance.windows_size[1] / 1.6,
            )
            rect_x2, rect_y2 = (
                instance.windows_size[0] // 1.33,
                instance.windows_size[1] // 1.6,
            )
        else:
            rect_x1, rect_y1 = (
                instance.windows_size[0] / 40,
                instance.windows_size[1] / 1.6,
            )
            rect_x2, rect_y2 = (
                instance.windows_size[0] / 1.349,
                instance.windows_size[1] // 1.6,
            )
        screen.blit(rect_surface, (rect_x1, rect_y1))
        screen.blit(rect_surface, (rect_x2, rect_y2))

        if self.tank_game.cannonball is not None:
            self.text_cannonball_info = self.font.render(
                f"Maxima Altura: {self.tank_game.cannonball.get_max_height()} [m]",
                True,
                "white",
            )
            screen.blit(
                self.text_cannonball_info,
                pygame.Vector2(
                    instance.windows_size[0] / 32, instance.windows_size[1] / 1.56
                ),
            )

            distance = self.tank_game.cannonball.calculate_distance_to(
                self.tanks[self.tank_game.actual_player].position
            )
            self.text_cannonball_info = self.font.render(
                f"Distancia total: {int(distance)}[m]",
                True,
                "white",
            )
            screen.blit(
                self.text_cannonball_info,
                pygame.Vector2(
                    instance.windows_size[0] / 1.29, instance.windows_size[1] / 1.56
                ),
            )

    @staticmethod
    def draw_cannonball_105_mm(screen: pygame.surface):
        """
        This method allows you to draw the 105mm cannonball icon
        """
        position = pygame.Vector2(
            instance.windows_size[0] / 4.41, instance.windows_size[1] / 4.23
        )
        pygame.draw.line(
            screen,
            "gray",
            position,
            (
                position.x + instance.windows_size[0] / 36.57,
                position.y - instance.windows_size[1] / 20.57,
            ),
            instance.windows_size[0] // 128,
        )
        pygame.draw.circle(screen, "black", position, instance.windows_size[0] / 51.2)

        pygame.draw.line(
            screen,
            "yellow",
            (
                position.x + instance.windows_size[0] / 36.57,
                position.y - instance.windows_size[1] / 20.57,
            ),
            (
                position.x + instance.windows_size[0] / 32,
                position.y - instance.windows_size[1] / 18,
            ),
            instance.windows_size[0] // 128,
        )

    @staticmethod
    def draw_cannonball_80_mm(screen: pygame.surface.Surface):
        """
        This method allows you to draw the 80mm cannonball icon.
        """
        position = pygame.Vector2(
            instance.windows_size[0] / 8, instance.windows_size[1] / 4.8
        )
        triangle = [
            (position.x, position.y),
            (
                position.x + instance.windows_size[0] / 102.4,
                position.y - instance.windows_size[1] / 40,
            ),
            (position.x + instance.windows_size[0] / 51.2, position.y),
        ]

        pygame.draw.rect(
            screen,
            constants.DarkGreen,
            pygame.Rect(
                position.x,
                position.y,
                instance.windows_size[0] / 51.2,
                instance.windows_size[1] / 19.2,
            ),
        )
        pygame.draw.line(
            screen,
            "yellow",
            (position.x, position.y + instance.windows_size[1] / 38.46),
            (
                position.x + instance.windows_size[0] / 51.2,
                position.y + instance.windows_size[1] / 38.46,
            ),
            13,
        )
        pygame.draw.polygon(screen, constants.DarkGreen, triangle)

        pygame.draw.line(
            screen,
            "orange",
            (
                position.x + instance.windows_size[0] / 102.4,
                position.y + instance.windows_size[1] / 19.2,
            ),
            (
                position.x + instance.windows_size[0] / 102.4,
                position.y + instance.windows_size[1] / 14.4,
            ),
            10,
        )

    @staticmethod
    def draw_cannonball_60_mm(screen: pygame.surface.Surface):
        """
        This method allows you to draw the 60mm cannonball icon.
        """
        position = pygame.Vector2(
            instance.windows_size[0] / 25.6, instance.windows_size[1] / 5.14
        )
        pygame.draw.line(
            screen,
            "#4b5320",
            (position.x, position.y),
            (position.x, position.y + instance.windows_size[1] / 14.4),
            int(instance.windows_size[0] // 51.2),
        )
        pygame.draw.line(
            screen,
            "#fbb741",
            (position.x, position.y + 37.5),
            (position.x, position.y + 50),
            25,
        )

    def tank_info(self) -> pygame.Surface:
        """
        This method is responsible for displaying all the tank and player information in a section of the HUD
        """
        actual_tank = self.tanks[self.tank_game.actual_player]
        width = instance.windows_size[0] / 3.65
        height = instance.windows_size[1] / 3.6
        sf = pygame.Surface((width, height))
        sf.fill("#232323")
        # this is for health
        heart_icon = image_cache["images/heart.png"]
        heart_icon = pygame.transform.scale(heart_icon, (width / 14, height / 8))
        sf.blit(heart_icon, (width / 7.5, height / 3.5))
        width_bar = width / 7.5 + width / 10
        height_bar = height / 3.7
        text = self.font30.render("Información", True, "white")
        sf.blit(text, (width / 2 - text.get_size()[0] / 2, 5))
        bar_length = width // 1.5
        bar_height = height / 6.66
        fill1 = (actual_tank.life / 100) * bar_length
        pygame.draw.rect(sf, "#248934", (width_bar, height_bar, bar_length, bar_height))
        pygame.draw.rect(
            sf,
            "#131313",
            (width_bar + fill1, height_bar, bar_length - fill1 + 1, bar_height),
        )
        player = self.font16.render(
            "Salud " + str(actual_tank.life) + " / 100", True, "white"
        )
        sf.blit(player, (width_bar + width_bar // 9, height_bar + height_bar // 9))

        # this is for money
        money_icon = image_cache["images/money.png"]
        money_icon = pygame.transform.scale(money_icon, (width / 11.66, height / 6.66))
        sf.blit(money_icon, (width / 7.5, height / 2.2))
        actual_money = self.font16.render(
            "Dinero disponible: $" + str(actual_tank.player.money),
            True,
            "#FFFFFF",
        )
        sf.blit(actual_money, (width / 4, height / 2))

        # this is por murders
        murders_icon = image_cache["images/murders.png"]
        murders_icon = pygame.transform.scale(murders_icon, (width / 14, height / 8))
        sf.blit(murders_icon, (width / 7.5, height / 1.55))
        actual_murders = self.font16.render(
            "Asesinatos cometidos: "
            + str(self.tanks[self.tank_game.actual_player].player.murders),
            True,
            "#FFFFFF",
        )
        sf.blit(actual_murders, (width / 4, height / 1.5))

        # this is por deads
        deads_icon = image_cache["images/deads.png"]
        deads_icon = pygame.transform.scale(deads_icon, (width / 14, height / 8))
        sf.blit(deads_icon, (width / 7.5, height / 1.25))
        actual_deads = self.font16.render(
            "Veces que ha muerto: "
            + str(self.tanks[self.tank_game.actual_player].player.deads),
            True,
            "#FFFFFF",
        )
        sf.blit(actual_deads, (width / 4, height / 1.2))

        return sf

    def get_actual_player(self):
        """
        This method allows you to draw the current player's tank on the
        HUD to indicate who is currently playing.
        """
        width = instance.windows_size[0] / 7.75
        height = instance.windows_size[1] / 3.6
        sf = pygame.Surface((width, height))
        sf.fill("#232323")
        actual_player1 = self.font30.render("Jugador", True, "#FFFFFF")
        actual_player = self.font30.render("actual", True, "#FFFFFF")
        sf.blit(actual_player1, (width / 6, height / 72))
        sf.blit(actual_player, (width / 4, height / 7))
        pygame.draw.rect(
            sf,
            self.tank_game.tanks[self.tank_game.actual_player].color,
            pygame.Rect(
                width / 3 + width / 9.16,
                height / 1.5 - height / 13.33,
                width / 6.6,
                height / 11.42,
            ),
        )
        pygame.draw.rect(
            sf,
            self.tank_game.tanks[self.tank_game.actual_player].color,
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
            self.tank_game.tanks[self.tank_game.actual_player].color,
            ((width / 3 + width / 5.68), height / 1.5 - height / 15.38),
            ((width / 3 - width / 16.5), height / 1.5 - height / 5.71),
            int(width / 20.625),
        )

        return sf

    def get_select_cannonball(self):
        """
        This method allows you to draw on the HUD the number of bullets that the current player has.
        """
        width = instance.windows_size[0] / 3.65
        height = instance.windows_size[1] / 3.6
        sf = pygame.Surface((width, height))
        sf.fill("#232323")
        alto = height // 2
        text = self.font30.render("Selección de bala", True, "white")
        sf.blit(text, (width / 2 - text.get_size()[0] / 2, width / 40))
        mm60 = self.font16.render("60MM", True, "white")
        sf.blit(mm60, (width / 3 - mm60.get_size()[0] / 0.5, width / 7))
        mm80 = self.font16.render("80MM", True, "white")
        sf.blit(mm80, (width / 2 - mm80.get_size()[0] / 1.5, width / 7))
        mm105 = self.font16.render("105MM", True, "white")
        sf.blit(mm105, (width / 1.2 - mm105.get_size()[0] / 2, width / 7))
        ancho = width / 7
        for i in range(3):
            pygame.draw.circle(sf, "#45484A", (ancho, alto), width / 11.66)
            ancho += width / 2.91
        self.color = self.tanks[self.tank_game.actual_player].available
        ancho = width / 7
        for i in range(3):
            pygame.draw.circle(sf, "#232323", (ancho, alto), width / 14)
            if self.tank_game.tanks[self.tank_game.actual_player].actual == i:
                if self.color[i] > 0:
                    pygame.draw.circle(sf, "#A7D131", (ancho, alto), width / 14)
                else:
                    pygame.draw.circle(sf, "#F80000", (ancho, alto), width / 14)
            ancho += width / 2.91
        ancho = width / 7
        if instance.windows_size[0] != instance.windows_size[1]:
            for i in range(3):
                pygame.draw.circle(sf, "#45484A", (ancho, alto), width / 17.5)
                cantidad = self.font.render(
                    f"{self.tanks[self.tank_game.actual_player].available[i]}",
                    True,
                    "white",
                )
                if self.tanks[self.tank_game.actual_player].available[i] > 9:
                    sf.blit(cantidad, (ancho - width / 23.33, alto - height / 13.33))
                else:
                    sf.blit(cantidad, (ancho - width / 43.75, alto - height / 13.33))
                ancho += width / 2.91
        else:
            for i in range(3):
                pygame.draw.circle(sf, "#45484A", (ancho, alto), width / 17.5)
                cantidad = self.font.render(
                    f"{self.tanks[self.tank_game.actual_player].available[i]}",
                    True,
                    "white",
                )
                if self.tanks[self.tank_game.actual_player].available[i] > 9:
                    sf.blit(cantidad, (ancho - width / 23.33, alto - height / 27.33))
                else:
                    sf.blit(cantidad, (ancho - width / 43.75, alto - height / 27.33))
                ancho += width / 2.91
        self.draw_cannonball_60_mm(sf)
        self.draw_cannonball_80_mm(sf)
        self.draw_cannonball_105_mm(sf)
        return sf

    def get_cannonball_indicators(self) -> pygame.Surface:
        """
        This method allows you to draw on the HUD both the angle and the speed at which you want to shoot.
        """
        width = instance.windows_size[0] / 3.65
        height = instance.windows_size[1] / 3.6

        sf = pygame.Surface((width, height))
        sf.fill("#232323")

        text = self.font30.render("Ajustes de bala", True, "white")
        velocity_label = self.font16.render("Velocidad", True, "white")
        angle_label = self.font16.render("Angulo", True, "white")
        gravity_label = self.font16.render("Gravedad", True, "white")
        wind_label = self.font16.render("Viento", True, "white")

        self.speedometer.actual = self.tank_game.tanks[
            self.tank_game.actual_player
        ].shoot_velocity
        self.font16.set_bold(True)
        velocity = self.font16.render(f"{self.speedometer.actual:.2f}", True, "white")

        sf.blit(text, (width / 2 - text.get_size()[0] / 2, width / 70))
        cds = pygame.rect.Rect(
            (2 / 2.7) * width - width / 35,
            (4 / 8) * height - height / 13.33,
            width / 5,
            height / 6.66,
        )
        pygame.draw.rect(sf, "#141414", cds)
        sf.blit(
            velocity, ((2 / 2.7) * width, (4 / 8) * height - velocity.get_size()[1] / 2)
        )
        sf.blit(
            velocity_label,
            (
                (2 / 2.7) * width - width / 35,
                (4 / 8) * height - height / 13.33 - velocity_label.get_size()[1],
            ),
        )
        if instance.type_of_effect in [
            AmbientEffect.GRAVITY_AND_WIND,
            AmbientEffect.GRAVITY,
        ]:
            gravity = self.font16.render(
                f"{self.actual_gravity:.2f}",
                True,
                "white",
            )
            cds = pygame.rect.Rect(
                (2 / 4) * width - width / 35,
                (4 / 8) * height - height / 13.33,
                width / 5,
                height / 6.66,
            )
            pygame.draw.rect(sf, "#141414", cds)
            sf.blit(
                gravity, ((2 / 4) * width, (4 / 8) * height - gravity.get_size()[1] / 2)
            )
            sf.blit(
                gravity_label,
                (
                    (2 / 4) * width - width / 35,
                    (4 / 8) * height - height / 13.33 - gravity_label.get_size()[1],
                ),
            )
        if instance.type_of_effect in [
            AmbientEffect.GRAVITY_AND_WIND,
            AmbientEffect.WIND,
        ]:
            wind = self.font16.render(
                f"{self.actual_wind.velocity:.2f}",
                True,
                "white",
            )

            cds = pygame.rect.Rect(
                (2 / 4) * width - width / 35,
                (6 / 8) * height - height / 13.33,
                width / 5,
                height / 6.66,
            )
            pygame.draw.rect(sf, "#141414", cds)
            sf.blit(wind, ((2 / 4) * width, (6 / 8) * height - wind.get_size()[1] / 2))
            sf.blit(
                wind_label,
                (
                    (2 / 4) * width - width / 35,
                    (6 / 8) * height - height / 13.33 - wind_label.get_size()[1],
                ),
            )

        angle = self.font16.render(
            f"{math.degrees(self.tank_game.tanks[self.tank_game.actual_player].shoot_angle):.2f}",
            True,
            "white",
        )

        cds = pygame.rect.Rect(
            (2 / 2.7) * width - width / 35,
            (6 / 8) * height - height / 13.33,
            width / 5,
            height / 6.66,
        )
        pygame.draw.rect(sf, "#141414", cds)
        sf.blit(angle, ((2 / 2.7) * width, (6 / 8) * height - angle.get_size()[1] / 2))
        sf.blit(
            angle_label,
            (
                (2 / 2.7) * width - width / 35,
                (6 / 8) * height - height / 23.33 - velocity_label.get_size()[1],
            ),
        )
        self.font16.set_bold(False)

        sf.blit(
            self.speedometer.get_draw(), (width / 15, (1 / 3) * height - height / 20)
        )

        return sf

    def draw_tank_health(self, sf: pygame.surface.Surface):
        """
        This method is responsible for drawing the health bars of the tanks on the game itself.
        The colors of the bars vary depending on the life level of the tank.
        """
        color_life = ""
        width = 30
        height = 10
        for tank in self.tank_game.tanks:
            if tank != self.tank_game.tanks[self.tank_game.actual_player]:
                bar_length = (tank.life / 100) * width
                pygame.draw.rect(
                    sf,
                    "gray",
                    (tank.position.x + 5, tank.position.y + 50, width, height),
                )

                if tank.life <= 100:
                    color_life = "green"
                if tank.life <= 85:
                    color_life = "yellow"
                if tank.life < 50:
                    color_life = "red"

                pygame.draw.rect(
                    sf,
                    color_life,
                    (tank.position.x + 5, tank.position.y + 50, bar_length, height),
                )

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function allows you to display on the screen everything related to the
        information about each tank such as angle and rate of fire,
        score, maximum height, maximum distance, also check if the tank
        killed itself to call the corresponding function. Furthermore, if the mode
        developer is activated shows the FPS
        """
        restart_pos = (
            instance.border_padding + instance.windows_size[0] / 128,
            instance.windows_size[1] - instance.windows_size[1] / 24,
        )
        radius = instance.windows_size[0] / 80
        ms = pygame.mouse.get_pos()
        if (
            (restart_pos[0] - ms[0]) ** 2 + (restart_pos[1] - ms[1]) ** 2
        ) < radius**2 and pygame.mouse.get_pressed()[0]:
            self.tank_game.restart()
        screen.blit(
            self.get_actual_player(),
            (
                instance.border_padding - instance.windows_size[0] / 128,
                instance.windows_size[1]
                - instance.windows_size[1] / 3.6
                - instance.border_padding / 2,
            ),
        )
        screen.blit(
            self.get_cannonball_indicators(),
            (
                instance.border_padding + instance.windows_size[0] / 7.5,
                instance.windows_size[1]
                - instance.windows_size[1] / 3.6
                - instance.border_padding / 2,
            ),
        )
        screen.blit(
            self.get_select_cannonball(),
            (
                instance.border_padding + instance.windows_size[0] / 2.39,
                instance.windows_size[1]
                - instance.hud_height
                - instance.border_padding / 2,
            ),
        )
        screen.blit(
            self.tank_info(),
            (
                instance.border_padding + instance.windows_size[0] / 1.42,
                instance.windows_size[1]
                - instance.hud_height
                - instance.border_padding / 2,
            ),
        )

        if self.tank_game.last_state is not None:
            self.draw_shoot_info(screen)

        if constants.DEVELOPMENT_MODE:
            screen.blit(
                self.font.render(
                    f"FPS: {int(instance.fps)}",
                    True,
                    "black",
                ),
                (0, 0),
            )
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_v]:
            self.draw_tank_health(screen)
