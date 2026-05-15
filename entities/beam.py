# entities/beam.py

from .base import BaseArc
from config import (
    BEAM_MAX_RADIUS,
    BEAM_SPEED,
    FPS,
    PLANET_ORBIT_RADIUS,
    RED,
    WHITE,
)


class Beam(BaseArc):
    """
    Class representing a beam emitted from the star.
    """

    # -- Class constants ---
    SPEED = BEAM_SPEED
    MAX_RADIUS = BEAM_MAX_RADIUS

    def __init__(self, center_pos, angle, arc_range, radius, width):
        """
        Initialize a beam object.

        :param center_pos: Beam center position (x, y)
        :param angle: Beam center angle
        :param arc_range: Beam angle range
        :param radius: Initial beam radius (from star surface)
        :param width: Beam line width
        """

        super().__init__(
            center_pos=center_pos,
            angle=angle,
            arc_range=arc_range,
            radius=radius,  # Initial radius at emission (from star surface)
            width=width,
            color=WHITE,
        )
        self.dodged = False  # Flag to track whether this beam was dodged

    def update(self):
        """
        Update beam state.
        """
        self.radius += self.SPEED  # Increase radius at beam expansion speed

    def is_alive(self):
        """
        Determine whether the beam is still active.
        """
        return self.radius < self.MAX_RADIUS  # Check if max radius is not reached

    def draw(self, screen):
        """
        Draw the beam on the screen.
        :param screen: Target Pygame screen object
        """

        # Fade out once radius exceeds the planet orbit radius (225)
        fade_distance = self.MAX_RADIUS - PLANET_ORBIT_RADIUS

        # Compute fade progress (0.0: start, 1.0: complete)
        fade_progress = (
            max(0, (self.radius - PLANET_ORBIT_RADIUS)) / fade_distance
            if fade_distance > 0
            else 1.0
        )
        life_ratio = 1.0 - min(fade_progress, 1.0)

        current_color = tuple(int(c * life_ratio) for c in self.color)
        draw_width = min(self.width, int(self.radius))

        self.draw_arc(screen, current_color, draw_width)


class BeamCorpse(BaseArc):
    """
    Class representing a beam "corpse" shown after collision.
    """

    DURATION = FPS // 4  # Display duration (0.25 seconds)

    def __init__(self, center_pos, angle, arc_range, radius, width):
        """
        Initialize a destroyed beam object.

        :param center_pos: Beam center position (x, y)
        :param angle: Beam center angle
        :param arc_range: Beam angle range
        :param radius: Beam radius at collision time
        :param width: Beam line width
        """
        super().__init__(
            center_pos=center_pos,
            angle=angle,
            arc_range=arc_range,
            radius=radius,
            width=width,
            color=RED,
        )
        self.life = self.DURATION  # Remaining display time

    def update(self):
        """
        Update corpse state (fade-out).
        """
        self.life -= 1

    def is_alive(self):
        """
        Determine whether the corpse should still be displayed.
        """
        return self.life > 0

    def draw(self, screen):
        """
        Draw the corpse (fade-out).
        :param screen: Target Pygame screen object
        """
        if self.is_alive():
            life_ratio = self.life / self.DURATION
            current_color = tuple(int(c * life_ratio) for c in self.color)
            self.draw_arc(screen, current_color, self.width)
