"""The scene abstraction and the modes the game can switch between."""

from abc import ABC, abstractmethod
from enum import StrEnum

import pygame


class GameMode(StrEnum):
    """The scenes the game can switch between."""

    START = "start"
    PLAY = "play"


class Scene(ABC):
    """
    Base class for game scenes.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> GameMode | None:
        """Handle one event, returning the mode to switch to, or None to stay.

        Scenes name a mode rather than returning the next scene so that they
        never import one another — which is what would turn a future
        play -> start transition into a circular import.
        """

    @abstractmethod
    def update(self) -> None:
        """Advance the scene one frame."""

    @abstractmethod
    def draw(self) -> None:
        """Draw the scene onto its screen."""
