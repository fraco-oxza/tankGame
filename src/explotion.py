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
        if self.current_index >= len(self.images):
            self.current_index = 0
            self.elapsed_time = 0.0
        self.elapsed_time += dt

    def has_next(self) -> bool:
        """Checks if there are more frames in the animation."""
        return self.elapsed_time < self.t_animation or self.loop

    def __init__(
        self,
        position: pygame.Vector2,
        images: list[pygame.surface.Surface],
        size=None,
        loop=False,
    ):
        """
        Initializes the Explosion object with the given position and animation frames.
        """
        self.elapsed_time = 0.0
        self.t_animation = 0.5
        self.images = images
        if size is not None:
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.scale(self.images[i], size)
        self.position = position
        self.current_index = 0
        self.loop = loop

    def draw(self, screen: pygame.surface.Surface) -> None:
        """Draws the current frame of the explosion animation on the screen."""
        pos_x = self.position[0] - self.images[self.current_index].get_size()[0] // 2
        pos_y = self.position[1] - self.images[self.current_index].get_size()[1] // 2
        screen.blit(self.images[self.current_index], (pos_x, pos_y))
