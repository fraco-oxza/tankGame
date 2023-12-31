import math
import random
from typing import Optional

import pygame
from pygame.key import ScancodeWrapper

import constants
import context
from background import Background
from bot import Bot
from caches import animation_cache, audio_cache, font_cache
from cannonballs import CannonballType, Cannonball
from context import Context
from effects import AmbientEffect
from exit_requested import ExitRequested, RestartRequested
from explotion import Explosion
from hud import HUD
from impact import Impact, ImpactType
from in_game_menu import InGameMenu
from in_game_menu import InGameMenuStatus
from inputs import check_running
from map import Map
from menu import Menu
from player import Player
from shop_menu import Shop
from snow_storm import SnowStorm
from tank import Tank
from terrain import Terrain
from warning_windows import WarningWindows
from wind import Wind
from winner_screen import WinnerScreen


class Round:
    """
    This class is responsible for managing the game, it is responsible for
    creating the different elements of the game, managing the turns, managing
    the inputs, managing the different states of the game and managing the
    different menus.
    """

    tanks: list[Tank]
    context: Context
    players: list[Player]
    turns_queue: list[int]
    actual_player: int
    cannonball: Optional[Cannonball]
    tanks_alive: int
    wind: Optional[Wind]
    gravity: float

    def __init__(self):
        """
        This method is responsible for initializing the class, it creates the
        attributes of the class and calls the methods that are responsible for
        creating the different elements of the game.
        """
        self.tanks_falling = None
        self.context = context.instance
        self.map = Map()

        if self.context.type_of_effect in [
            AmbientEffect.GRAVITY_AND_WIND,
            AmbientEffect.WIND,
        ]:
            self.wind = Wind()
        else:
            self.wind = None

        self.gravity = (
            constants.DEFAULT_GRAVITY
            if self.context.type_of_effect in [AmbientEffect.NONE, AmbientEffect.WIND]
            else random.uniform(constants.MIN_GRAVITY, constants.MAX_GRAVITY)
        )
        self.background = Background(self.map.define_background_image())
        self.snow_storm = SnowStorm(
            self.map.define_storm_color(), self.wind, self.gravity
        )
        self.terrain = Terrain(
            self.context.map_size,
            constants.MOUNTAINS,
            constants.VALLEYS,
            self.map.define_terrain_colors(),
        )

        self.tanks_alive = len(self.context.players)
        self.winner_msj = WinnerScreen(self)
        self.players = self.context.players
        self.winner = None
        self.running = True
        self.turns_queue = []
        self.animacion = None
        self.animacion_fuego = None
        self.last_state = None
        self.cannonball = None
        self.context.fps = constants.FPS
        self.menu = Menu(self.context.screen)
        self.create_tanks()
        self.create_turns()
        self.shop_menu = Shop(self.context.screen)
        self.throw_sound = audio_cache["sounds/throw.mp3"]
        self.fall_sound = audio_cache["sounds/fall.mp3"]
        self.fall_sound.set_volume(0.3)
        self.actual_player = self.turns_queue[-1]

        self.falling_speed = 0
        self.has_fallen = set()

        self.in_game_menu = InGameMenu(self.context.screen)
        self.hud = HUD(self.tanks, self, self.gravity, self.wind)
        self.warning = WarningWindows(self)

    def create_turns(self) -> None:
        """
        This method is responsible for creating the turns queue, it creates the
        queue based on the number of players.
        """
        if len(self.turns_queue) != 0:
            return

        self.turns_queue = [*range(len(self.tanks))]
        random.shuffle(self.turns_queue)

    def create_tanks(self) -> None:
        """
        This method is responsible for creating the tanks, it creates the tanks
        based on the number of players and the number of bots.
        """
        self.tanks = []
        positions = self.generate_tanks_positions()
        contador = 0
        for player, player_pos in zip(self.players, positions):
            if contador < context.instance.number_of_bots:
                self.tanks.append(Bot(player.color, pygame.Vector2(player_pos), player))
                contador = contador + 1
            else:
                self.tanks.append(
                    Tank(player.color, pygame.Vector2(player_pos), player)
                )

    def correct_tanks_position(self) -> None:
        """
        This method is responsible for correcting the position of the tanks,
        because when the terrain falls, the tanks can be left floating in the
        air or underground.
        """
        for tank in self.tanks:
            tank.position.y = (
                self.context.map_size[1]
                - self.terrain.ground_lines[
                    min(int(tank.position.x), len(self.terrain.ground_lines) - 1)
                ]
                - constants.TANK_OFFSET
            )

    def generate_tanks_positions(self) -> list[tuple[int, int]]:
        """
        This method is responsible for generating the positions of the tanks
        on the map. It generates the positions based on the number of players
        and the size of the map.
        """
        to_generate = len(self.players)
        segments_size = self.context.map_size[0] / to_generate

        points = []
        for zone in range(to_generate):
            center = ((zone * segments_size) + ((zone + 1) * segments_size)) / 2
            x = center + random.normalvariate(0, segments_size / 4)
            x = min(max(zone * segments_size, x), (zone + 1) * segments_size)
            x = int(x)
            y = (
                self.context.map_size[1]
                - self.terrain.ground_lines[x - 1]
                - constants.TANK_OFFSET
            )
            points.append((x, y))

        return points

    def find_tank(self):
        """
        This method is responsible for finding the tank that is alive and is
        not the player tank
        """
        current_tank = self.get_current_tank()
        if not isinstance(current_tank, Bot):
            return

        find = True
        while find:
            random_tank = random.randint(0, len(self.tanks) - 1)
            if random_tank != self.actual_player and self.tanks[random_tank].life > 0:
                current_tank.random_shoot(
                    self.tanks[random_tank].position, self.gravity
                )
                find = False

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
            game_rect, (self.context.border_padding, self.context.border_padding)
        )

        self.hud.draw(self.context.screen)

        self.snow_storm.tick(1.0 / self.context.fps)
        if self.cannonball is None and self.last_state is None:
            self.warning.draw(self.context.screen)
            if not self.warning.is_current_cannonball_available():
                error = audio_cache["sounds/error.mp3"]
                error.play()

        if self.winner is not None:
            self.winner_msj.draw(self.context.screen)

        if self.wind is not None:
            self.wind.tick(1.0 / self.context.fps)

        pygame.display.flip()
        self.context.clock.tick(constants.FPS)
        self.context.fps = self.context.clock.get_fps()

    def process_shoot_angle_change(
        self, playing_tank: Tank, keys_pressed: ScancodeWrapper
    ):
        """
        This method is responsible for changing the angle of the projectile that
        the player is going to shoot. It read the keys pressed and changes the
        angle of the projectile.
        """
        if keys_pressed[pygame.K_DOWN]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle += math.radians(1) * (
                    constants.FPS / self.context.fps
                )
            else:
                playing_tank.shoot_angle += math.radians(0.1) * (
                    constants.FPS / self.context.fps
                )

        if keys_pressed[pygame.K_UP]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_angle -= math.radians(1) * (
                    constants.FPS / self.context.fps
                )
            else:
                playing_tank.shoot_angle -= math.radians(0.1) * (
                    constants.FPS / self.context.fps
                )

    def process_shoot_speed_change(
        self, playing_tank: Tank, keys_pressed: ScancodeWrapper
    ):
        """
        This method is responsible for changing the speed of the projectile that
        the player is going to shoot. It read the keys pressed and changes the
        speed of the projectile.
        """
        if keys_pressed[pygame.K_RIGHT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity += 1 * (constants.FPS / self.context.fps)
            else:
                playing_tank.shoot_velocity += 0.1 * (constants.FPS / self.context.fps)

            playing_tank.shoot_velocity = min(
                constants.SHOOT_MAX_SPEED, playing_tank.shoot_velocity
            )

        if keys_pressed[pygame.K_LEFT]:
            if keys_pressed[pygame.K_LSHIFT]:
                playing_tank.shoot_velocity -= 1 * (constants.FPS / self.context.fps)
            else:
                playing_tank.shoot_velocity -= 0.1 * (constants.FPS / self.context.fps)

            if playing_tank.shoot_velocity < 1:
                playing_tank.shoot_velocity = 1

    @staticmethod
    def process_shoot_type_change(playing_tank: Tank, keys_pressed: ScancodeWrapper):
        """
        This method is responsible for changing the type of projectile that the
        player is going to shoot. It read the keys pressed and changes the type
        of projectile.
        """
        if (
            keys_pressed[pygame.K_1]
            or keys_pressed[pygame.K_2]
            or keys_pressed[pygame.K_3]
        ):
            change = audio_cache["sounds/click_cannonball.mp3"]
            change.play()
            if keys_pressed[pygame.K_1]:
                playing_tank.actual = CannonballType.MM60
            elif keys_pressed[pygame.K_2]:
                playing_tank.actual = CannonballType.MM80
            elif keys_pressed[pygame.K_3]:
                playing_tank.actual = CannonballType.MM105

    def process_input(self) -> None:
        """
        This method is responsible for reading from the keyboard what the user wants
        to do, modifying the attributes of the tanks or creating the cannonball.
        :return:
        """
        playing_tank = self.tanks[self.actual_player]
        keys_pressed = pygame.key.get_pressed()

        self.process_shoot_angle_change(playing_tank, keys_pressed)
        self.process_shoot_speed_change(playing_tank, keys_pressed)
        self.process_shoot_type_change(playing_tank, keys_pressed)

        if keys_pressed[pygame.K_SPACE]:
            self.cannonball = playing_tank.shoot()

        if keys_pressed[pygame.K_ESCAPE]:
            click = audio_cache["sounds/click.mp3"]
            click.play()
            self.process_in_game_menu()

    def process_in_game_menu(self):
        """This method allows you to check if the pause menu is active or not."""
        menu_state = self.in_game_menu.start_menu()

        if menu_state is InGameMenuStatus.EXIT:
            raise ExitRequested
        if menu_state is InGameMenuStatus.RESTART:
            raise RestartRequested

    def process_cannonball_trajectory(self) -> Optional[Impact]:
        """
        This method is responsible for moving the cannonball and seeing what happens,
        in case there is a terminal event, it stops the execution
        :return:
        """
        if self.cannonball is None:
            return None

        self.cannonball.tick((1.0 / self.context.fps) * constants.X_SPEED, self.gravity)

        if self.wind is not None:
            self.cannonball.position.x += (
                self.wind.velocity
                * (1.0 / self.context.fps)
                * constants.WIND_EFFECT_SCALE
            )

        if (
            self.cannonball.position.x < 0
            or self.cannonball.position.x > self.context.map_size[0]
        ):
            return Impact(self.cannonball.position, ImpactType.BORDER)

        if self.terrain.collides_with(self.cannonball.position):
            return Impact(self.cannonball.position, ImpactType.TERRAIN)

        for tank in self.tanks:
            if tank.collides_with(self.cannonball.position, self.cannonball.radius):
                return Impact(self.cannonball.position, ImpactType.TANK, tank)

        return None

    def get_current_tank(self):
        """
        This method is responsible for returning the tank that is currently
        playing.
        """
        return self.tanks[self.actual_player]

    def calculate_distance(self, tank: Tank) -> float:
        """
        This method is responsible for calculating the distance between the
        projectile and the tank.
        """
        if self.cannonball is None:
            return math.inf

        actual_radius = math.sqrt(
            ((tank.position.x - self.cannonball.position.x) ** 2)
            + ((tank.position.y - self.cannonball.position.y) ** 2)
        )

        return actual_radius

    def wait_release_space(self) -> None:
        """
        This method waits until the actual player releases the space key, because
        if we do not wait until the release, the player could shoot a very short
        trajectory, and they accidentally shoot as the other player.
        :return: None
        """
        if isinstance(self.get_current_tank(), Bot):
            pass
        else:
            while pygame.key.get_pressed()[pygame.K_SPACE]:
                check_running()
                self.render()

    def cannonball_travel(self) -> None:
        """
        This function is responsible for drawing the projectile's parabolic path,
        making it advance, and then drawing it.
        """
        self.fall_sound.play()
        while self.running and self.last_state is None:
            check_running()
            self.last_state = self.process_cannonball_trajectory()
            self.render()
        self.fall_sound.stop()

    def wait_on_space(self) -> None:
        """
        This function will pause most of the game logic but won't completely
        block the execution. Updates of the background or similar elements will
        be displayed, but the game won't progress to menus or actions.
        """
        while self.running:
            check_running()
            keys_pressed = pygame.key.get_pressed()
            if isinstance(self.get_current_tank(), Bot):
                break
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()

    def do_radius_damage(self):
        """
        This function is responsible for calculating the damage that the projectile
        will do to the tanks that are within the radius of action of the projectile.
        """
        if self.last_state is None or self.cannonball is None:
            return

        if self.last_state.impact_type != ImpactType.BORDER:
            for tank in self.tanks:
                if (
                    self.last_state.impact_type == ImpactType.TANK
                    and tank is self.last_state.impacted_tank
                ):
                    continue
                tank.life -= int(
                    (
                        self.cannonball.damage
                        / ((1.0 - self.calculate_distance(tank)) ** 2)
                    )
                    * 100
                )

    def check_last_state(self) -> None:
        """
        This function is responsible for checking what happened in the last shot
        and modifying the class fields to adapt to the outcome.
        """
        if self.last_state is None or self.cannonball is None:
            return

        if (
            self.last_state.impact_type == ImpactType.TANK
            and self.last_state.impacted_tank is not None
        ):
            self.last_state.impacted_tank.life -= self.cannonball.damage

        for tank in self.tanks:
            if tank.is_alive and tank.life <= 0:
                tank.is_alive = False
                tank.life = 0
                self.tanks_alive -= 1
                tank.player.deaths += 1

                if self.get_current_tank().player is not tank.player:
                    self.get_current_tank().player.money += 5000
                    self.get_current_tank().player.murders += 1
                else:
                    self.get_current_tank().player.money -= 5000

    def terrain_destruction(self):
        """
        This method takes care of the destruction of terrain, the fall of tanks
        and the damage related to this.
        """
        if (
            self.last_state is not None
            and self.last_state.impact_type == ImpactType.BORDER
        ):
            # Aquí detengo porque este caso no me sirve
            return

        if self.cannonball is not None and self.last_state is not None:
            radius = int(self.cannonball.radius_damage)
            imp_x, imp_y = self.cannonball.position
            imp_x = int(imp_x)
            imp_y = self.context.map_size[1] - imp_y

            for i in range(imp_x - radius, imp_x + radius + 1):
                left_damage = math.sqrt(max(radius**2 - (i - imp_x) ** 2, 0))

                sup_limit = imp_y + left_damage
                inf_limit = imp_y - left_damage
                if i < len(self.terrain.ground_lines):
                    current_line = self.terrain.new_ground_lines[i]

                    accumulated = 0
                    for j, size in enumerate(current_line):
                        start_layer = accumulated
                        end_layer = start_layer + size

                        affected = max(
                            0, min(end_layer, sup_limit) - max(start_layer, inf_limit)
                        )

                        self.terrain.ground_lines[i] -= affected

                        if sup_limit < end_layer:
                            fall = end_layer - max(sup_limit, start_layer)
                            self.terrain.falling[i][j] = (
                                self.context.map_size[1] - end_layer,
                                fall,
                            )
                            affected += fall
                            self.terrain.falling_speed = 0
                            self.terrain.is_falling = True

                        current_line[j] -= max(0, affected)
                        accumulated = end_layer

    def display_fire(self):
        """
        This method is responsible for the animation of the fire when a tank
        is not alive.
        """
        if self.animacion_fuego is None:
            return

        while self.animacion_fuego.has_next():
            self.animacion_fuego.tick(1.0 / (self.context.fps + 0.001))
            self.render()

    def display_explotion(self):
        """This method is responsible for the animation of the explosion."""
        if self.animacion is None:
            return

        while self.animacion.has_next():
            self.animacion.tick(1.0 / (self.context.fps + 0.001))
            self.render()

    def next_turn(self):
        """
        This method is responsible for changing the turn of the players. It is
        also responsible for create the turns queue.
        """
        if len(self.turns_queue) == 0:
            self.create_turns()

        self.actual_player = self.turns_queue[-1]  # Swap actual player
        self.turns_queue.pop()

    def make_tanks_fall(self, dt: float):
        """
        This method is responsible for making the tanks fall when the terrain
        is destroyed.
        """
        self.falling_speed += self.gravity * dt
        self.tanks_falling = False

        for i, tank in enumerate(self.tanks):
            x, y = tank.position
            x = int(x)
            y = self.context.map_size[1] - y - constants.TANK_OFFSET

            if y <= 0:
                if i in self.has_fallen:
                    tank.life = max(
                        0,
                        tank.life
                        - int(self.falling_speed * constants.DAMAGE_PER_SPEED),
                    )
                    self.has_fallen.discard(i)
                    tank.position.y = self.context.map_size[1]
                continue
            if max(x, 0) < len(self.terrain.ground_lines):
                if self.terrain.ground_lines[max(x, 0)] < y:
                    tank.position.y += self.falling_speed * dt
                    self.tanks_falling = True
                    self.has_fallen.add(i)
                elif i in self.has_fallen:
                    tank.life = max(
                        0,
                        tank.life
                        - int(self.falling_speed * constants.DAMAGE_PER_SPEED),
                    )
                    tank.position.y = (
                        self.context.map_size[1]
                        - self.terrain.ground_lines[int(tank.position.x)]
                        - constants.TANK_OFFSET
                    )
                    self.has_fallen.discard(i)

    def sleep_rendering(self, time_ms: int) -> None:
        """This method is responsible for making the game wait for a while."""
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < time_ms:
            check_running()
            self.render()

    def display_shop_menu(self):
        """
        This method is responsible for displaying the shop menu to buy
        ammunition.
        """
        for tank in self.tanks:
            if isinstance(tank, Bot):
                tank.buy_cannonballs()
            else:
                self.shop_menu.start_shop(tank)

    def update_wind(self):
        """
        This method is responsible for updating the wind speed. only if the
        wind is active.
        """
        if self.wind is not None:
            self.wind.change_speed()
            while self.wind.is_changing():
                check_running()
                self.render()

    def try_next_turn(self) -> bool:
        """
        This method is responsible for checking if the next player can shoot or
        not. If the player cannot shoot, it will pass the turn to the next one
        and return True. and if no one can shoot, it will return False.
        """
        tries = 0
        self.next_turn()
        while not self.get_current_tank().is_alive or (
            sum(self.get_current_tank().player.ammunition.values()) == 0
        ):
            self.next_turn()

            tries += 1
            if tries > 2 * self.context.number_of_players:
                return False
        return True

    def aim_and_shoot(self):
        """
        This method is responsible for aiming and shooting the projectile. If
        the player is a bot, it will aim and shoot automatically, otherwise it
        will wait for the player to press the space bar, and process their inputs
        to change the angle and speed.
        """
        if isinstance(self.get_current_tank(), Bot):
            self.find_tank()
            self.cannonball = self.get_current_tank().shoot()
        else:
            while self.running and self.cannonball is None:
                check_running()
                self.process_input()
                self.render()
        self.throw_sound.play()

    def do_explotion(self):
        """
        This method is responsible for displaying the explosion when the
        projectile collides with something.
        """
        if self.last_state is None or self.last_state.impact_type == ImpactType.BORDER:
            return

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

    def do_fall_terrain_and_tanks(self):
        """
        This method is responsible for making the terrain fall and the tanks fall
        when the projectile collides with something.
        """
        self.tanks_falling = True
        self.falling_speed = 0
        self.has_fallen = set()
        while self.terrain.is_falling or self.tanks_falling:
            check_running()
            dt = 1.0 / self.context.fps
            self.terrain.tick(dt * constants.TERRAIN_FALL_X_SPEED, self.gravity)
            self.make_tanks_fall(dt * constants.TERRAIN_FALL_X_SPEED)
            self.render()

    def wait_to_end_of_turn(self):
        """
        This method is responsible for waiting for the end of the turn.
        In the screen appears the stats of the shooting.
        If the player is a bot, it will wait for a while, otherwise it will wait
        for the player to press the space bar.
        """
        if not isinstance(self.get_current_tank(), Bot):
            self.wait_release_space()
            self.wait_on_space()
        else:
            self.sleep_rendering(constants.BOT_SLEEP_TIME)

    def play_turn(self):
        """
        This method is responsible for playing the turn of the player, it will
        call the functions that are responsible for the different parts of the
        turn.
        """
        self.update_wind()
        self.aim_and_shoot()
        self.cannonball_travel()
        self.do_explotion()
        self.do_radius_damage()
        self.terrain_destruction()
        self.do_fall_terrain_and_tanks()
        self.correct_tanks_position()
        self.wait_to_end_of_turn()
        self.check_last_state()
        self.wait_release_space()

    def try_to_find_winner(self):
        """
        This method is responsible for checking if there is a winner, if there
        is a winner, it will change the attributes of the class to adapt to the
        situation.
        """
        if self.tanks_alive != 1:
            return

        self.running = False
        for i, tank in enumerate(self.tanks):
            if tank.is_alive:
                self.winner = i

    def display_results(self):
        """
        This method does not show the results screen, but rather, based on the
        state changes, it is automatically shown when calling render. This
        function only waits for users to have read and want to continue,
        waiting for a click in the space.
        """
        if self.winner is not None:
            self.running = True
        while self.running:
            check_running()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                break
            self.render()

    def start(self) -> None:
        """
        This method is responsible for starting the game, it will call the
        functions that are responsible for the different parts of the game.
        """
        self.display_shop_menu()

        while self.running:
            check_running()

            if self.try_next_turn() is False:
                # No one can shoot
                return

            self.play_turn()
            self.try_to_find_winner()

            self.cannonball = None
            self.last_state = None

        self.display_results()
