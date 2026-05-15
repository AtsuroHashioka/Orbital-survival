# game.py

import pygame
import sys
import random

from config import BLACK, FPS, NUM_BACKGROUND_STARS, SCREEN_HEIGHT, SCREEN_WIDTH
from system.play.play_manager import Play_Manager
from system.start.start_manager import Start_Manager


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
        self.game_mode = "start"  # Initial game mode
        self.manager = Start_Manager(self.screen, self.clock)  # Game mode manager

        # --- Create background stars ---
        self.background_stars = self._create_stars(NUM_BACKGROUND_STARS)

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

            # Handle events by game mode
            if self.game_mode == "start":
                if self.manager.start_button.is_pressed(event):
                    self.game_mode = "play"
                    self.manager = Play_Manager(
                        self.screen, self.clock
                    )  # Create a Play_Manager instance
            # Temporary handling
            # elif self.game_mode == 'play':
            #     if self.manager.start_button.is_pressed(event):
            #         self.game_mode = 'start'
            #         self.manager = Start_Manager(self.screen, self.clock)  # Create a Start_Manager instance
            # else:
            #     pass # Temporary handling

    # --- Update game state ---
    def _update(self):
        """
        Update the state of in-game objects.
        """
        self.manager.update()

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

        self.manager.draw()

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
        sys.exit()
