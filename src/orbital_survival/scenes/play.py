import pygame

from orbital_survival.config import BUTTON_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from orbital_survival.logic import Logic
from orbital_survival.scenes.base import Scene
from orbital_survival.ui.play_button import PlayButton
from orbital_survival.ui.hud import HUD


class PlayScene(Scene):
    """
    Subclass that manages PLAY mode.
    """

    def __init__(self, screen):
        """
        Initialize a PlayScene object.

        :param screen: Pygame screen object
        """

        super().__init__(screen)

        # Initialize game state
        self._initialize_state()

    def handle_event(self, event):
        """
        Play mode never switches away on its own.
        """
        return None

    def _initialize_state(self):
        """Initialize game state."""
        self.start_time = pygame.time.get_ticks()  # Initialize elapsed-time reference

        # --- Create objects ---
        # Create logic object
        self.logic = Logic()

        # Place circular buttons at lower left/right center
        self.left_button = PlayButton(
            SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 80, BUTTON_RADIUS, "left"
        )
        self.right_button = PlayButton(
            SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT - 80, BUTTON_RADIUS, "right"
        )
        # Create HUD object
        self.hud = HUD()

    def update(self):
        """
        Update the state of in-game objects.
        """
        # --- Planet control (supports keyboard and mouse) ---
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Left acceleration check (left key or left button click)
        self.logic.left_active = keys[pygame.K_LEFT] or (
            mouse_buttons[0] and self.left_button.is_clicked(mouse_pos)
        )
        # Right acceleration check (right key or right button click)
        self.logic.right_active = keys[pygame.K_RIGHT] or (
            mouse_buttons[0] and self.right_button.is_clicked(mouse_pos)
        )

        # Update logic object state
        self.logic.update()

    def draw(self):
        """
        Draw objects on the screen.
        """

        for corpse in self.logic.corpses:
            corpse.draw(self.screen)

        self.logic.star.draw(self.screen)
        self.logic.planet.draw(self.screen)

        self.left_button.draw(self.screen, self.logic.left_active)
        self.right_button.draw(self.screen, self.logic.right_active)
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.hud.draw(
            self.screen,
            self.logic.planet.speed,
            self.logic.planet.actual_acceleration,
            self.logic.kill_count,
            self.logic.score,
            elapsed_time,
        )
