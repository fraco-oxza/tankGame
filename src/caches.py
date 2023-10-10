import os
import sys
from abc import abstractmethod

import pygame


def resource_path(relative_path: str):
    """
    This function is responsible for loading the resources from the resources
    folder. It is conditional, since when the program is packaged in an
    executable, the folder directory changes and other directories must be
    used. When the _MEIPASS environment variable is set, it means it is
    packaged.
    """
    path = getattr(
        sys, "_MEIPASS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
    )
    return os.path.join(path, "resources", relative_path)


class FileCache:
    @abstractmethod
    def __getitem__(self, filename: str):
        raise NotImplementedError


class ImageCache(FileCache):
    __images: dict[str, pygame.surface.Surface]

    def __init__(self):
        self.__images = {}

    def __getitem__(self, filename: str) -> pygame.surface.Surface:
        if filename not in self.__images:
            self.__images[filename] = pygame.image.load(resource_path(filename))
        return self.__images[filename]


class FontCache(FileCache):
    __fonts: dict[tuple[str, int], pygame.font.Font]

    def __init__(self):
        self.__fonts = {}

    def __getitem__(self, font_params: tuple[str, int]) -> pygame.font.Font:
        font_name, font_size = font_params

        if font_params not in self.__fonts:
            self.__fonts[font_params] = pygame.font.Font(
                resource_path(os.path.join("fonts", font_name)), font_size
            )

        return self.__fonts[font_params]


class AudioCache(FileCache):
    pass


image_cache = ImageCache()
font_cache = FontCache()
