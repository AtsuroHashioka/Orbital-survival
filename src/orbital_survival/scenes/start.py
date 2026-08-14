import pygame

from orbital_survival.config import GREEN, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from orbital_survival.scenes.base import Base_Manager
from orbital_survival.ui.start_button import Start_Button


class Start_Manager(Base_Manager):
    """
    Subclass that manages the start screen.
    """

    def __init__(self, screen, clock):
        """
        Initialize a StartManager object.

        :param screen: Screen object
        :param clock: Clock object
        """

        super().__init__(screen, clock)

        # Create space-key handler
        self.start_button = Start_Button()

        # Prepare fonts
        font_names = ["consolas", "dejavusansmono", "couriernew", "monospace"]
        self.title_font = pygame.font.SysFont(font_names, 74)
        self.prompt_font = pygame.font.SysFont(font_names, 36)

    def update(self):
        """
        Update the state of in-game objects.
        """
        pass

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
