import pygame
from context import instance
from caches import font_cache


class Button:
    """
    class responsible for identifying which button is being clicked with the mouse
    """
    def __init__(self, screen: pygame.Surface, secondary, principal):
        self.secondary_buttons = secondary
        self.principal_button_size = principal
        self.screen = screen

    def handle_input_inside(self, mouse: pygame.Vector2, button):
        """
        Through the position of the mouse,
        the position of the buttons and their size, you can identify if the mouse is over a button
        """
        if button[0] < mouse.x < (
                button[0] + self.secondary_buttons[0]
        ) and button[1] < mouse.y < (
                button[1] + self.secondary_buttons[1]
        ):
            return True

    def handle_input(self, mouse: pygame.Vector2):
        """
        This function returns the button that is being pressed through a number,
        which is returned to the option_menu class
        """
        sobre = 0
        button_left_1 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 5.53,
        )
        if self.handle_input_inside(mouse, button_left_1):
            sobre = 1
        button_left_2 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 3.2,
        )
        if self.handle_input_inside(mouse, button_left_2):
            sobre = 2
        button_left_3 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 2.28,
        )
        if self.handle_input_inside(mouse, button_left_3):
            sobre = 3
        button_left_4 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 1.77,
        )
        if self.handle_input_inside(mouse, button_left_4):
            sobre = 4
        button_left_5 = (
            instance.windows_size[0] / 3.45,
            instance.windows_size[1] / 1.45,
        )
        if self.handle_input_inside(mouse, button_left_5):
            sobre = 5
        button_left_6 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 5.53,
        )
        if self.handle_input_inside(mouse, button_left_6):
            sobre = 6
        button_left_7 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 3.2,
        )
        if self.handle_input_inside(mouse, button_left_7):
            sobre = 7
        button_left_8 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 2.28,
        )
        if self.handle_input_inside(mouse, button_left_8):
            sobre = 8
        button_left_9 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 1.77,
        )
        if self.handle_input_inside(mouse, button_left_9):
            sobre = 9
        button_left_10 = (
            instance.windows_size[0] / 1.52,
            instance.windows_size[1] / 1.45,
        )
        if self.handle_input_inside(mouse, button_left_10):
            sobre = 10
        button_left_11 = (
            instance.windows_size[0] / 1.25,
            instance.windows_size[1] / 2.21,
        )
        if button_left_11[0] < mouse.x < (
                button_left_11[0] + self.principal_button_size[0]
        ) and button_left_11[1] < mouse.y < (
                button_left_11[1] + self.principal_button_size[1]
        ):
            sobre = 11

        return sobre
