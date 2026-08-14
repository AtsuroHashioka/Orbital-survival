import pygame
import math
import random

from orbital_survival.entities.base import CelestialBody
from orbital_survival.entities.beam import Beam
from orbital_survival.config import BLACK, CIRCLE_WIDTH, FPS, SUN_ORANGE

CANNON_COUNT = 3  # Cannons spaced evenly around the star


class Star(CelestialBody):
    """
    Class representing the star.
    """

    def __init__(self, center_pos, size):
        """
        Initialize a Star object.
        :param center_pos: Star center position (x, y)
        :param size: Star radius
        """
        super().__init__(
            center_pos=center_pos,
            size=size,
            acceleration=self.ACCELERATION,
            friction=self.FRICTION,
            # Set initial angle and speed randomly
            angle=random.uniform(0, 2 * math.pi),
            speed=random.uniform(-0.005, 0.005),
        )
        self.color = SUN_ORANGE
        self.arc_range = math.pi * 60 / 360  # Draw range of black arc

        # Timer and current direction for random control
        self.random_timer = 0
        self.random_direction = 0
        self.beam_timer = 0

        self.beams = []  # List of emitted beams
        self.cannon_initial_radius = self.size  # Initial cannon radius
        # Radius of each cannon
        self.cannon_radii = [self.cannon_initial_radius] * CANNON_COUNT

    def update(self):
        """
        Randomly update star rotation (phase) and emit beams.
        """
        # Update and remove beams
        for beam in self.beams:
            beam.update()
        self.beams = [beam for beam in self.beams if beam.is_alive()]

        self.random_timer += 1
        self.beam_timer += 1

        # Randomly change acceleration direction
        if self.random_timer >= FPS // 8:
            self.random_timer = 0
            # Set probabilities: 20% for 0, 40% each for left/right
            self.random_direction = random.choices(
                [-1, 0, 1], weights=[40, 20, 40], k=1
            )[0]

        # Emit beams
        if self.beam_timer >= FPS // 8:
            self.beam_timer = 0
            # Emit beams from the three cannons
            for i in range(CANNON_COUNT):
                if random.random() < 0.20:  # 20% chance to fire
                    cannon_angle = self.angle + (2 * math.pi / CANNON_COUNT) * i
                    beam = Beam(
                        self.center_pos,
                        cannon_angle,
                        self.arc_range,
                        self.size,
                        int(self.size // 4),
                    )
                    self.beams.append(beam)
                    # Firing effect: temporarily shrink corresponding cannon radius
                    self.cannon_radii[i] = self.cannon_initial_radius * 0.75

        # Gradually restore each cannon radius to initial size
        for i in range(CANNON_COUNT):
            if self.cannon_radii[i] < self.cannon_initial_radius:
                self.cannon_radii[i] += 0.5  # Radius recovery speed
                # Clamp so it does not exceed initial radius
                if self.cannon_radii[i] > self.cannon_initial_radius:
                    self.cannon_radii[i] = self.cannon_initial_radius

        self.update_angle_and_speed(self.random_direction)

    def draw(self, screen):
        """
        Draw the star, cannons, and beams on the screen.
        :param screen: Target Pygame screen object
        """
        # Draw emitted beams first so they appear behind the star
        for beam in self.beams:
            beam.draw(screen)

        # Draw star body (black circle)
        pygame.draw.circle(screen, BLACK, self.center_pos, self.size / 2)
        # Draw star outline (orange border)
        pygame.draw.circle(
            screen, self.color, self.center_pos, self.size / 2, CIRCLE_WIDTH
        )  # Border width: 2

        # Draw cannons around the current angle
        for i in range(CANNON_COUNT):
            arc_radius = self.cannon_radii[i]  # Use radius for each cannon
            # Split phase into equal parts
            cannon_angle = self.angle + (2 * math.pi / CANNON_COUNT) * i
            cannon_angle %= 2 * math.pi  # Keep angle in the range [0, 2π)
            # Compute start and end angles of arc
            start_angle = cannon_angle - self.arc_range / 2
            end_angle = cannon_angle + self.arc_range / 2
            rect = pygame.Rect(
                self.center_pos[0] - arc_radius,
                self.center_pos[1] - arc_radius,
                arc_radius * 2,
                arc_radius * 2,
            )
            pygame.draw.arc(
                screen, self.color, rect, start_angle, end_angle, int(self.size // 4)
            )
