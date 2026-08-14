from abc import ABC, abstractmethod
from enum import StrEnum


class GameMode(StrEnum):
    """The scenes the game can switch between."""

    START = "start"
    PLAY = "play"


class Scene(ABC):
    """
    Base class for game scenes.
    """

    def __init__(self, screen):
        """
        Initialize a Scene object.

        :param screen: Screen object
        """
        self.screen = screen

    @abstractmethod
    def handle_event(self, event):
        """
        Handle a single event, returning the mode to switch to or None.

        Scenes return a GameMode rather than the next scene itself so that
        they never have to import one another, which would turn a future
        play -> start transition into a circular import.
        """

    @abstractmethod
    def update(self):
        """
        Update the state of in-game objects.
        """

    @abstractmethod
    def draw(self):
        """
        Draw objects on the screen.
        """
