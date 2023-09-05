from abc import abstractmethod
from random import randint, random

import pygame

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
        pygame.display.flip()

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

    def __init__(self, color: pygame.Color, position: pygame.Vector2):
        self.color = color
        self.position = position
        # player no lo usaremos en las primeras

    def draw(self, screen: pygame.surface.Surface) -> None:
        pass

    def erase(self, screen: pygame.surface.Surface) -> None:
        pass


class TankGame:
    terrain: Terrain
    tanks: list[Tank]
    cannonball: None | Cannonball
    screen: pygame.Surface

    def __init__(self) -> None:
        self.terrain = Terrain(constants.MOUNTAINS, constants.VALLEYS)

        pygame.init()
        self.screen = pygame.display.set_mode(constants.WINDOWS_SIZE)
        self.clock = pygame.time.Clock()
        self.cannonball = None

        # TODO: Inicializar tanques y asi

    def start(self) -> None:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(constants.SKY_COLOR)
            self.terrain.draw(self.screen)
            self.clock.tick(constants.FPS)


def main():
    a = TankGame()
    a.start()


if __name__ == "__main__":
    main()
