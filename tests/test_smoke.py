"""Headless smoke tests: the game must start, draw, and switch scenes.

The golden-master test proves the numbers are unchanged but never touches
rendering. These run the real draw calls against SDL's dummy video driver so
a broken import or a bad blit still fails the suite.
"""

from collections.abc import Iterator

import pygame
import pytest

from orbital_survival.config import (
    NUM_BACKGROUND_STARS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from orbital_survival.game import Game
from orbital_survival.scenes.base import GameMode
from orbital_survival.scenes.game_over import GameOverScene
from orbital_survival.scenes.play import PlayScene
from orbital_survival.scenes.start import StartScene


@pytest.fixture
def game() -> Iterator[Game]:
    instance = Game()
    yield instance
    pygame.quit()


def test_game_starts_on_the_start_screen(game: Game) -> None:
    assert isinstance(game.scene, StartScene)
    assert game.is_running is True


def test_background_stars_are_within_the_screen(game: Game) -> None:
    assert len(game.background_stars) == NUM_BACKGROUND_STARS
    for star in game.background_stars:
        x, y = star.pos
        assert 0 <= x <= SCREEN_WIDTH
        assert 0 <= y <= SCREEN_HEIGHT


def test_start_screen_renders(game: Game) -> None:
    for _ in range(3):
        game._update()
        game._draw()


def test_space_switches_to_play(game: Game) -> None:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()

    assert isinstance(game.scene, PlayScene)


def test_play_screen_renders(game: Game) -> None:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()

    for _ in range(60):
        game._update()
        game._draw()


def test_running_out_of_lives_switches_to_game_over(game: Game) -> None:
    """The switch has to come out of update: no event announces a death."""
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()
    assert isinstance(game.scene, PlayScene)
    game.scene.logic.lives = 0

    game._update()

    assert isinstance(game.scene, GameOverScene)


def test_game_over_screen_renders_and_returns_to_the_title(game: Game) -> None:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()
    assert isinstance(game.scene, PlayScene)
    game.scene.logic.lives = 0
    game._update()

    game._draw()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()

    assert isinstance(game.scene, StartScene)


def test_the_game_over_screen_carries_the_final_tally(game: Game) -> None:
    """The dead scene owns the numbers, so they must ride on the request."""
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()
    assert isinstance(game.scene, PlayScene)
    game.scene.logic.lives = 0
    game.scene.logic.score = 1230

    request = game.scene.update()

    assert request is not None
    assert request.mode is GameMode.GAME_OVER
    assert request.result is not None
    assert request.result.score == 1230


def test_quit_event_stops_the_loop(game: Game) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game._handle_events()

    assert game.is_running is False
