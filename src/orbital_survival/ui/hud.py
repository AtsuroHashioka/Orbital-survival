import pygame
from orbital_survival.config import GREEN, SCREEN_WIDTH, WHITE


class HUD:
    """
    Heads-Up Display class that shows game information on screen.
    """

    def __init__(self, font_size=30):
        """
        Initialize a HUD object.
        :param font_size: Font size for displayed text
        """
        # Automatically select an available monospaced font.
        # This keeps digit width constant and avoids visual jitter.
        font_names = ["consolas", "dejavusansmono", "couriernew", "monospace"]
        self.font = pygame.font.SysFont(font_names, font_size)
        self.color = WHITE

    def draw(
        self,
        screen,
        planet_speed,
        actual_planet_acceleration,
        kill_count,
        score,
        elapsed_time,
    ):
        """
        Draw HUD information on the screen.
        :param screen: Target Pygame screen object
        :param ...: Game data to display
        """

        # --- Speed display ---
        display_speed = planet_speed * 1000
        speed_text = self.font.render(f"SPEED:{display_speed:+08.4f}", True, GREEN)
        speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(speed_text, speed_rect)

        # --- Elapsed-time display ---
        time_text = self.font.render(f"TIME: {elapsed_time / 1000:6.2f}s", True, GREEN)
        time_rect = time_text.get_rect(topleft=(10, 10))
        screen.blit(time_text, time_rect)

        # --- Acceleration display ---
        display_accel = actual_planet_acceleration * 1000
        accel_text = self.font.render(f"ACCEL:{display_accel:+08.4f}", True, GREEN)
        accel_rect = accel_text.get_rect(
            topright=(SCREEN_WIDTH - 10, speed_rect.bottom + 5)
        )
        screen.blit(accel_text, accel_rect)

        # --- Score and collision count display ---
        score_text = self.font.render(f"SCORE: {score}", True, GREEN)
        score_rect = score_text.get_rect(topleft=(10, time_rect.bottom + 5))
        screen.blit(score_text, score_rect)

        kill_text = self.font.render(f"KILLED: {kill_count}", True, GREEN)
        kill_rect = kill_text.get_rect(topleft=(10, score_rect.bottom + 5))
        screen.blit(kill_text, kill_rect)
