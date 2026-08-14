"""Game rules: physics stepping, collision resolution and scoring.

This layer deliberately imports no pygame drawing code, so it can be run
headless — which is what makes the golden-master test possible.
"""

import math
from typing import Final

from orbital_survival.config import (
    CENTER_POS,
    PLANET_INITIAL_ANGLE,
    PLANET_ORBIT_RADIUS,
    PLANET_SIZE,
    STAR_SIZE,
)
from orbital_survival.entities.beam import BeamCorpse
from orbital_survival.entities.planet import Planet
from orbital_survival.entities.star import Star

DODGE_SCORE: Final[int] = 10
HIT_PENALTY: Final[int] = 200


class Logic:
    """
    Class that manages game logic.
    """

    def __init__(self) -> None:
        self.planet = Planet(
            CENTER_POS, PLANET_SIZE, PLANET_INITIAL_ANGLE, PLANET_ORBIT_RADIUS
        )
        self.star = Star(CENTER_POS, STAR_SIZE)

        # Direction button states
        self.left_active = False
        self.right_active = False

        self.corpses: list[BeamCorpse] = []
        self.score = 0
        self.kill_count = 0

    def update(self) -> None:
        """Step everything one frame, then resolve collisions.

        Holding both directions resolves to left; neither means coasting.
        """
        direction = 0
        if self.left_active:
            direction = 1
        elif self.right_active:
            direction = -1

        self.planet.update(direction)
        self.star.update()
        self._update_corpses()

        self._check_collisions()

    def _update_corpses(self) -> None:
        """Age the beam corpses and drop the ones that have expired."""
        for corpse in self.corpses:
            corpse.update()
        self.corpses = [corpse for corpse in self.corpses if corpse.is_alive()]

    def _check_collisions(self) -> None:
        """Resolve planet-beam collisions and update the score.

        A beam and the planet meet when the expanding arc overlaps the orbit
        radially *and* the two overlap angularly. The angular test adds a
        margin of asin(planet_size / orbit_radius), the half-angle the planet
        subtends from the center, so the planet is treated as a disc rather
        than as a point.

        The angular difference is a *sum*, `planet.angle + beam.angle`, not a
        subtraction. pygame.draw.arc takes counter-clockwise mathematical
        angles while the screen Y axis points down, so an arc drawn at theta
        appears where the planet's frame calls -theta. Adding the two angles
        is what cancels that flip.
        """
        planet_angle = self.planet.angle
        planet_orbit_radius = self.planet.orbit_radius
        planet_size = self.planet.size

        if planet_orbit_radius > planet_size:
            angle_margin = math.asin(planet_size / planet_orbit_radius)
        else:
            # The planet is bigger than its own orbit: every angle overlaps.
            angle_margin = math.pi

        surviving_beams = []
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
                    self.score -= HIT_PENALTY
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
                # Past the orbit without ever entering the band above, so it
                # was dodged. The flag keeps it from scoring again each frame.
                self.score += DODGE_SCORE
                beam.dodged = True

            if not collided:
                surviving_beams.append(beam)

        self.star.beams = surviving_beams
