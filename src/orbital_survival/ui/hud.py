"""The on-screen readout of speed, acceleration, score, kills and time."""

from dataclasses import dataclass

import pygame

from orbital_survival.config import FONT_NAMES, GREEN, SCREEN_WIDTH, WHITE

# Angular values are tiny fractions of a radian; scaling them makes the
# readout move visibly instead of sitting at 0.0000.
DISPLAY_SCALE = 1000
MARGIN = 10
LINE_GAP = 5


@dataclass(frozen=True, slots=True)
class HUDState:
    """The values one HUD frame displays."""

    planet_speed: float
    planet_acceleration: float
    kill_count: int
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
        """Draw the HUD, stacking time/score/kills left and speed/accel right."""
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

        kill_text = self.font.render(f"KILLED: {state.kill_count}", True, GREEN)
        kill_rect = kill_text.get_rect(topleft=(MARGIN, score_rect.bottom + LINE_GAP))
        screen.blit(kill_text, kill_rect)
