from abc import abstractmethod

from pygame import Vector2


class Collidable:
    """
    Class containing an abstract method that is passed via Override to
    other classes, where collisions are expected.
    """

    @abstractmethod
    def collides_with(self, point: Vector2) -> bool:
        """
        This method is responsible for saying if self, that is, the instance
        collidable has already collided with a point. Should return True in case of
        that collides and False otherwise.
        """
        raise NotImplementedError
