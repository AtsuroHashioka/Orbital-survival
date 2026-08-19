"""The on-screen readout of speed, acceleration, score, lives and time."""

from dataclasses import dataclass

import pygame

from orbital_survival.config import (
    FONT_NAMES,
    GREEN,
    MAX_LIVES,
    RED,
    SCREEN_WIDTH,
    WHITE,
)

# Angular values are tiny fractions of a radian; scaling them makes the
# readout move visibly instead of sitting at 0.0000.
DISPLAY_SCALE = 1000
MARGIN = 10
LINE_GAP = 5

HEART = "♥"
# Past this many lives a row of hearts stops being readable at a glance, so
# the row collapses to a count instead. The choice keys off MAX_LIVES rather
# than the current life total, so the format never changes mid-round.
MAX_HEARTS_SHOWN = 5


def lives_text(lives: int) -> str:
    """Render the remaining lives as hearts, or as a count if there are many."""
    remaining = max(0, lives)
    if MAX_LIVES <= MAX_HEARTS_SHOWN:
        return " ".join([HEART] * remaining)
    return f"{HEART} x {remaining}"


@dataclass(frozen=True, slots=True)
class HUDState:
    """The values one HUD frame displays."""

    planet_speed: float
    planet_acceleration: float
    lives: int
    score: int
    elapsed_ms: int


class HUD:
    """
    Heads-Up Display class that shows game information on screen.
    """

    def __init__(self, font_size: int = 30) -> None:
        self.font = pygame.font.SysFont(FONT_NAMES, font_size)
        self.color = WHITE

    def draw(self, screen: pygame.Surface, state: HUDState) -> None:
        """Draw the HUD, stacking time/score/lives left and speed/accel right."""
        display_speed = state.planet_speed * DISPLAY_SCALE
        speed_text = self.font.render(f"SPEED:{display_speed:+08.4f}", True, GREEN)
        speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - MARGIN, MARGIN))
        screen.blit(speed_text, speed_rect)

        time_text = self.font.render(
            f"TIME: {state.elapsed_ms / 1000:6.2f}s", True, GREEN
        )
        time_rect = time_text.get_rect(topleft=(MARGIN, MARGIN))
        screen.blit(time_text, time_rect)

        display_accel = state.planet_acceleration * DISPLAY_SCALE
        accel_text = self.font.render(f"ACCEL:{display_accel:+08.4f}", True, GREEN)
        accel_rect = accel_text.get_rect(
            topright=(SCREEN_WIDTH - MARGIN, speed_rect.bottom + LINE_GAP)
        )
        screen.blit(accel_text, accel_rect)

        score_text = self.font.render(f"SCORE: {state.score}", True, GREEN)
        score_rect = score_text.get_rect(topleft=(MARGIN, time_rect.bottom + LINE_GAP))
        screen.blit(score_text, score_rect)

        # The hearts carry no label: unlike the numbers above them they need
        # no naming, and red already sets them apart from the green readout.
        heart_text = self.font.render(lives_text(state.lives), True, RED)
        heart_rect = heart_text.get_rect(topleft=(MARGIN, score_rect.bottom + LINE_GAP))
        screen.blit(heart_text, heart_rect)
