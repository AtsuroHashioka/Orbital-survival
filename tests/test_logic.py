"""Unit tests for collision resolution and scoring.

These drive ``Logic._check_collisions`` directly with hand-placed beams.
Going through ``Logic.update`` would pull in the star's random firing and
make it impossible to isolate a single collision.
"""

import math
import random

import pytest

from config import CENTER_POS, PLANET_INITIAL_ANGLE, STAR_SIZE
from entities.beam import Beam
from system.logic import Logic

BEAM_ARC_RANGE = math.pi * 60 / 360
BEAM_WIDTH = int(STAR_SIZE // 4)

# The planet starts at pi/2. pygame draws arcs with counter-clockwise
# mathematical angles while the screen Y axis points down, so a beam drawn at
# theta lines up with a planet at -theta. Facing the planet therefore means
# the beam sits at -pi/2, not pi/2.
ALIGNED_ANGLE = -PLANET_INITIAL_ANGLE
OPPOSITE_ANGLE = PLANET_INITIAL_ANGLE


@pytest.fixture
def logic() -> Logic:
    """A Logic instance with the star's random beams cleared out."""
    random.seed(0)
    instance = Logic()
    instance.star.beams = []
    instance.corpses = []
    instance.score = 0
    instance.kill_count = 0
    return instance


def make_beam(angle: float, radius: float) -> Beam:
    return Beam(CENTER_POS, angle, BEAM_ARC_RANGE, radius, BEAM_WIDTH)


def test_beam_crossing_the_planet_scores_a_hit(logic: Logic) -> None:
    logic.star.beams = [make_beam(ALIGNED_ANGLE, logic.planet.radius)]

    logic._check_collisions()

    assert logic.kill_count == 1
    assert logic.score == -200


def test_hit_beam_is_removed_and_leaves_a_corpse(logic: Logic) -> None:
    logic.star.beams = [make_beam(ALIGNED_ANGLE, logic.planet.radius)]

    logic._check_collisions()

    assert logic.star.beams == []
    assert len(logic.corpses) == 1
    assert logic.corpses[0].angle == pytest.approx(ALIGNED_ANGLE % (2 * math.pi))


def test_beam_at_the_planet_radius_but_elsewhere_misses(logic: Logic) -> None:
    beam = make_beam(OPPOSITE_ANGLE, logic.planet.radius)
    logic.star.beams = [beam]

    logic._check_collisions()

    assert logic.kill_count == 0
    assert logic.score == 0
    assert logic.star.beams == [beam]


def test_beam_past_the_orbit_scores_a_dodge(logic: Logic) -> None:
    beam = make_beam(OPPOSITE_ANGLE, logic.planet.radius + 25)
    logic.star.beams = [beam]

    logic._check_collisions()

    assert logic.score == 10
    assert logic.kill_count == 0
    assert beam.dodged is True


def test_a_dodge_is_only_scored_once(logic: Logic) -> None:
    logic.star.beams = [make_beam(OPPOSITE_ANGLE, logic.planet.radius + 25)]

    logic._check_collisions()
    logic._check_collisions()
    logic._check_collisions()

    assert logic.score == 10


def test_beam_short_of_the_orbit_scores_nothing(logic: Logic) -> None:
    logic.star.beams = [make_beam(ALIGNED_ANGLE, STAR_SIZE)]

    logic._check_collisions()

    assert logic.score == 0
    assert logic.kill_count == 0


def test_collision_survives_angle_wraparound(logic: Logic) -> None:
    """A beam angle given beyond 2pi must still line up with the planet."""
    logic.star.beams = [make_beam(ALIGNED_ANGLE + 4 * math.pi, logic.planet.radius)]

    logic._check_collisions()

    assert logic.kill_count == 1


def test_corpses_expire(logic: Logic) -> None:
    logic.star.beams = [make_beam(ALIGNED_ANGLE, logic.planet.radius)]
    logic._check_collisions()
    corpse = logic.corpses[0]

    for _ in range(corpse.DURATION):
        logic._update_corpses()

    assert logic.corpses == []


def test_direction_is_left_right_or_idle(logic: Logic) -> None:
    """left+right pressed together resolves to left, matching the original."""
    logic.left_active = True
    logic.right_active = True
    before = logic.planet.speed

    logic.update()

    assert logic.planet.speed > before
