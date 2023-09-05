from abc import abstractmethod
from random import randint, random

import pygame
from pygame.scrap import contains

import constants


class Drawable:
    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        pass

    @abstractmethod
    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


class Terrain(Drawable):
    ground_lines: list[int]

    def __init__(self, mountains: int, valleys: int):
        # Este es el constructor, aquí puedes hacer la lógica
        # que cree las ground_lines
        width = constants.WINDOWS_SIZE[0]
        self.ground_lines = [constants.SEA_LEVEL] * int(
            width / constants.TERRAIN_LINE_WIDTH
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        for i in range(len(self.ground_lines)):
            pygame.draw.rect(
                screen,
                "green",
                pygame.Rect(
                    i * constants.TERRAIN_LINE_WIDTH,
                    constants.WINDOWS_SIZE[1] - self.ground_lines[i],
                    constants.TERRAIN_LINE_WIDTH,
                    self.ground_lines[i],
                ),
            )

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


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
        pass

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


class Player:
    name: str
    points: float

    def __init__(self, name: str, points: float):
        self.name = name
        self.points = points


class Tank(Drawable):
    player: Player
    color: pygame.Color
    position: pygame.Vector2
    shoot_velocity: float  # m/s
    shoot_angle: float  # rads

    def __init__(self, color: pygame.Color, position: pygame.Vector2):
        self.color = color
        self.position = position
        # player no lo usaremos en las primeras

    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.position, 5)

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


class TankGame:
    terrain: Terrain
    tanks: list[Tank]
    screen: pygame.Surface

    def __init__(self) -> None:
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
                        tank1_x // constants.TERRAIN_LINE_WIDTH
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
                        tank2_x // constants.TERRAIN_LINE_WIDTH
                    ],
                ),
            )
        )

    def start(self) -> None:
        running = True
        actual_player = randint(0, 1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(constants.SKY_COLOR)
            playing_tank = self.tanks[actual_player]

            # IN PROGRESS
            # keys_pressed = pygame.key.get_pressed()
            # if keys_pressed[pygame.K_DOWN]:
            # pass
            # if keys_pressed[pygame.K_UP]:
            # pass
            # if keys

            # Select angle and velocity

            # Swap the actual player
            actual_player = (actual_player + 1) % 2

            for tank in self.tanks:
                tank.draw(self.screen)

            self.terrain.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(60)


def main():
    a = TankGame()
    a.start()


if __name__ == "__main__":
    main()
