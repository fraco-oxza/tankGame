import pygame

from draw import Drawable


class Explosion(Drawable):
    t_animacion: float
    position: pygame.Vector2
    image: list[pygame.surface.Surface]

    def tick(self, dt: float):
        self.indice_actual = int((self.t_mostrado / self.t_animacion) * len(self.image))
        self.t_mostrado += dt

    def has_next(self):
        return self.t_mostrado < self.t_animacion

    def __init__(
        self, position: pygame.Vector2, imagenes: list[pygame.surface.Surface]
    ):
        self.t_mostrado = 0.0
        self.t_animacion = 0.5
        self.image = imagenes
        self.position = position
        self.indice_actual = 0
        self.center = pygame.rect.Rect

    def draw(self, screen: pygame.surface.Surface) -> None:
        pos_x = self.position[0] - self.image[self.indice_actual].get_size()[0] // 2
        pos_y = self.position[1] - self.image[self.indice_actual].get_size()[1] // 2
        screen.blit(self.image[self.indice_actual], (pos_x, pos_y))
