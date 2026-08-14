# Orbital Survival

A 2D survival game set in space.  
Control your planet, dodge rotating star beams, and survive as long as possible.

![Gamestart](img/Start.png)
![Gameplay](img/Play.png)

## Overview

You orbit around the center while a star emits beam attacks.  
Your goal is to avoid collisions and keep your score growing.

## Features

- Planet movement with acceleration + friction
- Randomized star rotation and beam firing
- Real-time HUD (speed, acceleration, score, collision count, elapsed time)
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

## Controls

- Left arrow key: accelerate left
- Right arrow key: accelerate right
- Mouse: click and hold the on-screen left/right buttons

## Scoring

- Dodge a beam: `+10`
- Get hit by a beam: `-200` and collision count (`KILLED`) increases by 1

## Project Structure

```text
.
├── img
│  ├── Play.png
│  └── Start.png
├── src
│  └── orbital_survival
│     ├── __init__.py
│     ├── __main__.py          # console-script entry point
│     ├── config.py            # tuning constants
│     ├── game.py              # window, main loop, scene switching
│     ├── logic.py             # physics, collisions and scoring
│     ├── entities
│     │  ├── base.py           # CelestialBody / BaseArc
│     │  ├── beam.py           # Beam, BeamCorpse
│     │  ├── planet.py
│     │  └── star.py
│     ├── scenes
│     │  ├── base.py
│     │  ├── play.py
│     │  └── start.py
│     └── ui
│        ├── hud.py
│        ├── play_button.py
│        └── start_button.py
├── tests
│  ├── _trace.py               # golden-master trace builder
│  ├── conftest.py
│  ├── data
│  │  └── golden_trace.json
│  ├── test_entities.py
│  ├── test_golden.py
│  ├── test_logic.py
│  └── test_smoke.py
├── pyproject.toml
├── README.md
└── uv.lock
```
