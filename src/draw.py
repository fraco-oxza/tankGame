from abc import abstractmethod

import pygame


class Drawable:
    """
    Clase que contiene un método abstracto que se pasa a través de Override a
    otras clases, donde se crearán elementos visuales que serán mostrados por
    medio de la interfaz.
    """

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Esta funcion se encarga de dibujar una instancia, a traves de la screen
        que se le pasa en los parametros. No se debe hacer el
        pygame.display.flip
        """
        raise NotImplementedError
