import pygame

from caches import image_cache
from exit_requested import ExitRequested
import context
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

    tank_game = TankGame(context.instance)
    try:
        tank_game.start()
    except ExitRequested:
        pass


if __name__ == "__main__":
    main()
