"""The circular left/right arrow buttons shown during play."""

import math
from typing import Literal

import pygame

from orbital_survival.config import BLACK, Color, Position, WHITE

type Direction = Literal["left", "right"]

BORDER_WIDTH = 2
ARROW_SCALE = 0.4  # Arrow half-size as a fraction of the button radius


class PlayButton:
    """
    Class representing circular arrow buttons on the play screen.
    """

    def __init__(
        self,
        center_x: float,
        center_y: float,
        radius: int,
        direction: Direction,
    ) -> None:
        self.center = (center_x, center_y)
        self.radius = radius
        self.direction = direction

        # Pre-rendered rather than redrawn every frame. Two states: normal
        # (black on white outline) and active (inverted).
        self.image_normal = self._create_surface(icon_color=WHITE, bg_color=BLACK)
        self.image_active = self._create_surface(icon_color=BLACK, bg_color=WHITE)
        self.rect = self.image_normal.get_rect(center=self.center)

    def _create_surface(self, icon_color: Color, bg_color: Color) -> pygame.Surface:
        """Render one button state onto a transparent surface."""
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        pygame.draw.circle(surface, bg_color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(
            surface, WHITE, (self.radius, self.radius), self.radius, BORDER_WIDTH
        )

        # Arrow vertices, relative to the button's own center.
        arrow_size = self.radius * ARROW_SCALE
        if self.direction == "left":
            tip = (self.radius - arrow_size, self.radius)
            back_x = self.radius + arrow_size
        else:
            tip = (self.radius + arrow_size, self.radius)
            back_x = self.radius - arrow_size

        pygame.draw.polygon(
            surface,
            icon_color,
            [
                tip,
                (back_x, self.radius - arrow_size),
                (back_x, self.radius + arrow_size),
            ],
        )

        return surface

    def draw(self, screen: pygame.Surface, is_active: bool = False) -> None:
        """Blit the pressed or unpressed image depending on `is_active`."""
        image = self.image_active if is_active else self.image_normal
        screen.blit(image, self.rect)

    def is_clicked(self, pos: Position) -> bool:
        """Return whether a point falls inside the button's circle.

        The circle is tested directly rather than via self.rect, which is the
        square bounding box and would accept the corners.
        """
        return (
            math.hypot(pos[0] - self.center[0], pos[1] - self.center[1]) <= self.radius
        )
