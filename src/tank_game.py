import math
from random import randint
from typing import Optional

import pygame

import constants
from background import Background
from caches import audio_cache, font_cache, animation_cache
from cannonballs import Cannonball
from cannonballs import CannonballType
from context import Context
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
    players: list[players]

    def __init__(self, context: Context) -> None:
        """
        constructor that initializes each element within the game, in
        addition to starting the window itself of the game.
        """
        pass
