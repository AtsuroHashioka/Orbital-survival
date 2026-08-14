"""Headless smoke tests: the game must start, draw, and switch scenes.

The golden-master test proves the numbers are unchanged but never touches
rendering. These run the real draw calls against SDL's dummy video driver so
a broken import or a bad blit still fails the suite.
"""

import pygame
import pytest

from orbital_survival.game import Game


@pytest.fixture
def game():
    instance = Game()
    yield instance
    pygame.quit()


def test_game_starts_on_the_start_screen(game) -> None:
    from orbital_survival.scenes.start import Start_Manager

    assert isinstance(game.manager, Start_Manager)
    assert game.is_running is True


def test_background_stars_are_within_the_screen(game) -> None:
    from orbital_survival.config import SCREEN_HEIGHT, SCREEN_WIDTH, NUM_BACKGROUND_STARS

    assert len(game.background_stars) == NUM_BACKGROUND_STARS
    for star in game.background_stars:
        x, y = star["pos"]
        assert 0 <= x <= SCREEN_WIDTH
        assert 0 <= y <= SCREEN_HEIGHT


def test_start_screen_renders(game) -> None:
    for _ in range(3):
        game._update()
        game._draw()


def test_space_switches_to_play(game) -> None:
    from orbital_survival.scenes.play import Play_Manager

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()

    assert isinstance(game.manager, Play_Manager)


def test_play_screen_renders(game) -> None:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game._handle_events()

    for _ in range(60):
        game._update()
        game._draw()


def test_quit_event_stops_the_loop(game) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game._handle_events()

    assert game.is_running is False
