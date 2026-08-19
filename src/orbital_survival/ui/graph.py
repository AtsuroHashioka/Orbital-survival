"""A separate window plotting speed, acceleration and input over time.

Opened only with `--graph`. The window is a second SDL window rather than a
panel inside the game, so the plot can be as wide as it needs to be without
stealing room from the playfield.

The plot is composed on an ordinary `pygame.Surface` with the same drawing
calls as the rest of the UI, then uploaded as a texture — `pygame.Window` has
no surface of its own to draw into, so a renderer is the only way onto a
second window.
"""

from collections import deque
from dataclasses import dataclass
from typing import NamedTuple

import pygame
from pygame._sdl2.video import Renderer, Texture, Window

from orbital_survival.config import (
    ACCELERATION,
    BLACK,
    DISPLAY_SCALE,
    EARTH_BLUE,
    FONT_NAMES,
    FRICTION,
    GRAPH_DRAW_INTERVAL,
    GRAPH_HEIGHT,
    GRAPH_HISTORY_FRAMES,
    GRAPH_WIDTH,
    GRAY,
    GREEN,
    SUN_ORANGE,
    Color,
)
from orbital_survival.entities.base import CelestialBody

MARGIN = 10
LABEL_FONT_SIZE = 18
# Each pane gives up this much of its top to its label. Drawing the label
# inside the plot instead would put it exactly where the traces spend their
# time: a series at its positive bound sits on the pane's top edge.
LABEL_HEIGHT = LABEL_FONT_SIZE + 2

# One frame changes the speed by `a * direction * friction - speed * (1 -
# friction)`. Both terms peak at ACCELERATION * FRICTION -- the second because
# MAX_SPEED is itself ACCELERATION * FRICTION / (1 - FRICTION) -- so the
# largest step is twice that, reached when the player reverses at full speed.
MAX_ACCELERATION = 2 * ACCELERATION * FRICTION


class Sample(NamedTuple):
    """One frame of the planet's motion, as the graph plots it."""

    speed: float
    acceleration: float
    direction: int


@dataclass(frozen=True, slots=True)
class Pane:
    """One of the stacked plots: how to label, scale and color a series."""

    label: str
    color: Color
    # Raw value -> displayed value, so the numbers match the HUD's.
    scale: float
    # Displayed value at the top edge of the pane; the bottom is its negative.
    value_range: float
    value_format: str


# Fixed rather than auto-scaled: every bound below follows from the tuning
# constants, so the axes track a change to ACCELERATION or FRICTION on their
# own, and a stationary baseline keeps "how fast is fast" readable at a glance.
PANES = (
    Pane(
        label="SPEED",
        color=GREEN,
        scale=DISPLAY_SCALE,
        value_range=CelestialBody.MAX_SPEED * DISPLAY_SCALE,
        value_format="+08.4f",
    ),
    Pane(
        label="ACCEL",
        color=SUN_ORANGE,
        scale=DISPLAY_SCALE,
        value_range=MAX_ACCELERATION * DISPLAY_SCALE,
        value_format="+08.4f",
    ),
    Pane(
        label="INPUT",
        color=EARTH_BLUE,
        scale=1,
        value_range=1,
        value_format="+.0f",
    ),
)


class GraphRecorder:
    """The rolling history of one round, oldest sample first.

    Owned by the play scene, so a new round starts from an empty history
    without anyone having to remember to clear it.
    """

    def __init__(self, history_frames: int = GRAPH_HISTORY_FRAMES) -> None:
        self.samples: deque[Sample] = deque(maxlen=history_frames)

    def record(self, speed: float, acceleration: float, direction: int) -> None:
        """Append one frame, dropping the oldest once the window is full."""
        self.samples.append(Sample(speed, acceleration, direction))

    def series(self) -> tuple[list[float], ...]:
        """Return the three series in `PANES` order, ready to plot."""
        return (
            [sample.speed for sample in self.samples],
            [sample.acceleration for sample in self.samples],
            [float(sample.direction) for sample in self.samples],
        )


class GraphWindow:
    """The second window, and the plot drawn into it.

    It holds the recorder rather than the scene that owns it, so that a round
    ending does not blank the graph: the last round's recorder stays attached
    until the next one replaces it.
    """

    def __init__(self) -> None:
        self.window = Window(
            "ORBITAL SURVIVAL - TELEMETRY", size=(GRAPH_WIDTH, GRAPH_HEIGHT)
        )
        self.renderer = Renderer(self.window)
        self.surface = pygame.Surface((GRAPH_WIDTH, GRAPH_HEIGHT))
        self.font = pygame.font.SysFont(FONT_NAMES, LABEL_FONT_SIZE)

        self.recorder: GraphRecorder | None = None
        # Counts up to GRAPH_DRAW_INTERVAL, so the first frame paints at once
        # instead of leaving the window blank until the interval elapses.
        self.frames_since_draw = GRAPH_DRAW_INTERVAL

    def attach(self, recorder: GraphRecorder) -> None:
        """Plot this recorder from now on."""
        self.recorder = recorder

    def owns(self, window: Window | None) -> bool:
        """Return whether a window event came from this window."""
        return window is self.window

    def close(self) -> None:
        """Destroy the window; the caller must stop calling `draw` afterwards."""
        self.window.destroy()

    def draw(self) -> None:
        """Repaint, but only once every GRAPH_DRAW_INTERVAL frames."""
        self.frames_since_draw += 1
        if self.frames_since_draw < GRAPH_DRAW_INTERVAL:
            return
        self.frames_since_draw = 0

        self._compose()

        texture = Texture.from_surface(self.renderer, self.surface)
        self.renderer.clear()
        texture.draw()
        self.renderer.present()

    def _compose(self) -> None:
        """Draw every pane onto the offscreen surface."""
        self.surface.fill(BLACK)

        series = self.recorder.series() if self.recorder else ((), (), ())
        for index, (pane, values) in enumerate(zip(PANES, series, strict=True)):
            self._draw_pane(pane, list(values), self._pane_rect(index))

    def _pane_rect(self, index: int) -> pygame.Rect:
        """Return the plot area of the index-th pane, counting from the top.

        The rect excludes the label row, which sits immediately above it.
        """
        # One margin above each pane plus one below the last.
        height = (GRAPH_HEIGHT - MARGIN * (len(PANES) + 1)) // len(PANES)
        return pygame.Rect(
            MARGIN,
            MARGIN + index * (height + MARGIN) + LABEL_HEIGHT,
            GRAPH_WIDTH - 2 * MARGIN,
            height - LABEL_HEIGHT,
        )

    def _draw_pane(self, pane: Pane, values: list[float], rect: pygame.Rect) -> None:
        """Draw one pane: its zero line, its trace, then its label."""
        pygame.draw.line(
            self.surface, GRAY, (rect.left, rect.centery), (rect.right, rect.centery)
        )

        # A single sample has no line to draw, and dividing by `count - 1`
        # below would fail on it.
        if len(values) > 1:
            points = [
                (self._x(index, len(values), rect), self._y(value, pane, rect))
                for index, value in enumerate(values)
            ]
            pygame.draw.lines(self.surface, pane.color, False, points)

        latest = values[-1] if values else 0.0
        label = f"{pane.label}:{latest * pane.scale:{pane.value_format}}"
        self.surface.blit(
            self.font.render(label, True, pane.color),
            (rect.left, rect.top - LABEL_HEIGHT),
        )

    def _x(self, index: int, count: int, rect: pygame.Rect) -> float:
        """Map a sample's position in the history onto the pane's width.

        The whole history is stretched across the pane, so changing
        GRAPH_HISTORY_FRAMES rescales time rather than resizing the window.
        """
        return rect.left + index * (rect.width - 1) / (count - 1)

    def _y(self, value: float, pane: Pane, rect: pygame.Rect) -> float:
        """Map a value onto the pane's height, clamped to its bounds.

        Clamping matters because MAX_SPEED is only approached asymptotically
        from below but ACCEL can sit exactly on its bound, and a rounding
        error there would draw a pixel outside the pane.
        """
        offset = value * pane.scale / pane.value_range * (rect.height / 2)
        return rect.centery - max(-rect.height / 2, min(rect.height / 2, offset))
