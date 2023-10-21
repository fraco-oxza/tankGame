import pygame

from caches import image_cache
import constants
from tank_game import TankGame


def main():
    """
    From this function the program is started, creating the only instance of
    TankGame that exists...
    """
    pygame.init()

    pygame.display.set_caption("TankGame!")
    icon = image_cache["images/tankIcon.png"]
    pygame.display.set_icon(icon)
    tank_game = TankGame(pygame.display.set_mode(constants.WINDOWS_SIZE))
    tank_game.start()


if __name__ == "__main__":
    main()
