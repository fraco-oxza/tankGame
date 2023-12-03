from enum import Enum


class AmbientEffect(Enum):
    """
    This class defines a numerator that represents different environmental effects.
    Each constant in the enumerator has a friendly name and an associated value, which indicates the type of environmental effect.
    """
    NONE = 0
    GRAVITY = 1
    WIND = 2
    GRAVITY_AND_WIND = 3
