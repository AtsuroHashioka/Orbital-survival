"""The scene abstraction and the modes the game can switch between."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum

import pygame


class GameMode(StrEnum):
    """The scenes the game can switch between."""

    START = "start"
    PLAY = "play"
    GAME_OVER = "game_over"


@dataclass(frozen=True, slots=True)
class GameResult:
    """The outcome of one finished round, shown on the game-over screen."""

    score: int
    elapsed_ms: int


@dataclass(frozen=True, slots=True)
class SceneRequest:
    """A scene's request to switch, carrying whatever the next scene needs.

    The payload rides along with the mode because the scene that has the
    numbers — the one that just ended — is thrown away the moment the switch
    happens. Handing them to `Game` keeps scenes from having to know one
    another.
    """

    mode: GameMode
    result: GameResult | None = None


class Scene(ABC):
    """
    Base class for game scenes.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> SceneRequest | None:
        """Handle one event, returning a switch request, or None to stay.

        Scenes name a mode rather than returning the next scene so that they
        never import one another — which is what would turn the
        play -> game over -> start cycle into a circular import.
        """

    @abstractmethod
    def update(self) -> SceneRequest | None:
        """Advance the scene one frame, optionally requesting a switch.

        Play requests the game-over screen from here rather than from
        `handle_event`: running out of lives follows from the simulation, not
        from anything the player pressed.
        """

    @abstractmethod
    def draw(self) -> None:
        """Draw the scene onto its screen."""
