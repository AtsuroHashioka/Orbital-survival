"""Golden-master test: the refactor must not change what the game computes.

``tests/data/golden_trace.json`` was recorded from the pre-refactor code.
Every later stage of the refactor has to reproduce it exactly. Comparison is
by exact equality rather than a tolerance: nothing in a rename-and-annotate
refactor should perturb the arithmetic, so any drift is a real regression.
"""

import pytest

from tests._trace import as_rows, build_trace, load_trace


@pytest.fixture(scope="module")
def recorded() -> list[dict]:
    return as_rows(load_trace())


@pytest.fixture(scope="module")
def replayed() -> list[dict]:
    return as_rows(build_trace())


def test_trace_metadata_matches() -> None:
    """The stored trace must have been produced with the current parameters."""
    stored = load_trace()
    fresh = build_trace()
    assert stored["frames"] == fresh["frames"]
    assert stored["game_seed"] == fresh["game_seed"]
    assert stored["input_seed"] == fresh["input_seed"]
    assert stored["fields"] == fresh["fields"]


def test_frame_count(recorded: list[dict], replayed: list[dict]) -> None:
    assert len(replayed) == len(recorded)


def test_every_frame_matches(recorded: list[dict], replayed: list[dict]) -> None:
    """Compare frame by frame so a failure names the frame that diverged."""
    for index, (expected, actual) in enumerate(zip(recorded, replayed, strict=True)):
        assert actual == expected, f"simulation diverged at frame {index}"


def test_trace_exercises_both_collision_outcomes(recorded: list[dict]) -> None:
    """Guard the guard: a trace with no hits or no dodges would prove little."""
    kills = recorded[-1]["kill_count"]
    dodges = (recorded[-1]["score"] + 200 * kills) // 10
    assert kills > 0, "trace never exercises the beam-hit branch"
    assert dodges > 0, "trace never exercises the beam-dodged branch"
