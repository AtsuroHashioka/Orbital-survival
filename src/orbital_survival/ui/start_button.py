import pygame


class Start_Button:
    """
    Class that detects space-key input.
    """

    def __init__(self):
        pass  # No specific initialization needed

    def is_pressed(self, event):
        """
        Process keyboard events and return True when SPACE is pressed.
        :param event: Pygame event object
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
        return False
