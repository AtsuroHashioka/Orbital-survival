import pygame
import random

from orbital_survival.config import (
    BLACK,
    FPS,
    NUM_BACKGROUND_STARS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from orbital_survival.scenes.base import GameMode
from orbital_survival.scenes.play import PlayScene
from orbital_survival.scenes.start import StartScene


class Game:
    """
    Main class that manages the entire game system.
    """

    def __init__(self):
        """
        Initialize the Game object.
        """
        # Initialize Pygame
        pygame.init()
        # Configure display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ORBITAL SURVIVAL")

        self.is_running = True  # Loop control for human play
        self.scene = self._create_scene(GameMode.START)

        # --- Create background stars ---
        self.background_stars = self._create_stars(NUM_BACKGROUND_STARS)

    def _create_scene(self, mode):
        """
        Build the scene for the given mode.

        Owning construction here is what lets scenes stay unaware of each
        other: they only name the mode they want to switch to.
        """
        match mode:
            case GameMode.START:
                return StartScene(self.screen)
            case GameMode.PLAY:
                return PlayScene(self.screen)

    # --- Create background stars ---
    def _create_stars(self, num_stars):
        """Create stars for the background."""
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            # Use many small stars and fewer large stars
            radius = random.choice([1, 1, 1, 2])
            # Randomize brightness
            brightness = random.randint(50, 150)
            color = (brightness, brightness, brightness)
            stars.append({"pos": (x, y), "radius": radius, "color": color})
        return stars

    # --- Event handling ---
    def _handle_events(self):
        """
        Handle keyboard and mouse events.
        """

        for event in pygame.event.get():
            # Exit loop when the window close button is pressed
            if event.type == pygame.QUIT:
                self.is_running = False

            next_mode = self.scene.handle_event(event)
            if next_mode is not None:
                self.scene = self._create_scene(next_mode)

    # --- Update game state ---
    def _update(self):
        """
        Update the state of in-game objects.
        """
        self.scene.update()

    # --- Rendering ---
    def _draw(self):
        """
        Draw objects on the screen.
        """
        self.screen.fill(BLACK)

        for star_data in self.background_stars:
            pygame.draw.circle(
                self.screen, star_data["color"], star_data["pos"], star_data["radius"]
            )

        self.scene.draw()

        pygame.display.flip()

    def run(self):
        """
        Main game loop.
        """

        # Game loop
        while self.is_running:
            # 1. Handle events
            self._handle_events()
            # 2. Update game state
            self._update()
            # 3. Run game-mode drawing
            self._draw()
            # 4. Control frame rate
            self.clock.tick(FPS)

        # Shutdown handling
        pygame.quit()
