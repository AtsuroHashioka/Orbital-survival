"""Golden-master test: only a deliberate rule change may move these numbers.

``tests/data/golden_trace.json`` holds one whole game, from the first frame
to game over. Comparison is by exact equality rather than a tolerance:
nothing short of a deliberate rule change should perturb the arithmetic, so
any drift is a real regression.
"""

from typing import Any

import pytest

from orbital_survival.config import MAX_LIVES
from tests._trace import as_rows, build_trace, load_trace

type Frames = list[dict[str, Any]]


@pytest.fixture(scope="module")
def recorded() -> Frames:
    return as_rows(load_trace())


@pytest.fixture(scope="module")
def replayed() -> Frames:
    return as_rows(build_trace())


def test_trace_metadata_matches() -> None:
    """The stored trace must have been produced with the current parameters."""
    stored = load_trace()
    fresh = build_trace()
    assert stored["max_frames"] == fresh["max_frames"]
    assert stored["game_seed"] == fresh["game_seed"]
    assert stored["input_seed"] == fresh["input_seed"]
    assert stored["fields"] == fresh["fields"]


def test_frame_count(recorded: Frames, replayed: Frames) -> None:
    assert len(replayed) == len(recorded)


def test_every_frame_matches(recorded: Frames, replayed: Frames) -> None:
    """Compare frame by frame so a failure names the frame that diverged."""
    for index, (expected, actual) in enumerate(zip(recorded, replayed, strict=True)):
        assert actual == expected, f"simulation diverged at frame {index}"


def test_trace_exercises_both_collision_outcomes(recorded: Frames) -> None:
    """Guard the guard: a trace with no hits or no dodges would prove little."""
    hits = MAX_LIVES - recorded[-1]["lives"]
    # Dodges are the only thing that moves the score now that hits cost
    # lives instead of points, so the count divides straight out of it.
    dodges = recorded[-1]["score"] // 10
    assert hits > 0, "trace never exercises the beam-hit branch"
    assert dodges > 0, "trace never exercises the beam-dodged branch"


def test_trace_ends_at_game_over(recorded: Frames) -> None:
    """The trace records a whole game, so it must stop where one stops.

    A trace cut short by the MAX_FRAMES ceiling would still replay
    identically and pass every test above, while quietly no longer pinning
    down when the run ends — which is the rule this trace exists to guard.
    """
    assert recorded[-1]["lives"] <= 0, "trace does not reach game over"
    assert all(frame["lives"] > 0 for frame in recorded[:-1]), (
        "trace continues past game over"
    )
