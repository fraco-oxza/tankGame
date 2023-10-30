import pygame

from exit_requested import ExitRequested


def check_running():
    """
    This method checks if the player has sent the signal to close the
    window and stops the execution if this is the case, it is also
    responsible for cleaning any position that has been left unused.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise ExitRequested
