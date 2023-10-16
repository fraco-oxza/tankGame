from abc import abstractmethod

from pygame import Vector2


class Collidable:
    """
    Clase que contiene un método abstracto que se pasa a través de Override a
    otras clases, donde se espera haya colisiones.
    """

    @abstractmethod
    def collides_with(self, point: Vector2) -> bool:
        """
        Esta funcion es la encargada de decir si self, es decir la instancia
        colisionable ya colisionó con un punto. Debe retornar True en caso de
        que colisione y False en otro caso.
        """
        raise NotImplementedError
