"""Entry point for `orbital-survival` and `python -m orbital_survival`."""

from orbital_survival.game import Game


def main() -> None:
    """Start the game and run it until the window is closed."""
    Game().run()


if __name__ == "__main__":
    main()
