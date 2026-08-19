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
from orbital_survival.scenes.base import GameMode, Scene, SceneRequest
from orbital_survival.scenes.game_over import GameOverScene
from orbital_survival.scenes.play import PlayScene
from orbital_survival.scenes.start import StartScene
from orbital_survival.ui.graph import GraphWindow

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

    def __init__(self, show_graph: bool = False) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ORBITAL SURVIVAL")

        # Opened once and reused by every round, so the graph does not blink
        # in and out of existence each time the player dies. None once the
        # player closes it, or when --graph was never passed.
        self.graph = GraphWindow() if show_graph else None

        self.is_running = True
        self.scene = self._create_scene(SceneRequest(GameMode.START))

        self.background_stars = self._create_stars(NUM_BACKGROUND_STARS)

    def _create_scene(self, request: SceneRequest) -> Scene:
        """Build the scene the request names, handing over its payload.

        Owning construction here is what lets scenes stay unaware of each
        other: they only name the mode they want to switch to.
        """
        match request.mode:
            case GameMode.START:
                return StartScene(self.screen)
            case GameMode.PLAY:
                return PlayScene(self.screen, self.graph)
            case GameMode.GAME_OVER:
                # Asking for the game-over screen without a tally to show
                # is a caller bug, so let it fail loudly rather than
                # inventing a score of zero.
                assert request.result is not None
                return GameOverScene(self.screen, request.result)

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
            if self._is_graph_close(event):
                self._close_graph()
                continue

            if event.type == pygame.QUIT:
                self.is_running = False

            request = self.scene.handle_event(event)
            if request is not None:
                self.scene = self._create_scene(request)

    def _is_graph_close(self, event: pygame.event.Event) -> bool:
        """Return whether this event is the graph window being closed.

        SDL reports the close of a secondary window as WINDOWCLOSE carrying
        the window it came from, and reserves QUIT for the display window --
        but only the `event.window` check keeps a stray QUIT from the graph
        window out of the branch below that ends the game.
        """
        if self.graph is None:
            return False
        return event.type == pygame.WINDOWCLOSE and self.graph.owns(
            getattr(event, "window", None)
        )

    def _close_graph(self) -> None:
        """Destroy the graph window and stop drawing to it."""
        if self.graph is not None:
            self.graph.close()
            self.graph = None

    def _update(self) -> None:
        """Advance the current scene one frame, honouring any switch."""
        request = self.scene.update()
        if request is not None:
            self.scene = self._create_scene(request)

    def _draw(self) -> None:
        """Repaint the frame: background, starfield, then the scene."""
        self.screen.fill(BLACK)

        for star in self.background_stars:
            pygame.draw.circle(self.screen, star.color, star.pos, star.radius)

        self.scene.draw()

        pygame.display.flip()

        # After the flip, so a slow repaint of the graph never delays the
        # frame the player is actually looking at.
        if self.graph is not None:
            self.graph.draw()

    def run(self) -> None:
        """Run the game loop until the window is closed."""
        while self.is_running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        self._close_graph()
        pygame.quit()
