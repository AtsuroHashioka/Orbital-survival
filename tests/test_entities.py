"""Unit tests for the orbital physics and the beam lifecycle."""

import math

import pytest

from orbital_survival.config import (
    ACCELERATION,
    BEAM_MAX_RADIUS,
    BEAM_SPEED,
    CENTER_POS,
    FRICTION,
    PLANET_ORBIT_RADIUS,
    PLANET_SIZE,
)
from orbital_survival.entities.base import CelestialBody
from orbital_survival.entities.beam import Beam, BeamCorpse


@pytest.fixture
def planet():
    from orbital_survival.entities.planet import Planet

    return Planet(CENTER_POS, PLANET_SIZE, 0.0, PLANET_ORBIT_RADIUS)


def test_planet_starts_at_rest(planet) -> None:
    assert planet.speed == 0.0
    assert planet.angle == 0.0


def test_acceleration_is_damped_by_friction(planet) -> None:
    planet.update(1)

    assert planet.speed == pytest.approx(ACCELERATION * FRICTION)


def test_reported_acceleration_is_the_speed_delta(planet) -> None:
    planet.update(1)
    first = planet.speed

    planet.update(1)

    assert planet.actual_acceleration == pytest.approx(planet.speed - first)


def test_idle_input_decays_speed(planet) -> None:
    planet.update(1)
    moving = planet.speed

    planet.update(0)

    assert planet.speed == pytest.approx(moving * FRICTION)
    assert planet.speed < moving


def test_speed_converges_to_max_speed(planet) -> None:
    for _ in range(5000):
        planet.update(1)

    assert planet.speed == pytest.approx(CelestialBody.MAX_SPEED)


def test_angle_stays_normalized(planet) -> None:
    planet.angle = 2 * math.pi - 1e-9

    for _ in range(200):
        planet.update(1)
        assert 0.0 <= planet.angle < 2 * math.pi


def test_position_follows_the_orbit(planet) -> None:
    planet.update(1)

    assert planet.x == pytest.approx(
        CENTER_POS[0] + PLANET_ORBIT_RADIUS * math.cos(planet.angle)
    )
    assert planet.y == pytest.approx(
        CENTER_POS[1] + PLANET_ORBIT_RADIUS * math.sin(planet.angle)
    )


def test_planet_stays_on_its_orbit(planet) -> None:
    for _ in range(500):
        planet.update(1)

    distance = math.hypot(planet.x - CENTER_POS[0], planet.y - CENTER_POS[1])
    assert distance == pytest.approx(PLANET_ORBIT_RADIUS)


def make_beam(radius: float) -> Beam:
    return Beam(CENTER_POS, 0.0, math.pi / 3, radius, 9)


def test_beam_expands_at_beam_speed() -> None:
    beam = make_beam(50)

    beam.update()

    assert beam.radius == 50 + BEAM_SPEED


def test_beam_is_alive_below_max_radius() -> None:
    assert make_beam(BEAM_MAX_RADIUS - 1).is_alive() is True


def test_beam_dies_at_max_radius() -> None:
    assert make_beam(BEAM_MAX_RADIUS).is_alive() is False


def test_beam_starts_undodged() -> None:
    assert make_beam(50).dodged is False


def test_corpse_counts_down_and_expires() -> None:
    corpse = BeamCorpse(CENTER_POS, 0.0, math.pi / 3, 200, 9)
    assert corpse.is_alive() is True

    for _ in range(corpse.DURATION):
        corpse.update()

    assert corpse.is_alive() is False


def test_star_normalizes_its_initial_angle() -> None:
    from orbital_survival.entities.star import Star

    star = Star(CENTER_POS, 36)

    assert 0.0 <= star.angle < 2 * math.pi
    assert star.beams == []
