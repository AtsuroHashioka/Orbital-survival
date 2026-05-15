# system/logic.py

import math

from config import (
    CENTER_POS,
    PLANET_INITIAL_ANGLE,
    PLANET_ORBIT_RADIUS,
    PLANET_SIZE,
    STAR_SIZE,
)
from entities.planet import Planet
from entities.star import Star
from entities.beam import BeamCorpse


class Logic:
    """
    Class that manages game logic.
    """

    def __init__(self):
        """
        Initialize the Logic object.

        :param center_pos: Center position of planet and star (x, y)
        :param planet_size: Planet size (radius)
        :param planet_initial_angle: Initial planet angle
        :param planet_orbit_radius: Planet orbital radius
        :param star_size: Star size (radius)
        """
        # --- Create objects ---
        # Create Planet object
        self.planet = Planet(
            CENTER_POS, PLANET_SIZE, PLANET_INITIAL_ANGLE, PLANET_ORBIT_RADIUS
        )
        # Create Star object
        self.star = Star(CENTER_POS, STAR_SIZE)

        # Direction button states
        self.left_active = False
        self.right_active = False

        # Beam corpse list
        self.corpses = []
        # Score and kill count
        self.score = 0
        self.kill_count = 0

    def update(self):
        """
        Update the state of in-game objects.
        """

        # Determine acceleration direction
        direction = 0
        if self.left_active:
            direction = 1
        elif self.right_active:
            direction = -1

        # Update planet state with selected direction
        self.planet.update(direction)
        # Update star state based on AI
        self.star.update()
        # Update corpses
        self._update_corpses()

        # Check collisions and remove beams
        self._check_collisions()

    def _update_corpses(self):
        """Update beam corpses and remove expired ones."""
        for corpse in self.corpses:
            corpse.update()
        self.corpses = [c for c in self.corpses if c.is_alive()]

    def _check_collisions(self):
        """Check collisions between the planet and beams."""
        planet_angle = self.planet.angle
        planet_orbit_radius = self.planet.radius
        planet_size = self.planet.size

        # Calculate angular margin for collision checks
        if planet_orbit_radius > planet_size:
            angle_margin = math.asin(planet_size / planet_orbit_radius)
        else:
            angle_margin = math.pi

        # Check beam collisions, add collided beams to corpse list,
        # and keep surviving beams.
        surviving_beams = []  # List of surviving beams
        for beam in self.star.beams:
            beam_front_radius = beam.radius + beam.width + self.planet.size
            beam_back_radius = max(0, beam.radius - beam.width - self.planet.size)

            collided = False
            if beam_back_radius < planet_orbit_radius < beam_front_radius:
                angle_diff = (planet_angle + beam.angle + math.pi) % (
                    2 * math.pi
                ) - math.pi

                if abs(angle_diff) < beam.arc_range / 2 + angle_margin:
                    self.kill_count += 1
                    self.score -= 200
                    # Add corpse for collided beam
                    self.corpses.append(
                        BeamCorpse(
                            beam.center_pos,
                            beam.angle,
                            beam.arc_range,
                            beam.radius,
                            beam.width,
                        )
                    )
                    collided = True
            elif beam.radius > planet_orbit_radius and not beam.dodged:
                self.score += 10
                beam.dodged = True

            if not collided:
                # Keep as surviving beam
                surviving_beams.append(beam)

        # Update star beam list (surviving beams only)
        self.star.beams = surviving_beams
