import pygame

import constants
from caches import image_cache
from draw import Drawable


class Background(Drawable):
    """
    This class represents the game background, which loads an image and creates
    animations of falling snow with wind.
    """

    sky_image: pygame.Surface

    def __init__(self, image: str):
        """Initialize the class by loading the images and creating the snowflakes."""
        self.image = image
        image_size = pygame.Vector2(
            constants.WINDOWS_SIZE[0],
            (1.0 / constants.ASPECT_RATIO) * constants.WINDOWS_SIZE[0],
        )
        self.sky_image = pygame.transform.scale(image_cache[self.image], image_size)
        self.sky_rect = self.sky_image.get_rect()

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        This function is responsible for drawing the background and the
        snowflakes.
        """
        screen.blit(self.sky_image, self.sky_rect.topleft)
