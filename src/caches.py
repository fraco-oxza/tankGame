from abc import abstractmethod
import os
import sys

import pygame


def resource_path(relative_path: str):
    """
    This function is responsible for loading resources from the resources folder.
    It is conditional since when the program is packaged in an executable, the
    folder directory changes, and other directories must be used. When the _MEIPASS
    environment variable is set, it means it is packaged.
    """
    path = getattr(
        sys, "_MEIPASS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
    )
    return os.path.join(path, "resources", relative_path)


class FileCache:
    """A base class for file caching."""

    @abstractmethod
    def __getitem__(self, filename: str):
        """Abstract method to get items from the cache."""
        raise NotImplementedError


class AnimationCache(FileCache):
    """A cache class for animations."""

    __animations: dict[str, list[pygame.surface.Surface]]

    def __init__(self):
        self.__animations = {}

    def __getitem__(self, animation_name: str) -> list[pygame.surface.Surface]:
        """Get the animation frames from the cache."""
        if animation_name in self.__animations:
            return self.__animations[animation_name]

        scale = (300, 200)  # TODO: Find the correct place for this scale

        animations_path = resource_path(os.path.join("animations", animation_name))
        animation = []

        # Find all images from the animation
        frames_quantity = len(os.listdir(animations_path))

        for frame_number in range(1, frames_quantity + 1):
            frame_path = resource_path(
                os.path.join(animations_path, f"{frame_number}.png")
            )
            animation.append(
                pygame.transform.scale(pygame.image.load(frame_path), scale)
            )

        self.__animations[animation_name] = animation

        return self.__animations[animation_name]


class ImageCache(FileCache):
    """A cache class for images."""

    __images: dict[str, pygame.surface.Surface]

    def __init__(self):
        self.__images = {}

    def __getitem__(self, filename: str) -> pygame.surface.Surface:
        """Get images from the cache."""
        if filename not in self.__images:
            self.__images[filename] = pygame.image.load(resource_path(filename))
        return self.__images[filename]


class FontCache(FileCache):
    """A cache class for fonts."""

    __fonts: dict[tuple[str, int], pygame.font.Font]

    def __init__(self):
        self.__fonts = {}

    def __getitem__(self, font_params: tuple[str, int]) -> pygame.font.Font:
        """Get fonts from the cache."""
        font_name, font_size = font_params

        if font_params not in self.__fonts:
            self.__fonts[font_params] = pygame.font.Font(
                resource_path(os.path.join("fonts", font_name)), font_size
            )

        return self.__fonts[font_params]


class AudioCache(FileCache):
    """A cache class for audio files."""

    __audios: dict[str, pygame.mixer.Sound]

    def __init__(self):
        self.__audios = {}

    def __getitem__(self, filename: str) -> pygame.mixer.Sound:
        """Get audio files from the cache."""
        if filename not in self.__audios:
            self.__audios[filename] = pygame.mixer.Sound(resource_path(filename))
        return self.__audios[filename]


image_cache = ImageCache()
font_cache = FontCache()
audio_cache = AudioCache()
animation_cache = AnimationCache()
