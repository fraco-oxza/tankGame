from abc import abstractmethod

from pygame import Vector2


class Collidable:
    """
    Class containing an abstract method that is passed via Override to
    other classes, where collisions are expected.
    """

    @abstractmethod
    def collides_with(self, point: Vector2, validation_distance: float = 0) -> bool:
        """
        This method is responsible for saying if self, that is, the instance
        collidable has already collided with a point. Should return True in case of
        that collides and False otherwise.
        The validation distance variable is used to express how close the body
        has to be to be considered a coalition, for example, if it is 0, then
        they have to be inside the body, but if it is 10, it will be activated
        10 meters before collide.
        """
        raise NotImplementedError
