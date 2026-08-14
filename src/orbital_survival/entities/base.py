import math
import pygame

from orbital_survival.config import ACCELERATION as CFG_ACCELERATION, FRICTION as CFG_FRICTION

# --- Base classes ---


class CelestialBody:
    """Base class for rotating celestial bodies such as planets and stars."""

    # --- Class constants ---
    ACCELERATION = float(CFG_ACCELERATION)
    FRICTION = float(CFG_FRICTION)
    MAX_SPEED = ACCELERATION * FRICTION / (1 - FRICTION)

    def __init__(self, center_pos, size, acceleration, friction, angle, speed):
        """
        Initialize a celestial body.

        :param center_pos: Center position of the body (x, y)
        :param size: Body size
        :param acceleration: Angular acceleration
        :param friction: Deceleration ratio
        :param angle: Angular position
        :param speed: Angular speed
        """
        self.center_pos = center_pos  # Center position of the body (x, y)
        self.size = size  # Body size
        self.angle = angle % (2 * math.pi)  # Angular position
        self.speed = speed  # Angular speed
        self.acceleration = acceleration  # Angular acceleration
        self.friction = friction  # Deceleration ratio

    def update_angle_and_speed(self, direction):
        """
        Apply acceleration and friction to update speed and angle.
        param direction: Acceleration direction (1: positive, -1: negative)
        """
        self.speed += self.acceleration * direction  # Update speed from acceleration
        self.speed *= self.friction  # Apply deceleration
        self.angle += self.speed  # Update angle from speed
        self.angle %= 2 * math.pi  # Keep angle in the range [0, 2π)


class BaseArc:
    """Base class for arc-drawing objects (beams and beam corpses)."""

    def __init__(self, center_pos, angle, arc_range, radius, width, color):
        """
        Initialize an arc object.

        :param center_pos: Arc center position (x, y)
        :param angle: Arc center angle
        :param arc_range: Arc angle range
        :param radius: Arc radius
        :param width: Arc line width
        :param color: Arc color
        """
        self.center_pos = center_pos  # Arc center position (x, y)
        self.angle = angle % (2 * math.pi)  # Arc center angle
        self.arc_range = arc_range  # Arc angle range
        self.radius = radius  # Arc radius
        self.width = width  # Arc line width
        self.color = color  # Arc color

    def update(self):
        """Update state. Implemented in subclasses."""
        raise NotImplementedError

    def is_alive(self):
        """Return whether object is alive. Implemented in subclasses."""
        raise NotImplementedError

    def draw_arc(self, screen, color, draw_width):
        """
        Draw an arc with the specified color and line width.
        :param screen: Target screen
        :param color: Color to draw
        :param draw_width: Line width to draw
        """
        if draw_width > 0:
            # Compute start and end angles of the arc
            start_angle = self.angle - self.arc_range / 2
            end_angle = self.angle + self.arc_range / 2

            # Create the rectangle used to draw the arc
            rect = pygame.Rect(
                int(self.center_pos[0] - self.radius),
                int(self.center_pos[1] - self.radius),
                int(self.radius * 2),
                int(self.radius * 2),
            )
            pygame.draw.arc(screen, color, rect, start_angle, end_angle, draw_width)
