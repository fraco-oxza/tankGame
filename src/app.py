from abc import abstractmethod
from random import randint
import math
import random
from typing import Optional

import pygame

import constants


class Collidable:
    @abstractmethod
    def collidesWith(self, point: pygame.Vector2) -> bool:
        pass


class Drawable:
    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        pass

    @abstractmethod
    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


class Terrain(Drawable, Collidable):
    ground_lines: list[int]

    def mountain(self, lista: list[int], indiceInicial: int, indiceFinal: int):
        actualIncrease = 0
        for i in range(indiceInicial, indiceFinal):
            middle = (indiceFinal + indiceInicial) // 2
            if i - 5 <= middle & i + 5 >= middle:
                actualIncrease += 5
            else:
                if i < middle:
                    actualIncrease += randint(2, 8)
                else:
                    actualIncrease -= randint(2, 8)
                print(i)
            lista[i] += actualIncrease

        return lista

    def completeList(self):
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

    def __init__(self, mountains: int, valleys: int):
        self.ground_lines = self.completeList()

    def draw(self, screen: pygame.surface.Surface) -> None:
        for i in range(len(self.ground_lines)):
            pygame.draw.rect(
                screen,
                constants.TERRAIN_COLOR,
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i],
                    constants.TERRAIN_LINE_WIDTH,
                    self.ground_lines[i],
                ),
            )

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass

    def collidesWith(self, point: pygame.Vector2) -> bool:
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
        pygame.draw.circle(screen, "#ffaa00", self.position, 6)

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


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
    shoot_angle: float  # rad // CONVERSABLE

    def __init__(self, color: pygame.Color, position: pygame.Vector2):
        self.color = color
        self.position = position
        self.shoot_angle = 3.0 * math.pi / 4.0  # rad
        self.shoot_velocity = 145  # m/s
        # player no lo usaremos en las primeras

    def draw(self, screen: pygame.surface.Surface) -> None:
        new_x = self.position.x + 40 * math.cos(self.shoot_angle)
        new_y = self.position.y - 40 * math.sin(self.shoot_angle)

        pygame.draw.rect(
            screen, self.color, pygame.Rect(self.position.x, self.position.y, 20, 20)
        )
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.position.x, self.position.y - 10, 20, 10),
        )
        pygame.draw.line(screen, self.color, self.position, (new_x, new_y), 5)

        pygame.draw.circle(
            screen, constants.BLACK, (self.position.x + 20, self.position.y + 20), 10
        )

    def collidesWith(self, point: pygame.Vector2) -> bool:
        # Sofi jobs
        return True

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass

    def shoot(self) -> Cannonball:
        v_x = self.shoot_velocity * math.cos(self.shoot_angle)
        # the -1 is since in this system the vertical coordinates are inverted
        v_y = -1 * self.shoot_velocity * math.sin(self.shoot_angle)

        new_x = self.position.x + 40 * math.cos(self.shoot_angle)
        new_y = self.position.y - 40 * math.sin(self.shoot_angle)

        return Cannonball(pygame.Vector2(new_x, new_y), pygame.Vector2(v_x, v_y))


class HUD(Drawable):
    tanks: list[Tank]
    left = 100
    top = 600
    width = 160
    height = 50

    def __init__(self, tanks: list[Tank]):
        self.TankGame = TankGame
        self.tanks = tanks
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_angle1 = None
        self.text_angle2 = None

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
        screen.blit(self.text_angle1, (self.left + 5, self.top + 5))
        screen.blit(self.text_angle2, (self.left + 905, self.top + 5))

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


class TankGame:
    terrain: Terrain
    tanks: list[Tank]
    screen: pygame.Surface
    cannonball: Optional[Cannonball]

    def __init__(self) -> None:
        self.running = True
        self.terrain = Terrain(constants.MOUNTAINS, constants.VALLEYS)

        pygame.init()
        self.screen = pygame.display.set_mode(constants.WINDOWS_SIZE)
        self.clock = pygame.time.Clock()
        self.cannonball = None
        self.tanks = list()

        quart_of_windows = int(constants.WINDOWS_SIZE[0] / 4)

        mid_point = randint(int(quart_of_windows), int(3 * quart_of_windows))

        tank1_x = randint(0, mid_point - quart_of_windows)
        tank2_x = randint(mid_point + quart_of_windows, constants.WINDOWS_SIZE[0])

        self.tanks.append(
            Tank(
                pygame.Color(255, 0, 0),
                pygame.Vector2(
                    tank1_x,
                    constants.WINDOWS_SIZE[1]
                    - self.terrain.ground_lines[
                        tank1_x // constants.TERRAIN_LINE_WIDTH - 1
                    ],
                ),
            )
        )

        self.tanks.append(
            Tank(
                pygame.Color(0, 0, 255),
                pygame.Vector2(
                    tank2_x,
                    constants.WINDOWS_SIZE[1]
                    - self.terrain.ground_lines[
                        tank2_x // constants.TERRAIN_LINE_WIDTH - 1
                    ],
                ),
            )
        )

        self.hud = HUD(self.tanks)

    def render(self) -> None:
        self.screen.fill(constants.SKY_COLOR)
        self.terrain.draw(self.screen)

        for tank in self.tanks:
            tank.draw(self.screen)

        if self.cannonball != None:
            self.cannonball.draw(self.screen)

        self.hud.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(constants.FPS)

    def check_running(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def start(self) -> None:
        actual_player = randint(0, 1)
        pygame.display.set_caption("TankGame!")
        icon = pygame.image.load("tankIcon.png")
        pygame.display.set_icon(icon)
        while self.running:
            self.check_running()

            playing_tank = self.tanks[actual_player]

            # Select the angle
            while self.running and self.cannonball is None:
                self.check_running()
                keysPressed = pygame.key.get_pressed()
                if keysPressed[pygame.K_DOWN]:
                    playing_tank.shoot_angle += math.radians(1)
                if keysPressed[pygame.K_UP]:
                    playing_tank.shoot_angle -= math.radians(1)
                if keysPressed[pygame.K_RIGHT]:
                    playing_tank.shoot_velocity += 1
                if keysPressed[pygame.K_LEFT]:
                    playing_tank.shoot_velocity -= 1
                    if playing_tank.shoot_velocity < 1:
                        playing_tank.shoot_velocity = 1
                if keysPressed[pygame.K_SPACE]:
                    self.cannonball = playing_tank.shoot()
                self.render()

            # Travel of the cannonball
            while self.running and self.cannonball is not None:
                self.check_running()
                self.cannonball.tick((1.0 / constants.FPS) * constants.X_SPEED)

                if self.terrain.collidesWith(self.cannonball.position):
                    self.cannonball = None

                self.render()

            while pygame.key.get_pressed()[pygame.K_SPACE]:
                self.check_running()
                self.render()

            actual_player = (actual_player + 1) % 2
            self.render()


def main():
    a = TankGame()
    a.start()


if __name__ == "__main__":
    main()
