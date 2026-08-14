"""The play screen: wires input to the logic layer and renders the result."""

import pygame

from orbital_survival.config import BUTTON_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from orbital_survival.logic import Logic
from orbital_survival.scenes.base import GameMode, Scene
from orbital_survival.ui.hud import HUD, HUDState
from orbital_survival.ui.play_button import PlayButton

BUTTON_SPACING = 100  # Horizontal offset of each button from the center
BUTTON_BOTTOM_MARGIN = 80


class PlayScene(Scene):
    """
    Subclass that manages PLAY mode.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self._initialize_state()

    def _initialize_state(self) -> None:
        """Build a fresh round: logic, buttons and HUD."""
        self.start_time = pygame.time.get_ticks()

        self.logic = Logic()

        # Circular buttons, centered on the lower edge.
        self.left_button = PlayButton(
            SCREEN_WIDTH / 2 - BUTTON_SPACING,
            SCREEN_HEIGHT - BUTTON_BOTTOM_MARGIN,
            BUTTON_RADIUS,
            "left",
        )
        self.right_button = PlayButton(
            SCREEN_WIDTH / 2 + BUTTON_SPACING,
            SCREEN_HEIGHT - BUTTON_BOTTOM_MARGIN,
            BUTTON_RADIUS,
            "right",
        )
        self.hud = HUD()

    def handle_event(self, event: pygame.event.Event) -> GameMode | None:
        """Play mode never switches away on its own."""
        return None

    def update(self) -> None:
        """Poll keyboard and mouse, then step the logic one frame.

        Input is polled rather than event-driven so that holding a key or a
        button keeps accelerating, instead of nudging once per key repeat.
        """
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.logic.left_active = keys[pygame.K_LEFT] or (
            mouse_buttons[0] and self.left_button.is_clicked(mouse_pos)
        )
        self.logic.right_active = keys[pygame.K_RIGHT] or (
            mouse_buttons[0] and self.right_button.is_clicked(mouse_pos)
        )

        self.logic.update()

    def draw(self) -> None:
        """Draw corpses, star, planet, controls and HUD, back to front."""
        for corpse in self.logic.corpses:
            corpse.draw(self.screen)

        self.logic.star.draw(self.screen)
        self.logic.planet.draw(self.screen)

        self.left_button.draw(self.screen, self.logic.left_active)
        self.right_button.draw(self.screen, self.logic.right_active)

        self.hud.draw(
            self.screen,
            HUDState(
                planet_speed=self.logic.planet.speed,
                planet_acceleration=self.logic.planet.actual_acceleration,
                kill_count=self.logic.kill_count,
                score=self.logic.score,
                elapsed_ms=pygame.time.get_ticks() - self.start_time,
            ),
        )
