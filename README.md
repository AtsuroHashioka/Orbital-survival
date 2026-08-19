# Orbital Survival

A 2D survival game set in space.  
Control your planet, dodge rotating star beams, and survive as long as possible.

![Gamestart](img/Start.png)
![Gameplay](img/Play.png)
![Gameover](img/GameOver.png)

## Overview

You orbit around the center while a star emits beam attacks.  
You start with three lives and lose one on every hit. When the last one is
gone the run ends, so your score is a record of how long you lasted.

## Features

- Planet movement with acceleration + friction
- Randomized star rotation and beam firing
- Real-time HUD (speed, acceleration, score, remaining lives, elapsed time)
- Keyboard and mouse support

## Requirements

- Python 3.12+
- uv

## Installation

```bash
uv sync
```

## Run

```bash
uv run orbital-survival
```

## Development

```bash
uv run mypy                # type check (strict)
uv run ruff check --fix    # lint
uv run ruff format         # format
```

## Controls

- Left arrow key: accelerate left
- Right arrow key: accelerate right
- Mouse: click and hold the on-screen left/right buttons
- Space: start a run from the title screen, and return there after a game over

## Rules

- You start with 3 lives, set by `MAX_LIVES` in `config.py`
- Dodge a beam: `+10` score
- Get hit by a beam: lose one life. The score is never docked
- Lives reach 0: **GAME OVER**. Press space to return to the title

Hits are resolved per beam with no window of invincibility, so two beams
arriving on the same frame cost two lives.

The HUD shows the lives you have left as red hearts. Raise `MAX_LIVES` above
five and the row collapses to a `♥ x N` count instead.

## Project Structure

```text
.
├── img
│  ├── GameOver.png
│  ├── Play.png
│  └── Start.png
├── src
│  └── orbital_survival
│     ├── __init__.py
│     ├── __main__.py          # console-script entry point
│     ├── config.py            # tuning constants
│     ├── game.py              # window, main loop, scene switching
│     ├── logic.py             # physics, collisions, lives and scoring
│     ├── entities
│     │  ├── base.py           # CelestialBody / BaseArc
│     │  ├── beam.py           # Beam, BeamCorpse
│     │  ├── planet.py
│     │  └── star.py
│     ├── scenes
│     │  ├── base.py           # Scene, GameMode, SceneRequest
│     │  ├── game_over.py
│     │  ├── play.py
│     │  └── start.py
│     └── ui
│        ├── hud.py
│        ├── play_button.py
│        └── start_button.py
├── pyproject.toml
├── README.md
└── uv.lock
```
