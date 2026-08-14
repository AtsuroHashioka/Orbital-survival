"""Window setup, the main loop, and switching between scenes."""

import random
from typing import NamedTuple

import pygame

from orbital_survival.config import (
    BLACK,
    FPS,
    NUM_BACKGROUND_STARS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    Color,
    Position,
)
from orbital_survival.scenes.base import GameMode, Scene
from orbital_survival.scenes.play import PlayScene
from orbital_survival.scenes.start import StartScene

# Mostly 1px stars with the occasional 2px one, at a dim brightness range
# that keeps them from competing with the gameplay.
STAR_RADII = [1, 1, 1, 2]
STAR_BRIGHTNESS_RANGE = (50, 150)


class BackgroundStar(NamedTuple):
    """One static speck of the starfield behind the game."""

    pos: Position
    radius: int
    color: Color


class Game:
    """
    Main class that manages the entire game system.
    """

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ORBITAL SURVIVAL")

        self.is_running = True
        self.scene = self._create_scene(GameMode.START)

        self.background_stars = self._create_stars(NUM_BACKGROUND_STARS)

    def _create_scene(self, mode: GameMode) -> Scene:
        """Build the scene for the given mode.

        Owning construction here is what lets scenes stay unaware of each
        other: they only name the mode they want to switch to.
        """
        match mode:
            case GameMode.START:
                return StartScene(self.screen)
            case GameMode.PLAY:
                return PlayScene(self.screen)

    def _create_stars(self, num_stars: int) -> list[BackgroundStar]:
        """Scatter the starfield once at startup; it never moves afterwards."""
        stars = []
        for _ in range(num_stars):
            # Draw order matters: these share the global random stream with
            # the star's initial spin, so reordering them changes the game.
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.choice(STAR_RADII)
            brightness = random.randint(*STAR_BRIGHTNESS_RANGE)
            stars.append(
                BackgroundStar(
                    pos=(x, y),
                    radius=radius,
                    color=(brightness, brightness, brightness),
                )
            )
        return stars

    def _handle_events(self) -> None:
        """Drain the event queue, letting the scene request a mode switch."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            next_mode = self.scene.handle_event(event)
            if next_mode is not None:
                self.scene = self._create_scene(next_mode)

    def _update(self) -> None:
        """Advance the current scene one frame."""
        self.scene.update()

    def _draw(self) -> None:
        """Repaint the frame: background, starfield, then the scene."""
        self.screen.fill(BLACK)

        for star in self.background_stars:
            pygame.draw.circle(self.screen, star.color, star.pos, star.radius)

        self.scene.draw()

        pygame.display.flip()

    def run(self) -> None:
        """Run the game loop until the window is closed."""
        while self.is_running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()
