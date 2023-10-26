import math

import pygame

import constants
from caches import font_cache, image_cache
from draw import Drawable
from speedometer import Speedometer
from tank import Tank


class HUD(Drawable):
    """
    This class is responsible for displaying elements related to the
    information on screen that is not part of the terrain or the game itself.
    """

    tanks: list[Tank]
    left = 100
    top = constants.WINDOWS_SIZE[1] - int((3 / 5) * constants.HUD_HEIGHT)
    width = 160
    height = 50
    color: list[int]

    def __init__(self, tanks: list[Tank], tank_game):
        self.tank_game = tank_game
        self.tanks = tanks
        self.hud_image = image_cache["images/Angle.png"]
        self.speedometer = Speedometer(int((2 / 3) * constants.HUD_HEIGHT))
        self.font = font_cache["Roboto.ttf", 24]
        self.font30 = font_cache["Roboto.ttf", 30]
        self.font16 = font_cache["Roboto.ttf", 16]
        self.font12 = font_cache["Roboto.ttf", 12]
        self.text_angle1 = None
        self.text_angle2 = None
        self.text_velocity1 = None
        self.text_velocity2 = None
        self.text_cannonball_info = None
        self.color = tanks[self.tank_game.actual_player].available

    def draw_shoot_info(self, screen: pygame.surface.Surface) -> None:
        """
        This method is responsible for drawing on the HUD all the information about
        the bullet such as the maximum distance traveled or the maximum height reached.
        """
        transparency = 128
        rect_surface = pygame.Surface((300, 50))
        rect_surface.set_alpha(transparency)
        rect_x1, rect_y1 = constants.H_MAX
        rect_x2, rect_y2 = constants.DISTANCE_MAX
        screen.blit(rect_surface, (rect_x1, rect_y1))
        screen.blit(rect_surface, (rect_x2, rect_y2))

        if self.tank_game.cannonball is not None:
            self.text_cannonball_info = self.font.render(
                f"Maxima Altura: {self.tank_game.cannonball.get_max_height()} [m]",
                True,
                "white",
            )
            screen.blit(self.text_cannonball_info, pygame.Vector2(40, 460))

            distance = self.tank_game.cannonball.calculate_distance_to(
                self.tanks[self.tank_game.actual_player].position
            )
            self.text_cannonball_info = self.font.render(
                f"Distancia total: {int(distance)}[m]",
                True,
                "white",
            )
            screen.blit(self.text_cannonball_info, pygame.Vector2(990, 460))

    @staticmethod
    def draw_cannonball_105_mm(screen: pygame.surface):
        """This method allows you to draw the 105mm cannonball icon."""
        position = pygame.Vector2(290, 170)
        pygame.draw.line(
            screen, "gray", position, (position.x + 35, position.y - 35), 10
        )
        pygame.draw.circle(screen, "black", position, 25)

        pygame.draw.line(
            screen,
            "yellow",
            (position.x + 35, position.y - 35),
            (position.x + 40, position.y - 40),
            10,
        )

    @staticmethod
    def draw_cannonball_80_mm(screen: pygame.surface):
        """This method allows you to draw the 80mm cannonball icon."""
        position = pygame.Vector2(160, 150)
        triangle = [
            (position.x, position.y),
            (position.x + 12.5, position.y - 18),
            (position.x + 25, position.y),
        ]

        pygame.draw.rect(
            screen, constants.DarkGreen, pygame.Rect(position.x, position.y, 25, 37.5)
        )
        pygame.draw.line(
            screen,
            "yellow",
            (position.x, position.y + 18.75),
            (position.x + 25, position.y + 18.75),
            13,
        )
        pygame.draw.polygon(screen, constants.DarkGreen, triangle)

        pygame.draw.line(
            screen,
            "orange",
            (position.x + 12.5, position.y + 37.5),
            (position.x + 12.5, position.y + 50),
            10,
        )

    @staticmethod
    def draw_cannonball_60_mm(screen: pygame.surface):
        """This method allows you to draw the 60mm cannonball icon."""
        position = pygame.Vector2(50, 140)
        pygame.draw.line(
            screen,
            "#4b5320",
            (position.x, position.y),
            (position.x, position.y + 50),
            25,
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
        width = 350
        height = constants.HUD_HEIGHT
        sf = pygame.Surface((width, constants.HUD_HEIGHT))
        sf.fill("#232323")
        # this is for health
        heart_icon = image_cache["images/heart.png"]
        heart_icon = pygame.transform.scale(heart_icon, (25, 25))
        sf.blit(heart_icon, (width / 7.5, height / 3.5))
        width_bar = height // 2.7
        height_bar = width / 6
        text = self.font30.render("Información", True, "white")
        sf.blit(text, (width / 2 - text.get_size()[0] / 2, 5))
        bar_length = width // 1.5
        bar_height = 30
        fill1 = (self.tanks[self.tank_game.actual_player].life / 100) * bar_length
        pygame.draw.rect(sf, "#248934", (width_bar, height_bar, bar_length, bar_height))
        pygame.draw.rect(
            sf,
            "#131313",
            (width_bar + fill1, height_bar, bar_length - fill1 + 1, bar_height),
        )
        player = self.font16.render("Salud", True, "white")
        sf.blit(player, (width_bar + width_bar // 9, height_bar + height_bar // 9))

        # this is for money
        money_icon = image_cache["images/money.png"]
        money_icon = pygame.transform.scale(money_icon, (30, 30))
        sf.blit(money_icon, (width / 7.5, height / 2.2))
        actual_money = self.font16.render(
            "Dinero disponible: $"
            + str(self.tanks[self.tank_game.actual_player].player.money),
            True,
            "#FFFFFF",
        )
        sf.blit(actual_money, (width / 4, height / 2))

        # this is por murders
        murders_icon = image_cache["images/murders.png"]
        murders_icon = pygame.transform.scale(murders_icon, (25, 25))
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
        deads_icon = pygame.transform.scale(deads_icon, (25, 25))
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
        width = 165
        height = constants.HUD_HEIGHT
        sf = pygame.Surface((width, height))
        sf.fill("#232323")
        actual_player1 = self.font30.render("Jugador", True, "#FFFFFF")
        actual_player = self.font30.render("actual", True, "#FFFFFF")
        sf.blit(actual_player1, (width / 6, 10))
        sf.blit(actual_player, (width / 5, 40))
        pygame.draw.rect(
            sf,
            self.tank_game.tanks[self.tank_game.actual_player].color,
            pygame.Rect(width / 3 + 18, height / 1.5 - 15, 25, 17.5),
        )
        pygame.draw.rect(
            sf,
            self.tank_game.tanks[self.tank_game.actual_player].color,
            pygame.Rect(
                width / 3,
                height / 1.5,
                62.5,
                25,
            ),
        )
        pygame.draw.rect(
            sf,
            constants.GRAY,
            pygame.Rect(
                width / 3,
                height / 1.5 + 25,
                62.5,
                10,
            ),
        )

        for i in range(6):
            pygame.draw.circle(
                sf,
                constants.BLACK,
                (
                    width / 3 + 12.5 * i,
                    height / 1.5 + 35,
                ),
                7.5,
            )

        pygame.draw.line(
            sf,
            self.tank_game.tanks[self.tank_game.actual_player].color,
            ((width / 3 + 29), height / 1.5 - 13),
            ((width / 3 - 10), height / 1.5 - 35),
            8,
        )

        return sf

    def get_select_cannonball(self):
        """
        This method allows you to draw on the HUD the number of bullets that the current player has.
        """
        width = 350
        height = constants.HUD_HEIGHT
        sf = pygame.Surface((width, height))
        sf.fill("#232323")
        alto = height // 2
        text = self.font30.render("Selección de bala", True, "white")
        sf.blit(text, (width / 2 - text.get_size()[0] / 2, 5))
        mm60 = self.font16.render("60MM", True, "white")
        sf.blit(mm60, (width / 3 - mm60.get_size()[0] / 0.5, 50))
        mm80 = self.font16.render("80MM", True, "white")
        sf.blit(mm80, (width / 2 - mm80.get_size()[0] / 1.5, 50))
        mm105 = self.font16.render("105MM", True, "white")
        sf.blit(mm105, (width / 1.2 - mm105.get_size()[0] / 2, 50))
        ancho = 50
        for i in range(3):
            pygame.draw.circle(sf, "#45484A", (ancho, alto), 30)
            ancho += 120
        self.color = self.tanks[self.tank_game.actual_player].available
        ancho = 50
        for i in range(3):
            if self.color[i] > 0:
                pygame.draw.circle(sf, "#A7D131", (ancho, alto), 25)
                if self.tank_game.tanks[self.tank_game.actual_player].actual == i:
                    pygame.draw.circle(sf, "#1A54D4", (ancho, alto), 25)
            else:
                pygame.draw.circle(sf, "#F80000", (ancho, alto), 25)
            ancho += 120
        ancho = 50
        for i in range(3):
            pygame.draw.circle(sf, "#45484A", (ancho, alto), 20)
            cantidad = self.font.render(
                f"{self.tanks[self.tank_game.actual_player].available[i]}",
                True,
                "white",
            )
            if self.tanks[self.tank_game.actual_player].available[i] > 9:
                sf.blit(cantidad, (ancho - 15, alto - 15))
            else:
                sf.blit(cantidad, (ancho - 8, alto - 15))
            ancho += 120
        self.draw_cannonball_60_mm(sf)
        self.draw_cannonball_80_mm(sf)
        self.draw_cannonball_105_mm(sf)
        return sf

    def get_cannonball_indicators(self) -> pygame.Surface:
        """
        This method allows you to draw on the HUD both the angle and the speed at which you want to shoot.
        """
        width = 350
        height = constants.HUD_HEIGHT

        sf = pygame.Surface((width, height))
        sf.fill("#232323")

        text = self.font30.render("Ajustes de bala", True, "white")
        velocity_label = self.font16.render("Velocidad", True, "white")
        angle_label = self.font16.render("Angulo", True, "white")

        self.speedometer.actual = self.tank_game.tanks[
            self.tank_game.actual_player
        ].shoot_velocity
        self.font16.set_bold(True)
        velocity = self.font16.render(f"{self.speedometer.actual:.2f}", True, "white")

        sf.blit(text, (width / 2 - text.get_size()[0] / 2, 5))
        cds = pygame.rect.Rect((2 / 3) * width - 10, (4 / 8) * height - 15, 70, 30)
        pygame.draw.rect(sf, "#141414", cds)
        sf.blit(
            velocity, ((2 / 3) * width, (4 / 8) * height - velocity.get_size()[1] / 2)
        )
        sf.blit(
            velocity_label,
            (
                (2 / 3) * width - 10,
                (4 / 8) * height - 15 - velocity_label.get_size()[1],
            ),
        )

        angle = self.font16.render(
            f"{math.degrees(self.tank_game.tanks[self.tank_game.actual_player].shoot_angle):.2f}",
            True,
            "white",
        )
        cds = pygame.rect.Rect((2 / 3) * width - 10, (6 / 8) * height - 15, 70, 30)
        pygame.draw.rect(sf, "#141414", cds)
        sf.blit(angle, ((2 / 3) * width, (6 / 8) * height - angle.get_size()[1] / 2))
        sf.blit(
            angle_label,
            (
                (2 / 3) * width - 10,
                (6 / 8) * height - 15 - velocity_label.get_size()[1],
            ),
        )
        self.font16.set_bold(False)

        sf.blit(self.speedometer.get_draw(), (20, (1 / 3) * height - 10))

        return sf

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function allows you to display on the screen everything related to the
        information about each tank such as angle and rate of fire,
        score, maximum height, maximum distance, also check if the tank
        killed itself to call the corresponding function. Furthermore, if the mode
        developer is activated shows the FPS
        """
        restart_pos = (constants.BORDER_PADDING + 10, constants.WINDOWS_SIZE[1] - 30)
        radius = 16
        ms = pygame.mouse.get_pos()
        if (
            (restart_pos[0] - ms[0]) ** 2 + (restart_pos[1] - ms[1]) ** 2
        ) < radius**2 and pygame.mouse.get_pressed()[0]:
            self.tank_game.restart()
        screen.blit(
            self.get_actual_player(),
            (
                constants.BORDER_PADDING - 10,
                constants.WINDOWS_SIZE[1]
                - constants.HUD_HEIGHT
                - constants.BORDER_PADDING / 2,
            ),
        )
        screen.blit(
            self.get_cannonball_indicators(),
            (
                constants.BORDER_PADDING + 170,
                constants.WINDOWS_SIZE[1]
                - constants.HUD_HEIGHT
                - constants.BORDER_PADDING / 2,
            ),
        )
        screen.blit(
            self.get_select_cannonball(),
            (
                constants.BORDER_PADDING + 535,
                constants.WINDOWS_SIZE[1]
                - constants.HUD_HEIGHT
                - constants.BORDER_PADDING / 2,
            ),
        )
        screen.blit(
            self.tank_info(),
            (
                constants.BORDER_PADDING + 900,
                constants.WINDOWS_SIZE[1]
                - constants.HUD_HEIGHT
                - constants.BORDER_PADDING / 2,
            ),
        )

        if self.tank_game.last_state is not None:
            self.draw_shoot_info(screen)

        if constants.DEVELOPMENT_MODE:
            screen.blit(
                self.font.render(
                    f"FPS: {int(self.tank_game.fps)}",
                    True,
                    "black",
                ),
                (0, 0),
            )

    def show_instructions(self, screen: pygame.surface.Surface):
        """
        This function allows you to display an image at the start of the game with the
        necessary instructions for the players
        """
        screen.fill("#3C0384")

        instructions = image_cache["images/instructions.png"]
        rect = instructions.get_rect()
        size = rect.size

        screen.blit(
            instructions,
            (
                constants.WINDOWS_SIZE[0] / 2 - size[0] / 2,
                constants.WINDOWS_SIZE[1] / 2 - size[1] / 2,
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
            (constants.WINDOWS_SIZE[0] - size[0], constants.WINDOWS_SIZE[1] - size[1]),
        )
