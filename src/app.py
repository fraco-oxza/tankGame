from __future__ import annotations

import math
import os
import random
from abc import abstractmethod
from random import randint
from typing import Optional
import sys

import pygame

import constants


def resource_path(relative_path: str):
    path = getattr(
        sys, "_MEIPASS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
    )
    return os.path.join(path, "resources", relative_path)


class Collidable:
    @abstractmethod
    def collides_with(self, point: pygame.Vector2) -> bool:
        raise NotImplementedError


class Drawable:
    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        raise NotImplementedError


class Background(Drawable):
    sky_image: pygame.Surface

    def __init__(self):
        image_size = pygame.Vector2(
            constants.WINDOWS_SIZE[0], (9 / 16) * constants.WINDOWS_SIZE[0]
        )
        self.sky_image = pygame.transform.scale(
            pygame.image.load(resource_path("images/sky.jpg")), image_size
        )
        self.sky_rect = self.sky_image.get_rect()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.sky_image, self.sky_rect.topleft)


class Terrain(Drawable, Collidable):
    ground_lines: list[int]

    def mountainRandom(self, lista: list[int], indiceInicial: int, indiceFinal: int):
        actualIncrease = 0
        for i in range(indiceInicial, indiceFinal):
            middle = (indiceFinal + indiceInicial) // 2
            if i < middle:
                actualIncrease += randint(2, 8)
            else:
                actualIncrease -= randint(2, 8)
                print(i)
            lista[i] += actualIncrease

        return lista

    def completeListRandom(self):
        lista = [constants.SEA_LEVEL] * (
            constants.WINDOWS_SIZE[0] // constants.TERRAIN_LINE_WIDTH
        )

        # 1000
        # 0 333 - 334 666 - 667 1000
        divide = (
            constants.WINDOWS_SIZE[0] // constants.MOUNTAINS
        ) // constants.TERRAIN_LINE_WIDTH

        for i in range(0, constants.MOUNTAINS):
            aumentar = i * divide

            indiceX1 = random.randint(aumentar, divide * (i + 1) - 1)
            indiceX2 = random.randint(aumentar, divide * (i + 1) - 1)

            if indiceX2 < indiceX1:
                # indiceX2, indiceX1 = (indiceX1, indiceX2)
                aux = indiceX1
                indiceX1 = indiceX2
                indiceX2 = aux

            self.mountain(lista, indiceX1, indiceX2)

        return lista

    def sin_mountain(self, i: int, j: int):
        m = (i + j) // 2

        for k in range(i, m):
            self.ground_lines[k] += ((k - i) ** 2) // 300

        for k in range(m, j):
            self.ground_lines[k] += ((j - k) ** 2) // 300

    def valley(self, inicio: int, fin: int):
        m = (inicio + fin) // 2
        for i in range(inicio, m):
            self.ground_lines[i] -= ((i - inicio) ** 2) // 700
        for j in range(m, fin):
            self.ground_lines[j] -= ((j - fin) ** 2) // 700

    def __init__(self, mountains: int, valleys: int):
        self.ground_lines = [constants.SEA_LEVEL + constants.HUD_HEIGHT] * (
            constants.WINDOWS_SIZE[0] // constants.TERRAIN_LINE_WIDTH
        )
        self.sin_mountain(160 * 2, 400 * 2)
        self.sin_mountain(450 * 2, 640 * 2)
        self.valley(0, 250 * 2)
        self.valley(250 * 2, 500 * 2)

    def draw(self, screen: pygame.surface.Surface) -> None:
        for i in range(len(self.ground_lines)):
            pygame.draw.rect(
                screen,
                constants.TERRAIN_COLOR,
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i],
                    constants.TERRAIN_LINE_WIDTH,
                    20,
                ),
            )
            pygame.draw.rect(
                screen,
                "#c8dfe2",
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i] + 20,
                    constants.TERRAIN_LINE_WIDTH,
                    self.ground_lines[i] - 20,
                ),
            )
            pygame.draw.rect(
                screen,
                "#2e4957",
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i] + 60,
                    constants.TERRAIN_LINE_WIDTH,
                    self.ground_lines[i] - 60,
                ),
            )
            pygame.draw.rect(
                screen,
                "#415c6b",
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i] + 120,
                    constants.TERRAIN_LINE_WIDTH,
                    self.ground_lines[i] - 120,
                ),
            )
            pygame.draw.rect(
                screen,
                "#50707f",
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i] + 200,
                    constants.TERRAIN_LINE_WIDTH,
                    self.ground_lines[i] - 200,
                ),
            )
    def collides_with(self, point: pygame.Vector2) -> bool:
        if point.x < 0.0:
            return True

        line_index = int(point.x) // constants.TERRAIN_LINE_WIDTH

        if line_index >= len(self.ground_lines):
            return True

        return point.y > (constants.WINDOWS_SIZE[1] - self.ground_lines[line_index])


class Cannonball(Drawable):
    position: pygame.Vector2
    velocity: pygame.Vector2
    trajectory: list[pygame.Vector2]
    max_height: int
    max_distance: int

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        self.position = position
        self.velocity = velocity
        self.max_height = sys.maxsize
        self.max_distance = sys.maxsize
        self.trajectory = []

    def tick(self, dt: float):
        if self.position.y < self.max_height:
            self.max_height = int(self.position.y)
        self.position += self.velocity * dt
        self.velocity[1] += constants.GRAVITY * dt
        self.trajectory.append(pygame.Vector2(self.position.x, self.position.y))

    def draw(self, screen: pygame.surface.Surface) -> None:
        for point in self.trajectory:
            pygame.draw.circle(screen, "#cccccc", point, 1)
        pygame.draw.circle(screen, "#ff0000", self.position, 2)

    def get_max_height(self) -> int:
        return constants.WINDOWS_SIZE[1] - self.max_height - constants.HUD_HEIGHT

    def get_max_distance(self, tank_position: pygame.Vector2, canonball_position: pygame.Vector2) -> int:
        return ((canonball_position.x - tank_position.x) ** 2 + (canonball_position.y - tank_position.y) ** 2) ** (
                    1 / 2)


    def max_velocity(self) -> float:
        angle_rad = math.atan2(self.velocity.y, self.velocity.x)
        v_max = self.velocity.magnitude() * math.cos(angle_rad)
        return v_max


class Player:
    name: str
    points: int

    def __init__(self, name: str, points: int):
        self.name = name
        self.points = points

    def score(self, impact: Impact, tank_position: pygame.Vector2):
        cannonball_position = impact.position
        distance = (
            (cannonball_position.x - tank_position.x) ** 2
            + (cannonball_position.y - tank_position.y) ** 2
        ) ** (1 / 2)
        if isinstance(impact, TerrainImpact):
            if distance <= constants.TANK_RADIO * 2:
                self.points = self.points + 100
            elif distance <= constants.TANK_RADIO + 200:
                self.points = self.points + 50
            else:
                self.points = self.points - (self.points // 3)

        elif isinstance(impact, TankImpact):
            self.points += 1000


class Tank(Drawable, Collidable):
    player: Player
    color: pygame.Color
    position: pygame.Vector2
    shoot_velocity: float  # m/s
    shoot_angle: float  # rad //

    def __init__(self, color: pygame.Color, position: pygame.Vector2, player: Player):
        self.player = player
        self.color = color
        self.position = position
        self.shoot_angle = 3.0 * math.pi / 4.0  # rad
        self.shoot_velocity = 145  # m/s

    def draw(self, screen: pygame.surface.Surface) -> None:
        # hit box
        # pygame.draw.circle(screen, "yellow", self.position, constants.TANK_RADIO)

        new_x = self.position.x + 20 * math.cos(self.shoot_angle)
        new_y = self.position.y - 20 * math.sin(self.shoot_angle)

        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.position.x - 5, self.position.y - 2, 10, 7),
        )
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.position.x - 12.5, self.position.y + 5, 25, 10),
        )
        pygame.draw.rect(
            screen,
            constants.GRAY,
            pygame.Rect(self.position.x - 12.5, self.position.y + 15, 25, 4),
        )

        # decoration IN PROCESS, IS UGLY NOW

        for i in range(6):
            pygame.draw.circle(
                screen,
                constants.BLACK,
                (self.position.x - 12 + 5 * i, self.position.y + 18),
                3,
            )

        # cannon

        pygame.draw.line(screen, self.color, self.position, (new_x, new_y), 3)
        pygame.draw.circle(screen, self.color, (new_x, new_y), 2)

    def collides_with(self, point: pygame.Vector2) -> bool:
        if ((point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2) ** (
            1 / 2
        ) <= constants.TANK_RADIO:
            return True
        return False

    def shoot(self) -> Cannonball:
        v_x = self.shoot_velocity * math.cos(self.shoot_angle)
        # the -1 is since in this system the vertical coordinates are inverted
        v_y = -1 * self.shoot_velocity * math.sin(self.shoot_angle)

        new_x = self.position.x + 20 * math.cos(self.shoot_angle)
        new_y = self.position.y - 20 * math.sin(self.shoot_angle)

        return Cannonball(pygame.Vector2(new_x, new_y), pygame.Vector2(v_x, v_y))


class HUD(Drawable):
    tanks: list[Tank]
    left = 100
    top = constants.WINDOWS_SIZE[1] - int((3 / 5) * constants.HUD_HEIGHT)
    width = 160
    height = 50

    def __init__(self, tanks: list[Tank], tank_game: TankGame):
        self.tank_game = tank_game
        self.tanks = tanks
        self.font = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 24)
        self.font16 = pygame.font.Font(resource_path("fonts/Roboto.ttf"), 16)
        self.text_angle1 = None
        self.text_angle2 = None
        self.text_velocity1 = None
        self.text_velocity2 = None
        self.text_cannonball_info = None

    def draw(self, screen: pygame.surface.Surface) -> None:
        self.tanks[0].shoot_angle %= 2.0 * math.pi
        self.tanks[1].shoot_angle %= 2.0 * math.pi

        pygame.draw.rect(
            screen,
            constants.HUD_COLOR,
            pygame.Rect(
                0,
                constants.WINDOWS_SIZE[1] - constants.HUD_HEIGHT,
                constants.WINDOWS_SIZE[0],
                constants.HUD_HEIGHT,
            ),
        )

        if (
            self.tank_game.cannonball is not None
            and self.tank_game.cannonball.position.y < 0
        ):
            draw_pos = (
                self.tank_game.cannonball.position.x,
                constants.WINDOWS_SIZE[1] - constants.HUD_HEIGHT,
            )
            pygame.draw.circle(screen, "#cc0000", draw_pos, 6)
            cannonball_height = self.font16.render(
                "^%d[m]"
                % int(
                    constants.WINDOWS_SIZE[1]
                    - self.tank_game.cannonball.position.y
                    - constants.HUD_HEIGHT
                ),
                True,
                "white",
            )
            screen.blit(
                cannonball_height,
                (
                    draw_pos[0] - cannonball_height.get_rect().size[0] // 2,
                    draw_pos[1] + cannonball_height.get_rect().size[1] // 2,
                ),
            )

        if self.tank_game.last_state is not None:
            transparency = 128
            rect_surface = pygame.Surface((300, 70))
            rect_surface.set_alpha(transparency)
            rect_x1, rect_y1 = constants.H_MAX
            rect_x2, rect_y2 = constants.DISTANCE_MAX
            screen.blit(rect_surface, (rect_x1, rect_y1))
            screen.blit(rect_surface, (rect_x2, rect_y2))

            if self.tank_game.cannonball is not None:
                self.text_cannonball_info = self.font.render(
                    "Maxima Altura: %d" % (self.tank_game.cannonball.get_max_height()) + " [m]",
                    True,
                    "white",

                )
                screen.blit(self.text_cannonball_info, pygame.Vector2(40, 675))
            if self.tank_game.cannonball is not None:
                distance = self.tank_game.cannonball.get_max_distance(self.tanks[self.tank_game.actual_player].position,
                                                                      self.tank_game.cannonball.position)
                self.text_cannonball_info = self.font.render("Distancia total: %d" % (distance) + " [m]", True,
                                                             "white", )
                screen.blit(self.text_cannonball_info, pygame.Vector2(1020, 675))
        self.text_angle1 = self.font.render(
            "Ángulo: %.1f" % math.degrees(self.tanks[0].shoot_angle) + "°",
            True,
            "white",
        )
        self.text_angle2 = self.font.render(
            "Ángulo: %.1f" % math.degrees(self.tanks[1].shoot_angle) + "°",
            True,
            "white",
        )

        self.text_velocity1 = self.font.render(
            "Velocidad: " + str(int(self.tanks[0].shoot_velocity)) + " m/s",
            True,
            "white",
        )
        self.text_velocity2 = self.font.render(
            "Velocidad: " + str(int(self.tanks[1].shoot_velocity)) + " m/s",
            True,
            "white",
        )
        pygame.draw.rect(
            screen, "Black", pygame.Rect(self.left, self.top, self.width, self.height)
        )
        pygame.draw.rect(
            screen, "Grey", pygame.Rect(self.left, self.top, self.width, self.height), 2
        )
        pygame.draw.rect(
            screen,
            "Black",
            pygame.Rect(self.left + 900, self.top, self.width, self.height),
        )
        pygame.draw.rect(
            screen,
            "Grey",
            pygame.Rect(self.left + 900, self.top, self.width, self.height),
            2,
        )
        pygame.draw.rect(
            screen,
            "Black",
            pygame.Rect(self.left + 200, self.top, self.width + 60, self.height),
        )
        pygame.draw.rect(
            screen,
            "Grey",
            pygame.Rect(self.left + 200, self.top, self.width + 60, self.height),
            2,
        )
        pygame.draw.rect(
            screen,
            "Black",
            pygame.Rect(self.left + 640, self.top, self.width + 60, self.height),
        )
        pygame.draw.rect(
            screen,
            "Grey",
            pygame.Rect(self.left + 640, self.top, self.width + 60, self.height),
            2,
        )

        screen.blit(self.text_angle1, (self.left + 5, self.top + 5))
        screen.blit(self.text_angle2, (self.left + 905, self.top + 5))
        screen.blit(self.text_velocity1, (self.left + 205, self.top + 5))
        screen.blit(self.text_velocity2, (self.left + 645, self.top + 5))

        if self.tank_game.winner is not None:
            # Maca Sofia trabajo, pantalla de ganador
            pass

    def show_instructions(self, screen: pygame.surface.Surface):
        screen.fill("#151f28")

        instructions = pygame.image.load(resource_path("images/instructions.png"))
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

        pygame.display.flip()


class Impact:
    position: pygame.Vector2

    def __init__(self, position: pygame.Vector2) -> None:
        self.position = position


class TerrainImpact(Impact):
    pass


class TankImpact(Impact):
    pass


class TankGame:
    """
    This class represents the complete game, it is responsible for maintaining the tanks, bullets, controlling user
    input, drawing, among others. It can be said that it is the central class of the project.
    """

    terrain: Terrain
    tanks: list[Tank]
    screen: pygame.Surface
    cannonball: Optional[Cannonball]
    running: bool
    actual_player: int
    winner: Optional[int]

    def __init__(self) -> None:
        """
        constructor that initializes each element within the game, in addition to starting the window itself of the game
        """
        pygame.init()

        pygame.display.set_caption("TankGame!")
        icon = pygame.image.load(resource_path("images/tankIcon.png"))
        pygame.display.set_icon(icon)

        self.background = Background()
        self.terrain = Terrain(constants.MOUNTAINS, constants.VALLEYS)

        self.winner = None
        self.running = True
        self.screen = pygame.display.set_mode(constants.WINDOWS_SIZE)
        self.clock = pygame.time.Clock()
        self.last_state = None

        self.cannonball = None
        self.tanks = []
        self.actual_player = randint(0, 1)

        quart_of_windows = int(constants.WINDOWS_SIZE[0] / 4)

        mid_point = randint(int(quart_of_windows), int(3 * quart_of_windows))

        tank1_x = randint(0, mid_point - quart_of_windows)
        tank2_x = randint(mid_point + quart_of_windows, constants.WINDOWS_SIZE[0])

        player1 = Player("1", 0)
        player2 = Player("2", 0)

        self.tanks.append(
            Tank(
                pygame.Color(50, 50, 0),
                pygame.Vector2(
                    tank1_x,
                    constants.WINDOWS_SIZE[1]
                    - self.terrain.ground_lines[
                        tank1_x // constants.TERRAIN_LINE_WIDTH - 1
                    ]
                    - 15,
                ),
                player1,
            )
        )

        self.tanks.append(
            Tank(
                pygame.Color(80, 50, 50),
                pygame.Vector2(
                    tank2_x,
                    constants.WINDOWS_SIZE[1]
                    - self.terrain.ground_lines[
                        tank2_x // constants.TERRAIN_LINE_WIDTH - 1
                    ]
                    - 15,
                ),
                player2,
            )
        )

        self.hud = HUD(self.tanks, self)

    def render(self) -> None:
        """
        This method is responsible for drawing each element of the window, it also puts the execution to sleep for a
        while to make the game run at the fps, specified in the FPS constant
        :return:
        """
        self.background.draw(self.screen)
        self.terrain.draw(self.screen)

        for tank in self.tanks:
            tank.draw(self.screen)

        if self.cannonball is not None:
            self.cannonball.draw(self.screen)

        self.hud.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(constants.FPS)

    def check_running(self):
        """
        This method checks if the player has sent the signal to close the window and stops the execution if this is the
        case, it is also responsible for cleaning any position that has been left unused.
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def process_input(self) -> None:
        """
        This method is responsible for reading from the keyboard what the user wants to do, modifying the attributes of
        the tanks or creating the cannonball.
        :return:
        """
        playing_tank = self.tanks[self.actual_player]

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_DOWN]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle += math.radians(0.5)
            else:
                playing_tank.shoot_angle += math.radians(0.1)

        if keys_pressed[pygame.K_UP]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle -= math.radians(0.5)
            else:
                playing_tank.shoot_angle -= math.radians(0.1)

        if keys_pressed[pygame.K_RIGHT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity += 0.5
            else:
                playing_tank.shoot_velocity += 0.1

            if playing_tank.shoot_velocity > 200:
                playing_tank.shoot_velocity = 200

        if keys_pressed[pygame.K_LEFT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity -= 0.5
            else:
                playing_tank.shoot_velocity -= 0.1

            if playing_tank.shoot_velocity < 1:
                playing_tank.shoot_velocity = 1

        if keys_pressed[pygame.K_SPACE]:
            self.cannonball = playing_tank.shoot()

    def process_cannonball_trajectory(self) -> Optional[Impact]:
        """
        This method is responsible for moving the cannonball and seeing what happens, in case there is a terminal event,
        it stops the execution
        :return:
        """
        if self.cannonball is None:
            return None

        self.cannonball.tick((1.0 / constants.FPS) * constants.X_SPEED)

        if self.terrain.collides_with(self.cannonball.position):
            last_position = self.cannonball.position
            return TerrainImpact(last_position)

        for tank in self.tanks:
            if tank.collides_with(self.cannonball.position):
                self.running = False
                self.winner = self.actual_player
                return TankImpact(self.cannonball.position)

        return None

    def wait_release_space(self) -> None:
        """
        This method waits until the actual player releases the space key, because if we do not wait until the release,
        the player could shoot a very short trajectory, and they accidentally shoot as the other player.
        :return: None
        """
        while pygame.key.get_pressed()[pygame.K_SPACE]:
            self.check_running()
            self.render()

    def start(self) -> None:
        # Instrucciones
        self.hud.show_instructions(self.screen)

        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.clock.tick(constants.FPS)

        self.wait_release_space()

        while self.running:
            self.check_running()
            # Select the angle
            while self.running and self.cannonball is None:
                self.check_running()
                self.process_input()
                self.render()

            # Travel of the cannonball
            while self.running and self.last_state is None:
                self.check_running()
                print(self.process_cannonball_trajectory())
                self.last_state = self.process_cannonball_trajectory()
                self.render()

            self.wait_release_space()

            while self.running:
                self.check_running()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_SPACE]:
                    break
                self.render()

            if isinstance(self.last_state, Impact):
                other_player = (self.actual_player + 1) % 2
                self.tanks[self.actual_player].player.score(
                    self.last_state, self.tanks[other_player].position
                )
                print(
                    "puntaje ",
                    self.actual_player,
                    ":",
                    self.tanks[self.actual_player].player.points,
                )

            self.cannonball = None
            self.last_state = None

            self.wait_release_space()
            self.actual_player = (self.actual_player + 1) % 2  # Swap actual player
            self.render()

        while self.winner is not None:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()


def main():
    tank_game = TankGame()
    tank_game.start()


if __name__ == "__main__":
    main()
