from __future__ import annotations

import math
import random
from abc import abstractmethod
from random import randint
from typing import Optional

import pygame

import constants


class Collidable:
    @abstractmethod
    def collides_with(self, point: pygame.Vector2) -> bool:
        raise NotImplementedError


class Drawable:
    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        raise NotImplementedError


class Background(Drawable):
    @staticmethod
    def sky():
        sky = pygame.image.load("sky.jpg")
        sky_rect = sky.get_rect()
        sky = pygame.transform.scale(sky, constants.WINDOWS_SIZE)

        return sky_rect, sky

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen_rect, sky = Background.sky()
        screen.blit(sky, screen_rect.topleft)


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
            self.ground_lines[k] += ((k - i) ** 2) / 200.0

        for k in range(m, j):
            self.ground_lines[k] += ((j - k) ** 2) / 200.0

    def __init__(self, mountains: int, valleys: int):
        self.ground_lines = [constants.SEA_LEVEL] * (
            constants.WINDOWS_SIZE[0] // constants.TERRAIN_LINE_WIDTH
        )
        self.sin_mountain(0, 500)
        self.sin_mountain(400, 600)

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
                "#222222",
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i] + 20,
                    constants.TERRAIN_LINE_WIDTH,
                    self.ground_lines[i] - 20,
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

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        self.position = position
        self.velocity = velocity

    def tick(self, dt: float):
        self.position += self.velocity * dt
        self.velocity[1] += constants.GRAVITY * dt

    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.circle(screen, "#ff0000", self.position, 2)


class Player:
    name: str
    points: float

    def __init__(self, name: str, points: float):
        self.name = name
        self.points = points


class Tank(Drawable, Collidable):
    player: Player
    color: pygame.Color
    position: pygame.Vector2
    shoot_velocity: float  # m/s
    shoot_angle: float  # rad //

    def __init__(self, color: pygame.Color, position: pygame.Vector2):
        self.color = color
        self.position = position
        self.shoot_angle = 3.0 * math.pi / 4.0  # rad
        self.shoot_velocity = 145  # m/s
        # player no lo usaremos en las primeras

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
    top = 600
    width = 160
    height = 50

    def __init__(self, tanks: list[Tank], tank_game: TankGame):
        self.tank_game = tank_game
        self.tanks = tanks
        self.font = pygame.font.Font("Roboto.ttf", 24)
        self.text_angle1 = None
        self.text_angle2 = None
        self.text_velocity1 = None
        self.text_velocity2 = None

    def draw(self, screen: pygame.surface.Surface) -> None:
        if self.tanks[0].shoot_angle * (180 / 3.14) > 360:
            self.tanks[0].shoot_angle = 0
        elif self.tanks[0].shoot_angle * (180 / 3.14) < 0:
            self.tanks[0].shoot_angle = 6.28319
        if self.tanks[1].shoot_angle * (180 / 3.14) > 360:
            self.tanks[1].shoot_angle = 0
        elif self.tanks[1].shoot_angle * (180 / 3.14) < 0:
            self.tanks[1].shoot_angle = 6.28319
        self.text_angle1 = self.font.render(
            "Ángulo: " + str(int(self.tanks[0].shoot_angle * (180 / 3.14))) + "°",
            True,
            "white",
        )
        self.text_angle2 = self.font.render(
            "Ángulo: " + str(int(self.tanks[1].shoot_angle * (180 / 3.14))) + "°",
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
        icon = pygame.image.load("tankIcon.png")
        pygame.display.set_icon(icon)

        self.background = Background()
        self.terrain = Terrain(constants.MOUNTAINS, constants.VALLEYS)

        self.winner = None
        self.running = True
        self.screen = pygame.display.set_mode(constants.WINDOWS_SIZE)
        self.clock = pygame.time.Clock()

        self.cannonball = None
        self.tanks = []
        self.actual_player = randint(0, 1)

        quart_of_windows = int(constants.WINDOWS_SIZE[0] / 4)

        mid_point = randint(int(quart_of_windows), int(3 * quart_of_windows))

        tank1_x = randint(0, mid_point - quart_of_windows)
        tank2_x = randint(mid_point + quart_of_windows, constants.WINDOWS_SIZE[0])

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
            playing_tank.shoot_angle += math.radians(0.5)
        if keys_pressed[pygame.K_UP]:
            playing_tank.shoot_angle -= math.radians(0.5)
        if keys_pressed[pygame.K_RIGHT]:
            playing_tank.shoot_velocity += 0.5
        if keys_pressed[pygame.K_LEFT]:
            playing_tank.shoot_velocity -= 0.5
            if playing_tank.shoot_velocity < 1:
                playing_tank.shoot_velocity = 1
        if keys_pressed[pygame.K_SPACE]:
            self.cannonball = playing_tank.shoot()

    def process_cannonball_trajectory(self) -> None:
        """
        This method is responsible for moving the cannonball and seeing what happens, in case there is a terminal event,
        it stops the execution
        :return:
        """
        self.cannonball.tick((1.0 / constants.FPS) * constants.X_SPEED)

        if self.terrain.collides_with(self.cannonball.position):
            self.cannonball = None
            return

        for tank in self.tanks:
            if tank.collides_with(self.cannonball.position):
                self.running = False
                self.winner = (self.actual_player + 1) % 2
                return

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
        while self.running:
            self.check_running()

            # Select the angle
            while self.running and self.cannonball is None:
                self.check_running()
                self.process_input()
                self.render()

            # Travel of the cannonball
            while self.running and self.cannonball is not None:
                self.check_running()
                self.process_cannonball_trajectory()
                self.render()

            self.wait_release_space()
            self.actual_player = (self.actual_player + 1) % 2  # Swap actual player
            self.render()

        if self.winner is not None:
            print("Ha ganado el jugador ", self.winner)


def main():
    tank_game = TankGame()
    tank_game.start()


if __name__ == "__main__":
    main()
