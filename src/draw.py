from abc import abstractmethod

import pygame


class Drawable:
    """
    Class containing an abstract method that is passed via Override to
    other classes, where visual elements will be created that will be shown by
    middle of the interface.
    """

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        """
         This function is responsible for drawing an instance, through the screen
         What is passed in the parameters. You should not do the
         pygame.display.flip
         """
        raise NotImplementedError
