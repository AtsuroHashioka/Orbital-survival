"""Shared test setup.

Forces SDL onto its dummy backends so the suite runs on machines and CI
runners without a display or sound device. This must happen before pygame
is imported anywhere, hence its placement in conftest.
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
