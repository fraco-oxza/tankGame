from enum import Enum
import math
import random
from typing import Optional

import pygame

from background import Background
from caches import animation_cache, audio_cache, font_cache
from cannonballs import CannonballType
import constants
import context
from context import Context
from explotion import Explosion
from hud import HUD
from impact import Impact, ImpactType
from winner_screen import WinnerScreen
from in_game_menu import InGameMenu
from in_game_menu import InGameMenuStatus
from map import Map
from menu import Menu
from player import Player
from snow_storm import SnowStorm
from tank import Tank
from terrain import Terrain
from warning_windows import WarningWindows


class ResultType(Enum):
    Normal = 0
    ExitRequested = 1


class Round:
    tanks: list[Tank]
    context: Context
    players: list[Player]
    turns_queue: list[int]
    actual_player: int

    def __init__(self, players: list[Player]):
        self.context = context.instance
        self.map = Map()
        self.background = Background(self.map.define_background_image())
        self.snow_storm = SnowStorm(self.map.define_storm_color())
        self.terrain = Terrain(
            self.context.map_size,
            constants.MOUNTAINS,
            constants.VALLEYS,
            self.map.define_terrain_colors(),
        )
        # TODO: Add the winner screen
        self.winner_msj = WinnerScreen(self)
        self.players = players
        self.winner = None
        self.running = True
        self.turns_queue = []
        self.animacion = None

        self.last_state = None
        self.cannonball = None
        self.menu = Menu(self.snow_storm)
        self.create_tanks()
        self.create_turns()

        self.actual_player = self.turns_queue[-1]
        self.turns_queue.pop()

        self.in_game_menu = InGameMenu(self.context.screen, self.snow_storm)
        self.hud = HUD(self.tanks, self)
        self.warning = WarningWindows(self)

    def create_turns(self) -> None:
        if len(self.turns_queue) != 0:
            return

        self.turns_queue = [*range(len(self.tanks))]
        random.shuffle(self.turns_queue)

    def create_tanks(self) -> None:
        self.tanks = []

        positions = self.generate_tanks_positions()
        for player, player_pos in zip(self.players, positions):
            self.tanks.append(Tank(player.color, pygame.Vector2(player_pos), player))

    def generate_tanks_positions(self) -> list[tuple[int, int]]:
        to_generate = len(self.players)
        segments_size = self.context.map_size[0] / to_generate

        points = []
        for zone in range(to_generate):
            center = ((zone * segments_size) + ((zone + 1) + segments_size)) / 2
            x = int(center + random.normalvariate(0, segments_size / 2))
            y = (
                self.context.map_size[1]
                - self.terrain.ground_lines[x // constants.TERRAIN_LINE_WIDTH - 1]
                - 15
            )
            points.append((x, y))

        return points

    def draw_cannonball_indicator(self, sf: pygame.surface.Surface):
        """This method allows you to track the bullet when it is not on the screen."""
        if self.cannonball is None:
            return

        if self.cannonball.position.y < 0:
            top_padding = 10

            pygame.draw.polygon(
                sf,
                "#2196F3",
                [
                    (self.cannonball.position.x, top_padding),
                    (self.cannonball.position.x - 10, top_padding + 10),
                    (self.cannonball.position.x + 10, top_padding + 10),
                ],
            )
            height = self.context.map_size[1] - self.cannonball.position.y
            height_text = font_cache["Roboto.ttf", 18].render(
                f" {height:.2f}[m] ", True, "#ffffff", "#2196F3"
            )

            sf.blit(
                height_text,
                (
                    max(
                        0,
                        min(
                            self.cannonball.position.x - height_text.get_size()[0] // 2,
                            self.context.map_size[0] - height_text.get_size()[0],
                        ),
                    ),
                    (top_padding + 10),
                ),
            )

    def render(self) -> None:
        """
        This method is responsible for drawing each element of the window, it
        also puts the execution to sleep for a while to make the game run at the
        fps, specified in the FPS constant
        """
        game_rect = pygame.surface.Surface(self.context.map_size)

        self.background.draw(game_rect)
        self.snow_storm.draw(game_rect)
        self.terrain.draw(game_rect)
        self.draw_cannonball_indicator(game_rect)

        for tank in self.tanks:
            tank.draw(game_rect)

        if self.cannonball is not None:
            self.cannonball.draw(game_rect)

        self.context.screen.fill(constants.HUD_BACKGROUND)
        if self.last_state is not None and self.cannonball is not None:
            self.cannonball.draw_trajectory(game_rect)
        if self.animacion is not None:
            self.animacion.draw(game_rect)
        self.context.screen.blit(
            game_rect, (constants.BORDER_PADDING, constants.BORDER_PADDING)
        )

        self.hud.draw(self.context.screen)

        self.snow_storm.tick(1.0 / (self.fps + 0.1))
        if self.cannonball is None and self.last_state is None:
            self.warning.draw(self.context.screen)
            if not self.warning.is_current_cannonball_available():
                error = audio_cache["sounds/error.mp3"]
                error.play()

        if self.winner is not None:
            self.winner_msj.draw(self.context.screen)

        pygame.display.flip()
        self.context.clock.tick(constants.FPS)
        self.fps = self.context.clock.get_fps()

    def check_running(self):
        """
        This method checks if the player has sent the signal to close the
        window and stops the execution if this is the case, it is also
        responsible for cleaning any position that has been left unused.
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
            click = audio_cache["sounds/click.mp3"]
            click.play()
            self.process_in_game_menu()

    def process_in_game_menu(self):
        """This method allows you to check if the pause menu is active or not."""
        menu_state = self.in_game_menu.start_menu()

        if menu_state is InGameMenuStatus.EXIT:
            self.running = False
        elif menu_state is InGameMenuStatus.RESTART:
            # TODO: Ver que hacer con esto en base al nuevo modelo
            # TankGame.__init__(self, self.context)
            pass
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
            or self.cannonball.position.x > self.context.map_size[0]
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
        """
        This method takes care of the destruction of terrain, the fall of tanks and the damage related to this.
        """
        if (
            self.last_state is not None
            and self.last_state.impact_type == ImpactType.BORDER
        ):
            # Aquí detengo porque este caso no me sirve
            return

        if self.cannonball is not None and self.last_state is not None:
            radius = self.cannonball.radius_damage
            # FIXME: Esto esta muy mal con el nuevo modelo
            if self.tanks[0].position.x in range(
                int(self.cannonball.position.x - radius),
                int(self.cannonball.position.x + radius),
            ):
                self.tanks[0].position.y += radius
                self.tanks[0].life -= 10
            if self.tanks[1].position.x in range(
                int(self.cannonball.position.x - radius),
                int(self.cannonball.position.x + radius),
            ):
                self.tanks[1].position.y += radius
                self.tanks[1].life -= 10
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
        """This method takes care of the menu music and the start button click."""
        soundtrack = audio_cache["sounds/inicio.mp3"]
        soundtrack.play()
        while self.running:
            self.check_running()
            self.menu.draw(self.context.screen)
            self.menu.tick((1.0 / (self.fps + 0.1)))

            ms = pygame.mouse.get_pos()

            self.menu.is_hover = self.menu.collides_with(pygame.Vector2(*ms))

            if pygame.mouse.get_pressed()[0] and self.menu.is_hover:
                soundtrack.stop()
                click = audio_cache["sounds/click.mp3"]

                click.play()
                break

            pygame.display.flip()
            self.context.clock.tick(constants.FPS)
            self.context.fps = self.context.clock.get_fps()

    def display_explotion(self):
        """This method is responsible for the animation of the explosion."""
        if self.animacion is None:
            return

        while self.animacion.has_next():
            self.animacion.tick(1.0 / (self.fps + 0.001))
            self.render()

    def start(self) -> None:
        """
        This method shows the basic instructions and then gives way to the
        game as such. It is responsible for managing the current situation, such as which
        player's turn, the angle of the cannon or if it has been decided to shoot,
        where in which case it will be checked if the bullet continues to advance or if it has
        shocked with something.
        """
        self.start_menu()

        self.hud.show_instructions(self.context.screen)
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
            self.context.clock.tick(constants.FPS)

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
            if len(self.turns_queue) == 0:
                self.create_turns()
            self.actual_player = self.turns_queue[-1]  # Swap actual player
            self.turns_queue.pop()
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
