import pygame
import math
from orbital_survival.config import BLACK, WHITE


class PlayButton:
    """
    Class representing circular arrow buttons on the play screen.
    """

    def __init__(self, center_x, center_y, radius, direction):
        """
        Initialize a button object.
        :param center_x: Button center x-coordinate
        :param center_y: Button center y-coordinate
        :param radius: Button radius
        :param direction: Arrow direction ('left' or 'right')
        """
        self.center = (center_x, center_y)
        self.radius = radius
        self.direction = direction

        # Pre-render button images for better performance.
        # Two states: normal (black background, white icon) and active (inverted).
        self.image_normal = self._create_surface(icon_color=WHITE, bg_color=BLACK)
        self.image_active = self._create_surface(icon_color=BLACK, bg_color=WHITE)
        self.rect = self.image_normal.get_rect(center=self.center)

    def _create_surface(self, icon_color, bg_color):
        """
        Internal method to create a button surface with specified icon colors.
        :param icon_color: Arrow icon color
        :return: Rendered Pygame Surface object
        """
        # Create a transparent surface sized to button diameter
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # Draw background circle
        pygame.draw.circle(surface, bg_color, (self.radius, self.radius), self.radius)
        # Add a white circular border
        pygame.draw.circle(surface, WHITE, (self.radius, self.radius), self.radius, 2)

        # Compute vertices for the arrow triangle
        # Coordinates are relative to button radius
        arrow_size = self.radius * 0.4
        if self.direction == "left":
            p1 = (self.radius - arrow_size, self.radius)
            p2 = (self.radius + arrow_size, self.radius - arrow_size)
            p3 = (self.radius + arrow_size, self.radius + arrow_size)
        else:  # 'right'
            p1 = (self.radius + arrow_size, self.radius)
            p2 = (self.radius - arrow_size, self.radius - arrow_size)
            p3 = (self.radius - arrow_size, self.radius + arrow_size)

        # Draw smooth arrow polygon
        pygame.draw.polygon(surface, icon_color, [p1, p2, p3])

        return surface

    def draw(self, screen, is_active=False):
        """
        Draw the button and switch style based on active state.
        :param screen: Target Pygame screen object
        :param is_active: Whether the button is currently pressed
        """
        if is_active:
            screen.blit(self.image_active, self.rect)
        else:
            screen.blit(self.image_normal, self.rect)

    def is_clicked(self, pos):
        """
        Check whether the given position is inside the circular button area.
        :param pos: Mouse click coordinates (x, y)
        :return: True if clicked, otherwise False
        """
        # Compare distance from center against radius
        return (
            math.hypot(pos[0] - self.center[0], pos[1] - self.center[1]) <= self.radius
        )
