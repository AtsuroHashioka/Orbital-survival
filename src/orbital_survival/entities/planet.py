import pygame
import math

from orbital_survival.entities.base import CelestialBody
from orbital_survival.config import BLACK, CIRCLE_WIDTH, EARTH_BLUE


class Planet(CelestialBody):
    """
    Class representing the planet.
    """

    # --- Class constants ---
    MAX_TRAJECTORY_LENGTH = 2 * math.pi / 6
    TRAJECTORY_NUM = 60

    def __init__(self, center_pos, size, angle, orbit_radius):
        """
        Initialize a Planet object.
        :param center_pos: Orbital center position (x, y)
        :param size: Planet radius
        :param angle: Initial planet angle (radians)
        :param orbit_radius: Orbital radius
        """
        super().__init__(
            center_pos=center_pos,
            size=size,
            acceleration=self.ACCELERATION,
            friction=self.FRICTION,
            angle=angle,
            speed=0.0,
        )
        self.orbit_radius = orbit_radius
        self.color = EARTH_BLUE

        # Keep per-frame actual angular acceleration for display
        self.actual_acceleration = 0.0

        # Compute initial coordinates
        self.x = self.center_pos[0] + self.orbit_radius * math.cos(self.angle)
        self.y = self.center_pos[1] + self.orbit_radius * math.sin(self.angle)

    def update(self, direction):
        """
        Update planet state every frame.
        1. Compute current speed and angle with input and friction.
        2. Compute angular acceleration for HUD display.
        3. Update position.
        :param direction: User input direction (-1: left, 0: none, 1: right)
        """
        # Store speed before update to compute actual acceleration
        speed_before_update = self.speed

        # Update speed and angle
        self.update_angle_and_speed(direction)

        # Compute acceleration values for HUD
        self.actual_acceleration = self.speed - speed_before_update

        # Compute (x, y) coordinates
        self.x = self.center_pos[0] + self.orbit_radius * math.cos(self.angle)
        self.y = self.center_pos[1] + self.orbit_radius * math.sin(self.angle)

    def draw(self, screen):
        """
        Draw the planet and its trajectory.
        :param screen: Target Pygame screen object
        """
        # --- Draw trajectory ---
        self._draw_trajectory(screen)

        # --- Draw planet body ---
        self._draw_planet(screen)

    def _draw_planet(self, screen):
        """
        Draw the planet body on the screen.
        :param screen: Target Pygame screen object
        """

        # --- Draw body ---
        # Draw main planet body (black circle)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size)
        # Draw planet outline (blue border)
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.size, CIRCLE_WIDTH
        )  # Border width: 2

    def _draw_trajectory(self, screen):
        """
        Draw the planet trajectory on the screen.
        :param screen: Target Pygame screen object
        """
        for n in range(self.TRAJECTORY_NUM):
            tjy_angle = self.angle - self.MAX_TRAJECTORY_LENGTH * (
                self.speed / self.MAX_SPEED
            ) * (n / self.TRAJECTORY_NUM)
            tjy_x = self.center_pos[0] + self.orbit_radius * math.cos(tjy_angle)
            tjy_y = self.center_pos[1] + self.orbit_radius * math.sin(tjy_angle)
            tjy_size = self.size * (1 - n / self.TRAJECTORY_NUM)
            tjy_color = tuple(
                int(c * math.sqrt(1 - n / self.TRAJECTORY_NUM)) for c in self.color
            )
            pygame.draw.circle(
                screen, tjy_color, (int(tjy_x), int(tjy_y)), int(tjy_size)
            )
