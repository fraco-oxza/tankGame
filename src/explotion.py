import pygame

from draw import Drawable


class Explosion(Drawable):
    """This class represents an explosion animation."""

    t_animation: float
    position: pygame.Vector2
    images: list[pygame.surface.Surface]

    def tick(self, dt: float):
        """Updates the animation frame based on the elapsed time."""
        self.current_index = int(
            (self.elapsed_time / self.t_animation) * len(self.images)
        )
        self.elapsed_time += dt

    def has_next(self) -> bool:
        """Checks if there are more frames in the animation."""
        return self.elapsed_time < self.t_animation

    def __init__(self, position: pygame.Vector2, images: list[pygame.surface.Surface]):
        """
        Initializes the Explosion object with the given position and animation frames.
        """
        self.elapsed_time = 0.0
        self.t_animation = 0.5
        self.images = images
        self.position = position
        self.current_index = 0

    def draw(self, screen: pygame.surface.Surface) -> None:
        """Draws the current frame of the explosion animation on the screen."""
        pos_x = self.position[0] - self.images[self.current_index].get_size()[0] // 2
        pos_y = self.position[1] - self.images[self.current_index].get_size()[1] // 2
        screen.blit(self.images[self.current_index], (pos_x, pos_y))
