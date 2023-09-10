import math
import random
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
        raise NotImplementedError


class Drawable:
    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        raise NotImplementedError


class Background(Drawable):
    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.line(
            screen,
            constants.DarkGreen,
            (0, constants.SEA_LEVEL + 140),
            (50, constants.SEA_LEVEL + 140),
            40,
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[350, 220], [20, 435], [680, 435]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[750, 220], [600, 430], [900, 430]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[1000, 120], [1280, 435], [680, 435]]
        )
        pygame.draw.polygon(
            screen, constants.White, [[265, 279], [349, 221], [436, 279]]
        )
        pygame.draw.polygon(
            screen, constants.White, [[750, 220], [699, 284], [801, 284]]
        )
        pygame.draw.polygon(
            screen, constants.White, [[1000, 120], [915, 206], [1075, 206]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[318, 265], [296, 282], [333, 282]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[348, 265], [333, 282], [370, 282]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[385, 265], [370, 282], [400, 282]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[727, 268], [717, 285], [734, 285]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[747, 268], [734, 285], [755, 285]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[765, 268], [755, 285], [775, 285]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[953, 189], [937, 207], [966, 207]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[979, 189], [966, 207], [992, 207]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[1005, 189], [992, 207], [1015, 207]]
        )
        pygame.draw.polygon(
            screen, constants.DarkGreen, [[1029, 189], [1015, 207], [1040, 207]]
        )
        pygame.draw.rect(screen, constants.Menu, pygame.Rect(0, 485, 1280, 720))
        # pygame.draw.line(screen, constants.TERRAIN_COLOR, (0, constants.SEA_LEVEL + 160), (50, constants.SEA_LEVEL + 160),50)
        # pygame.draw.polygon(screen, constants.TERRAIN_COLOR, [[159, 89], [23, 485], [260, 485]])
        # pygame.draw.line(screen, constants.TERRAIN_COLOR, (248, constants.SEA_LEVEL + 160), (361, constants.SEA_LEVEL + 160), 50)
        # pygame.draw.polygon(screen, constants.TERRAIN_COLOR, [[542, 114], [328, 485], [783, 485]])
        # pygame.draw.line(screen, constants.TERRAIN_COLOR, (679, constants.SEA_LEVEL + 160), (925, constants.SEA_LEVEL + 160),
        #                50)
        # pygame.draw.polygon(screen, constants.TERRAIN_COLOR, [[1280, 145], [861, 485], [1280, 486]])
        # pygame.draw.line(screen, constants.TERRAIN_COLOR, (1246, constants.SEA_LEVEL + 160), (1279, constants.SEA_LEVEL + 160),
        #                50)


class Terrain(Drawable, Collidable):
    ground_lines: list[int]

    def fondo(self):
        j = 0

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

    def Rect(self, lista: list, indexInicio: int, indexFinal: int):
        for i in range(indexInicio, indexFinal):
            lista.append(constants.SEA_LEVEL + 160)
        return lista

    def increaseMountain(self,lista:list,indexInicio:int, indexFinal:int):
        for i in range(indexInicio,indexFinal):
            h=lista[i-1]
            h = h + 3
            lista[i] = h
        return lista

    def decreaseMountain(self, lista: list, indexInicio: int, indexFinal: int):
        for i in range(indexInicio, indexFinal):
            h = lista[i - 1]
            h = h - 3
            lista[i] = h
        return lista

    def completeList(self):
        lista = [constants.SEA_LEVEL] * (
            constants.WINDOWS_SIZE[0] // constants.TERRAIN_LINE_WIDTH
        )
        arrayFinal = []
        for i in range(0, len(lista)):
            if (i % 214 == 0) & (i + 80 < 640):
                lista = self.increaseMountain(lista, i, i + 80)
                arrayFinal.append(i + 80)
            for j in range(0, len(arrayFinal)):
                lista = self.decreaseMountain(lista, arrayFinal[j], arrayFinal[j] + 80)
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
        new_x = self.position.x + 40 * math.cos(self.shoot_angle)
        new_y = self.position.y - 40 * math.sin(self.shoot_angle)

        pygame.draw.rect(
            screen, self.color, pygame.Rect(self.position.x, self.position.y, 20, 10)
        )
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.position.x, self.position.y + 10, 50, 20),
        )
        pygame.draw.rect(
            screen,
            constants.GRAY,
            pygame.Rect(self.position.x, self.position.y + 30, 50, 8),
        )

        # decoration IN PROCESS, IS UGLY NOW

        pygame.draw.circle(
            screen, constants.BLACK, (self.position.x, self.position.y + 35), 5
        )
        pygame.draw.circle(
            screen, constants.BLACK, (self.position.x + 10, self.position.y + 38), 5
        )
        pygame.draw.circle(
            screen, constants.BLACK, (self.position.x + 20, self.position.y + 40), 5
        )
        pygame.draw.circle(
            screen, constants.BLACK, (self.position.x + 30, self.position.y + 40), 5
        )
        pygame.draw.circle(
            screen, constants.BLACK, (self.position.x + 40, self.position.y + 38), 5
        )
        pygame.draw.circle(
            screen, constants.BLACK, (self.position.x + 50, self.position.y + 35), 5
        )

        # cannon

        pygame.draw.line(screen, self.color, self.position, (new_x, new_y), 5)

        pygame.draw.circle(screen, self.color, (new_x, new_y), 4)

    def collidesWith(self, point: pygame.Vector2) -> bool:
         fin = False
         if ( ((point.x - self.position.x)**2 + (point.y - self.position.y )**2)**(1/2) <= constants.TANK_RADIO):
             print(((point.x - self.position.x )**2 + (point.y - self.position.y))**(1/2))
             fin= True
         return fin

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
        """
        This method is responsible for drawing each element of the window, it also puts the execution to sleep for a
        while to make the game run at the fps, specified in the FPS constant
        :return:
        """
        self.screen.fill(constants.SKY_COLOR)
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

        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_DOWN]:
            playing_tank.shoot_angle += math.radians(0.1)
        if keysPressed[pygame.K_UP]:
            playing_tank.shoot_angle -= math.radians(0.5)
        if keysPressed[pygame.K_RIGHT]:
            playing_tank.shoot_velocity += 0.5
        if keysPressed[pygame.K_LEFT]:
            playing_tank.shoot_velocity -= 0.5
            if playing_tank.shoot_velocity < 1:
                playing_tank.shoot_velocity = 1
        if keysPressed[pygame.K_SPACE]:
            self.cannonball = playing_tank.shoot()

    def process_cannonball_trajectory(self) -> None:
        """
        This method is responsible for moving the cannonball and seeing what happens, in case there is a terminal event,
        it stops the execution
        :return:
        """
        self.cannonball.tick((1.0 / constants.FPS) * constants.X_SPEED)

        if self.terrain.collidesWith(self.cannonball.position):
            self.cannonball = None
            return

        for tank in self.tanks:
            if tank.collidesWith(self.cannonball.position):
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
