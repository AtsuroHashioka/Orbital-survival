"""Deterministic simulation trace used as a golden master.

The game's only source of non-determinism is the ``random`` module (the
star's initial angle/speed, its per-frame direction choice, and its firing
rolls). ``pygame.time.get_ticks`` feeds the HUD only and never reaches the
logic layer, so seeding ``random`` makes a run reproducible frame by frame.

Player input is generated from a *separate* ``random.Random`` instance so
that driving the planet does not consume draws from the global stream the
game itself uses.

The trace is stored as one row per frame rather than one object per frame:
repeating the field names 600 times triples the file size for no gain.
"""

import json
import random
from pathlib import Path
from typing import Any

from orbital_survival.config import MAX_LIVES
from orbital_survival.logic import Logic

TRACE_PATH = Path(__file__).parent / "data" / "golden_trace.json"

# MAX_FRAMES is a ceiling, not a length: the trace stops at game over, so
# that what it pins down is a whole game rather than an arbitrary slice of
# one. These seeds were picked over a small search for a long run that
# still exercises both collision outcomes — 1000 frames, 3 hits and 45
# dodges — while leaving headroom under the ceiling, so that a future
# tuning change lengthening the run does not silently truncate the trace.
MAX_FRAMES = 1200
GAME_SEED = 249
INPUT_SEED = 1

FIELDS = (
    "planet_angle",
    "planet_speed",
    "planet_accel",
    "planet_x",
    "planet_y",
    "star_angle",
    "star_speed",
    "cannon_radii",
    "beam_radii",
    "beam_dodged",
    "corpse_lives",
    "score",
    "lives",
)


def _inputs(rng: random.Random) -> tuple[bool, bool]:
    """Pick a left/right/idle input for one frame."""
    roll = rng.random()
    return roll < 0.35, 0.35 <= roll < 0.70


def build_trace() -> dict[str, Any]:
    """Record the logic layer frame by frame until the run ends.

    Stops at game over, or at MAX_FRAMES if the run somehow outlives it.
    """
    random.seed(GAME_SEED)
    logic = Logic()
    input_rng = random.Random(INPUT_SEED)

    states = []
    for _ in range(MAX_FRAMES):
        logic.left_active, logic.right_active = _inputs(input_rng)
        logic.update()
        states.append(
            [
                logic.planet.angle,
                logic.planet.speed,
                logic.planet.actual_acceleration,
                logic.planet.x,
                logic.planet.y,
                logic.star.angle,
                logic.star.speed,
                list(logic.star.cannon_radii),
                [beam.radius for beam in logic.star.beams],
                [beam.dodged for beam in logic.star.beams],
                [corpse.life for corpse in logic.corpses],
                logic.score,
                logic.lives,
            ]
        )

        if logic.is_game_over:
            break

    return {
        "max_frames": MAX_FRAMES,
        "game_seed": GAME_SEED,
        "input_seed": INPUT_SEED,
        "fields": list(FIELDS),
        "states": states,
    }


def as_rows(trace: dict[str, Any]) -> list[dict[str, Any]]:
    """Zip the packed rows back into per-frame dicts for readable assertions."""
    fields = trace["fields"]
    return [dict(zip(fields, state, strict=True)) for state in trace["states"]]


def load_trace() -> dict[str, Any]:
    """Read the recorded trace from disk."""
    with TRACE_PATH.open(encoding="utf-8") as handle:
        loaded: dict[str, Any] = json.load(handle)
    return loaded


def save_trace(trace: dict[str, Any]) -> None:
    """Write a trace to disk with one frame per line, so diffs stay readable."""
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    header = {key: value for key, value in trace.items() if key != "states"}
    lines = [json.dumps(state, separators=(",", ":")) for state in trace["states"]]
    with TRACE_PATH.open("w", encoding="utf-8") as handle:
        handle.write("{\n")
        for key, value in header.items():
            handle.write(f" {json.dumps(key)}: {json.dumps(value)},\n")
        handle.write(' "states": [\n')
        handle.write(",\n".join(f"  {line}" for line in lines))
        handle.write("\n ]\n}\n")


if __name__ == "__main__":
    built = build_trace()
    save_trace(built)
    rows = as_rows(built)
    hits = MAX_LIVES - rows[-1]["lives"]
    dodges = rows[-1]["score"] // 10
    print(f"wrote {TRACE_PATH} ({len(rows)} frames)")
    print(f"final score={rows[-1]['score']} hits={hits} dodges={dodges}")
