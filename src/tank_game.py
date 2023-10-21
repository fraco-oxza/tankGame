import math
from random import randint
from typing import Optional

import pygame

import constants
from background import Background
from caches import audio_cache, font_cache, animation_cache
from cannonballs import Cannonball
from cannonballs import CannonballType
from explotion import Explosion
from hud import HUD
from impact import Impact, ImpactType
from in_game_menu import InGameMenu
from in_game_menu import InGameMenuStatus
from map import Map
from menu import Menu
from player import Player
from snow_storm import SnowStorm
from tank import Tank
from terrain import Terrain
from warning_windows import WarningWindows
from winner_screen import WinnerScreen


class TankGame:
    """
    This class represents the complete game, it is responsible for maintaining the
    tanks, bullets, controlling user input, drawing, among others. It can be said that
    it is the central class of the project.
    """

    terrain: Terrain
    tanks: list[Tank]
    screen: pygame.Surface
    cannonball: Optional[Cannonball]
    map_size: tuple[int, int]
    running: bool
    actual_player: int
    winner: Optional[int]
    winner_msj: WinnerScreen
    last_state: Optional[Impact]
    warning = Optional[WarningWindows]

    def __init__(self, screen: pygame.surface.Surface) -> None:
        """
        constructor that initializes each element within the game, in
        addition to starting the window itself of the game.
        """

        self.fontReiniciar = font_cache["Roboto.ttf", 25]
        self.map_size = (
            constants.WINDOWS_SIZE[0] - 2 * constants.BORDER_PADDING,
            constants.WINDOWS_SIZE[1]
            - constants.HUD_HEIGHT
            - 2 * constants.BORDER_PADDING,
        )
        self.map = Map()
        self.background = Background(self.map.define_background_image())
        self.snow_storm = SnowStorm(self.map.define_storm_color())
        self.terrain = Terrain(
            self.map_size,
            constants.MOUNTAINS,
            constants.VALLEYS,
            self.map.define_terrain_colors(),
        )
        self.fps = float(constants.FPS)
        self.winner_msj = WinnerScreen(self)
        self.winner = None
        self.running = True
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.last_state = None
        self.cannonball = None
        self.menu = Menu(self.snow_storm)
        self.tanks = []
        self.actual_player = randint(0, 1)
        self.animacion = None
        quart_of_windows = int(self.map_size[0] / 4)

        tank_pos_border_margin = int(quart_of_windows / 4)

        mid_point = randint(
            int(quart_of_windows + tank_pos_border_margin),
            int(3 * quart_of_windows - tank_pos_border_margin),
        )

        tank1_x = randint(tank_pos_border_margin, mid_point - quart_of_windows)
        tank2_x = randint(
            mid_point + quart_of_windows, self.map_size[0] - tank_pos_border_margin
        )

        player1 = Player("1", 0)
        player2 = Player("2", 0)

        self.tanks.append(
            Tank(
                pygame.Color(50, 50, 0),
                pygame.Vector2(
                    tank1_x,
                    self.map_size[1]
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
                    self.map_size[1]
                    - self.terrain.ground_lines[
                        tank2_x // constants.TERRAIN_LINE_WIDTH - 1
                    ]
                    - 15,
                ),
                player2,
            )
        )

        self.in_game_menu = InGameMenu(self.screen, self.snow_storm)
        self.hud = HUD(self.tanks, self)
        self.warning = WarningWindows(self)

    def render(self) -> None:
        """
        This method is responsible for drawing each element of the window, it
        also puts the execution to sleep for a while to make the game run at the
        fps, specified in the FPS constant
        """
        game_rect = pygame.surface.Surface(self.map_size)

        self.background.draw(game_rect)
        self.snow_storm.draw(game_rect)
        self.terrain.draw(game_rect)

        for tank in self.tanks:
            tank.draw(game_rect)

        if self.cannonball is not None:
            self.cannonball.draw(game_rect)

        self.screen.fill(constants.HUD_BACKGROUND)
        if self.last_state is not None and self.cannonball is not None:
            self.cannonball.draw_trajectory(game_rect)
        if self.animacion is not None:
            self.animacion.draw(game_rect)
        self.screen.blit(
            game_rect, (constants.BORDER_PADDING, constants.BORDER_PADDING)
        )

        self.hud.draw(self.screen)

        self.snow_storm.tick(1.0 / (self.fps + 0.1))
        if self.cannonball is None and self.last_state is None:
            self.warning.draw(self.screen)
            if (
                self.warning.quantity_mm_60() is False
                or self.warning.quantity_mm_105() is False
                or self.warning.quantity_mm_80() is False
            ):
                error = audio_cache["sounds/error.mp3"]
                error.play()

        if self.winner is not None:
            self.winner_msj.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(constants.FPS)
        self.fps = self.clock.get_fps()

    def check_running(self):
        """
        This method checks if the player has sent the signal to close the window and
        stops the execution if this is the case, it is also responsible for cleaning
        any position that has been left unused.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def process_input(self) -> None:
        """
        This method is responsible for reading from the keyboard what the user wants
        to do, modifying the attributes of the tanks or creating the cannonball.
        :return:
        """
        playing_tank = self.tanks[self.actual_player]

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_DOWN]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle += math.radians(1) * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_angle += math.radians(0.1) * (
                    constants.FPS / self.fps
                )

        if keys_pressed[pygame.K_UP]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle -= math.radians(1) * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_angle -= math.radians(0.1) * (
                    constants.FPS / self.fps
                )

        if keys_pressed[pygame.K_RIGHT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity += 1 * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_velocity += 0.1 * (constants.FPS / self.fps)

            playing_tank.shoot_velocity = min(
                constants.SHOOT_MAX_SPEED, playing_tank.shoot_velocity
            )

        if keys_pressed[pygame.K_LEFT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity -= 1 * (constants.FPS / self.fps)
            else:
                playing_tank.shoot_velocity -= 0.1 * (constants.FPS / self.fps)

            if playing_tank.shoot_velocity < 1:
                playing_tank.shoot_velocity = 1

        if keys_pressed[pygame.K_SPACE]:
            self.cannonball = playing_tank.shoot()

        if (
            keys_pressed[pygame.K_1]
            or keys_pressed[pygame.K_2]
            or keys_pressed[pygame.K_3]
        ):
            change = audio_cache["sounds/click_cannonball.mp3"]
            change.play()
            if keys_pressed[pygame.K_1]:
                self.tanks[self.actual_player].actual = CannonballType.MM60
            elif keys_pressed[pygame.K_2]:
                self.tanks[self.actual_player].actual = CannonballType.MM80
            elif keys_pressed[pygame.K_3]:
                self.tanks[self.actual_player].actual = CannonballType.MM105
        if keys_pressed[pygame.K_ESCAPE]:
            self.process_in_game_menu()

    def process_in_game_menu(self):
        menu_state = self.in_game_menu.start_menu()

        if menu_state is InGameMenuStatus.EXIT:
            self.running = False
        elif menu_state is InGameMenuStatus.RESTART:
            TankGame.__init__(self, self.screen)
        elif menu_state is InGameMenuStatus.CONTINUE:
            pass

    def process_cannonball_trajectory(self) -> Optional[Impact]:
        """
        This method is responsible for moving the cannonball and seeing what happens,
        in case there is a terminal event, it stops the execution
        :return:
        """
        if self.cannonball is None:
            return None

        self.cannonball.tick((1.0 / self.fps) * constants.X_SPEED)

        if (
            self.cannonball.position.x < 0
            or self.cannonball.position.x > self.map_size[0]
        ):
            return Impact(self.cannonball.position, ImpactType.BORDER)

        if self.terrain.collides_with(self.cannonball.position):
            return Impact(self.cannonball.position, ImpactType.TERRAIN)

        for tank in self.tanks:
            if self.cannonball is None:
                return
            other_player = (self.actual_player + 1) % 2
            if tank.collides_with(
                self.cannonball.position, self.tanks[self.actual_player].actual
            ):
                actual_radius_position = self.calculate_distance(self.actual_player)

                if (
                    actual_radius_position is not None
                    and actual_radius_position > constants.TANK_RADIO
                ):
                    other_radius_position = self.calculate_distance(other_player)
                    if (
                        other_radius_position is not None
                        and other_radius_position < constants.TANK_RADIO
                    ):
                        return Impact(self.cannonball.position, ImpactType.TANK)
                else:
                    return Impact(self.cannonball.position, ImpactType.SUICIDIO)

        return None

    def calculate_distance(self, player: int):
        if self.cannonball is None:
            return

        actual_radius = math.sqrt(
            ((self.tanks[player].position.x - self.cannonball.position.x) ** 2)
            + ((self.tanks[player].position.y - self.cannonball.position.y) ** 2)
        )
        return actual_radius

    def wait_release_space(self) -> None:
        """
        This method waits until the actual player releases the space key, because
        if we do not wait until the release, the player could shoot a very short
        trajectory, and they accidentally shoot as the other player.
        :return: None
        """
        while pygame.key.get_pressed()[pygame.K_SPACE]:
            self.check_running()
            self.render()

    def cannonball_travel(self) -> None:
        """
        This function is responsible for drawing the projectile's parabolic path,
        making it advance, and then drawing it.
        """
        while self.running and self.last_state is None:
            self.check_running()
            self.last_state = self.process_cannonball_trajectory()
            self.render()

    @staticmethod
    def life_tank(point: pygame.Vector2, tank: Tank, cannonball_type: int):
        """Esta función se encarga de quitar vida al tanque según la bala que impactó"""
        if cannonball_type == CannonballType.MM60:
            if (
                math.sqrt(
                    (point.x - tank.position.x) ** 2 + (point.y - tank.position.y) ** 2
                )
                <= constants.TANK_RADIO + 10
            ):
                tank.life = tank.life - 30
                if tank.life < 0:
                    tank.life = 0

        elif cannonball_type == CannonballType.MM80:
            if (
                math.sqrt(
                    (point.x - tank.position.x) ** 2 + (point.y - tank.position.y) ** 2
                )
                <= constants.TANK_RADIO + 20
            ):
                tank.life = tank.life - 40
                if tank.life < 0:
                    tank.life = 0
        elif cannonball_type == CannonballType.MM105:
            if (
                math.sqrt(
                    (point.x - tank.position.x) ** 2 + (point.y - tank.position.y) ** 2
                )
                <= constants.TANK_RADIO + 30
            ):
                tank.life = tank.life - 50
                if tank.life < 0:
                    tank.life = 0

    def wait_on_space(self) -> None:
        """
        This function will pause most of the game logic but won't completely
        block the execution. Updates of the background or similar elements will
        be displayed, but the game won't progress to menus or actions.
        """
        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()

    def check_last_state(self) -> None:
        """
        This function is responsible for checking what happened in the last shot
        and modifying the class fields to adapt to the outcome.
        """
        if self.last_state is not None:
            if self.last_state.impact_type == ImpactType.TANK:
                other_player = (self.actual_player + 1) % 2
                self.life_tank(
                    self.last_state.position,
                    self.tanks[other_player],
                    self.tanks[self.actual_player].actual,
                )

                self.tanks[self.actual_player].player.score(
                    self.last_state, self.tanks[other_player].position
                )
            elif self.last_state.impact_type == ImpactType.SUICIDIO:
                other_player = (self.actual_player + 1) % 2
                self.life_tank(
                    self.last_state.position,
                    self.tanks[self.actual_player],
                    self.tanks[self.actual_player].actual,
                )

                self.tanks[other_player].player.score(
                    self.last_state, self.tanks[self.actual_player].position
                )
            elif self.last_state.impact_type == ImpactType.TERRAIN:
                other_player = (self.actual_player + 1) % 2
                actual_radius_position = (
                    self.calculate_distance(self.actual_player)
                    - self.cannonball.radius_damage
                )
                if actual_radius_position > constants.TANK_RADIO:
                    other_radius_position = (
                        self.calculate_distance(other_player)
                        - self.cannonball.radius_damage
                    )
                    if other_radius_position < constants.TANK_RADIO:
                        self.life_tank(
                            self.last_state.position,
                            self.tanks[other_player],
                            self.tanks[self.actual_player].actual,
                        )
                        self.tanks[self.actual_player].player.score(
                            self.last_state, self.tanks[other_player].position
                        )
                        self.last_state.impact_type = ImpactType.TANK

                else:
                    self.last_state.impact_type = ImpactType.SUICIDIO
                    self.life_tank(
                        self.last_state.position,
                        self.tanks[self.actual_player],
                        self.tanks[self.actual_player].actual,
                    )
                    self.tanks[other_player].player.score(
                        self.last_state, self.tanks[self.actual_player].position
                    )

        if (
            self.last_state is not None
            and self.last_state.impact_type != ImpactType.BORDER
        ) and self.cannonball is not None:
            self.cannonball.kill()

    def terrain_destruction(self):
        if (
            self.last_state is not None
            and self.last_state.impact_type == ImpactType.BORDER
        ):
            # Aquí detengo porque este caso no me sirve
            return
        if self.cannonball is not None and self.last_state is not None:
            radius = self.cannonball.radius_damage
            if self.tanks[0].position.x in range(
                int(self.cannonball.position.x - radius),
                int(self.cannonball.position.x + radius),
            ):
                self.tanks[0].position.y += radius
            if self.tanks[1].position.x in range(
                int(self.cannonball.position.x - radius),
                int(self.cannonball.position.x + radius),
            ):
                self.tanks[1].position.y += radius
            for i in range(
                int(self.last_state.position.x) - radius,
                int(self.last_state.position.x) + radius,
            ):
                leftover_damage = math.sqrt(
                    max(0, radius**2 - (self.last_state.position.x - i) ** 2)
                )
                if i < len(self.terrain.new_ground_lines):
                    j = len(self.terrain.new_ground_lines[i]) - 1
                    while leftover_damage != 0 and j >= 0:
                        initial_height = self.terrain.new_ground_lines[i][j]
                        if initial_height >= leftover_damage:
                            self.terrain.ground_lines[i] -= leftover_damage
                            self.terrain.new_ground_lines[i][j] -= leftover_damage
                            leftover_damage = 0
                        else:
                            leftover_damage -= initial_height
                            self.terrain.new_ground_lines[i][j] = 0
                        j -= 1

    def start_menu(self):
        soundtrack = audio_cache["sounds/inicio.mp3"]
        soundtrack.play()
        while self.running:
            self.check_running()
            self.menu.draw(self.screen)
            self.menu.tick((1.0 / (self.fps + 0.1)))

            ms = pygame.mouse.get_pos()

            self.menu.is_hover = self.menu.collides_with(pygame.Vector2(*ms))

            if pygame.mouse.get_pressed()[0] and self.menu.is_hover:
                soundtrack.stop()
                click = audio_cache["sounds/click.mp3"]

                click.play()
                break

            pygame.display.flip()
            self.clock.tick(constants.FPS)
            self.fps = self.clock.get_fps()

    def display_explotion(self):
        if self.animacion is None:
            return

        while self.animacion.has_next():
            self.animacion.tick(1.0 / (self.fps + 0.001))
            self.render()

    def start(self) -> None:
        """
        Esta función muestra las instrucciones básicas para después dar paso al
        juego como tal. Se encarga de gestionar la situación actual, como cuál
        jugador es el turno, el ángulo del cañon o si se ha decidido disparar,
        donde en cuyo caso se comprobará si la bala sigue avanzando o si ha
        impactado con algo.
        """
        self.start_menu()

        self.hud.show_instructions(self.screen)
        pygame.display.flip()
        in_game = audio_cache["sounds/inGame.mp3"]
        in_game.play()
        in_game.set_volume(0.2)
        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                click = audio_cache["sounds/click.mp3"]
                click.play()
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
            throw = audio_cache["sounds/throw.mp3"]
            throw.play()
            fall = audio_cache["sounds/fall.mp3"]
            fall.set_volume(0.3)
            fall.play()

            self.cannonball_travel()
            fall.stop()

            if (
                self.last_state is not None
                and self.last_state.impact_type != ImpactType.BORDER
            ):
                if self.cannonball is not None and self.last_state.impact_type in (
                    ImpactType.TANK,
                    ImpactType.SUICIDIO,
                ):
                    tank_explotion = audio_cache["sounds/bomb.mp3"]
                    tank_explotion.play()
                    self.animacion = Explosion(
                        self.cannonball.position, animation_cache["tank_explosion"]
                    )
                elif (
                    self.cannonball is not None
                    and self.last_state.impact_type == ImpactType.TERRAIN
                ):
                    shoot = audio_cache["sounds/shoot.mp3"]
                    shoot.play()
                    self.animacion = Explosion(
                        self.cannonball.position, animation_cache["snow_explosion"]
                    )
                # Display explotion
                self.display_explotion()
                self.animacion = None

            self.terrain_destruction()

            self.wait_release_space()
            self.wait_on_space()

            self.check_last_state()

            self.cannonball = None

            self.wait_release_space()
            self.actual_player = (self.actual_player + 1) % 2  # Swap actual player
            self.render()

            are_tanks_without_live = False
            for tank in self.tanks:
                if self.last_state is not None:
                    if tank.life == 0 and (
                        self.last_state.impact_type == ImpactType.TANK
                    ):
                        self.winner = (self.actual_player + 1) % 2
                        self.running = False
                        are_tanks_without_live = True
                        break
                    if (
                        tank.life == 0
                        and self.last_state.impact_type == ImpactType.SUICIDIO
                    ):
                        self.winner = self.actual_player
                        self.running = False
                        are_tanks_without_live = True
                        break

            if are_tanks_without_live:
                break
            self.last_state = None
        if self.winner is not None:
            self.running = True
        while self.running:
            self.check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()
