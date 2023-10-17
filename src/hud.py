import math

import pygame

import constants
from caches import font_cache, image_cache
from draw import Drawable
from speedometer import Speedometer
from tank import Tank


class HUD(Drawable):
    """
    Esta clase es responsable de mostrar elementos relacionados con la
    información en pantalla que no es parte del terreno o del juego en sí :)
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

    def health_bars(self) -> pygame.Surface:
        other_player = (self.tank_game.actual_player + 1) % 2
        width = 350
        height = constants.HUD_HEIGHT
        alto1 = height // 3
        ancho1 = width / 6
        alto2 = height // 1.5
        ancho2 = width / 6

        sf = pygame.Surface((width, constants.HUD_HEIGHT))
        sf.fill("#232323")
        text = self.font30.render("Salud de tanques", True, "white")
        sf.blit(text, (width / 2 - text.get_size()[0] / 2, 5))
        bar_length = width // 1.5
        bar_height = 30
        fill1 = (self.tanks[self.tank_game.actual_player].life / 100) * bar_length
        pygame.draw.rect(sf, "#248934", (ancho1, alto1, bar_length, bar_height))
        pygame.draw.rect(
            sf, "#131313", (ancho1 + fill1, alto1, bar_length - fill1 + 1, bar_height)
        )
        fill2 = (self.tanks[other_player].life / 100) * bar_length
        pygame.draw.rect(sf, "#AD2301", (ancho2, alto2, bar_length, bar_height))
        pygame.draw.rect(
            sf, "#131313", (ancho2 + fill2, alto2, bar_length - fill2 + 1, bar_height)
        )
        jugador = self.font16.render("Jugador", True, "white")
        sf.blit(jugador, (ancho1 + ancho1 // 9, alto1 + alto1 // 9))
        oponente = self.font16.render("Oponente", True, "white")
        sf.blit(oponente, (ancho2 + ancho2 // 9, alto2 + alto2 // 18))
        return sf

    def get_select_cannonball(self):
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
        Esta función  permite mostrar en pantalla todo lo relacionado a la
        información de cada tanque tales como angulo y velocidad de disparo,
        puntaje, máxima altura, máxima distancia, también verifica si el tanque
        se suicidó para llamar a la función correspondiente. Además, si el modo
        desarrollador está activado muestra los FPS.
        """
        restart_pos = (constants.BORDER_PADDING + 10, constants.WINDOWS_SIZE[1] - 30)
        radius = 16
        ms = pygame.mouse.get_pos()
        if (
            (restart_pos[0] - ms[0]) ** 2 + (restart_pos[1] - ms[1]) ** 2
        ) < radius**2 and pygame.mouse.get_pressed()[0]:
            self.tank_game.restart()

        screen.blit(
            self.get_cannonball_indicators(),
            (
                constants.BORDER_PADDING + 50,
                constants.WINDOWS_SIZE[1]
                - constants.HUD_HEIGHT
                - constants.BORDER_PADDING / 2,
            ),
        )
        screen.blit(
            self.get_select_cannonball(),
            (
                constants.BORDER_PADDING + 450,
                constants.WINDOWS_SIZE[1]
                - constants.HUD_HEIGHT
                - constants.BORDER_PADDING / 2,
            ),
        )
        screen.blit(
            self.health_bars(),
            (
                constants.BORDER_PADDING + 850,
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
        Esta función permite mostrar al inicio del juego una imagen con las
        instrucciones necesarias para el/los jugadores
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
