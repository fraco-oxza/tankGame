from abc import abstractmethod
from random import randint
import math
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
        pygame.draw.circle(screen, "blue", self.position, 4)

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
    shoot_angle: float  # rad

    def __init__(self, color: pygame.Color, position: pygame.Vector2):
        self.color = color
        self.position = position
        self.shoot_angle = 0.2
        self.shoot_velocity = 145  # m/s
        # player no lo usaremos en las primeras

    def draw(self, screen: pygame.surface.Surface) -> None:
        #pygame.draw.circle(screen, self.color, self.position, 10)
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position.x, self.position.y, 20, 20))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position.x, self.position.y-10, 20, 10))
        pygame.draw.polygon(screen, self.color, ((self.position.x, self.position.y-10), (self.position.x +2, self.position.y+2),
                                                 (self.position.x + 55, self.position.y - 35), (self.position.x + 10, self.position.y-10)))

        pygame.draw.circle(screen, constants.BLACK, (self.position.x +20 , self.position.y+20), 10)
    def erase(self, screen: pygame.surface.Surface) -> None:
        pass

    def shoot(self) -> Cannonball:
        v_x = self.shoot_velocity * math.cos(self.shoot_angle)
        # the -1 is since in this system the vertical coordinates are inverted
        v_y = -1 * self.shoot_velocity * math.sin(self.shoot_angle)

        return Cannonball(
            pygame.Vector2(self.position.x, self.position.y), pygame.Vector2(v_x, v_y)
        )


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
                        tank2_x // constants.TERRAIN_LINE_WIDTH - 1
                    ],
                ),
            )
        )

    def start(self) -> None:
        running = True
        actual_player = randint(0, 1)
        pygame.display.set_caption("TankGame!")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            playing_tank = self.tanks[actual_player]
            self.screen.fill(constants.SKY_COLOR)

            # IN PROGRESS
            # keys_pressed = pygame.key.get_pressed()
            # if keys_pressed[pygame.K_DOWN]:
            # pass
            # if keys_pressed[pygame.K_UP]:
            # pass
            # if keys

            actual_player = (actual_player + 1) % 2
            self.terrain.draw(self.screen)

            for tank in self.tanks:
                tank.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(constants.FPS)


def main():
    a = TankGame()
    a.start()


if __name__ == "__main__":
    main()
