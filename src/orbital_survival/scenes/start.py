import pygame

from orbital_survival.config import FONT_NAMES, GREEN, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from orbital_survival.scenes.base import GameMode, Scene


def is_start_pressed(event):
    """Return True when the event is a SPACE key press."""
    return event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE


class StartScene(Scene):
    """
    Subclass that manages the start screen.
    """

    def __init__(self, screen):
        """
        Initialize a StartScene object.

        :param screen: Screen object
        """

        super().__init__(screen)

        # Prepare fonts
        self.title_font = pygame.font.SysFont(FONT_NAMES, 74)
        self.prompt_font = pygame.font.SysFont(FONT_NAMES, 36)

    def handle_event(self, event):
        """
        Switch to PLAY when SPACE is pressed.
        """
        return GameMode.PLAY if is_start_pressed(event) else None

    def update(self):
        """
        Update the state of in-game objects.
        """

    def draw(self):
        """
        Draw objects on the screen.
        """

        # Show game title in the center of the screen
        title_text = self.title_font.render("ORBITAL SURVIVAL", True, WHITE)
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
        )
        self.screen.blit(title_text, title_rect)

        # Show "Press SPACE" under the title
        prompt_text = self.prompt_font.render("PRESS SPACE TO PLAY", True, GREEN)
        prompt_rect = prompt_text.get_rect(
            center=(SCREEN_WIDTH / 2, title_rect.bottom + 30)
        )
        self.screen.blit(prompt_text, prompt_rect)
