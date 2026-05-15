# system/base_manager.py


class Base_Manager:
    """
    Base class for game modes.
    """

    def __init__(self, screen, clock):
        """
        Initialize a Base_Manager object.

        :param screen: Screen object
        :param clock: Clock object
        """
        self.screen = screen
        # Clock object for time management
        self.clock = clock

    def update(self):
        """
        Update the state of in-game objects.
        """
        pass

    def draw(self):
        """
        Draw objects on the screen.
        """
        pass
