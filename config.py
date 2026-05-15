# config.py
import math

# --- Rendering-related parameters ---

# Screen size
SCREEN_SIZE = 400
SCREEN_WIDTH = SCREEN_SIZE * 3
SCREEN_HEIGHT = SCREEN_SIZE * 2
# Color definitions (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
EARTH_BLUE = (51, 153, 204)
SUN_ORANGE = (252, 130, 0)
# Frame rate
FPS = 120
NUM_BACKGROUND_STARS = 250
BUTTON_RADIUS = 30

# --- Game-system-related parameters ---

CENTER_POS = (
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2 - 50,
)  # Center coordinates of celestial bodies; shifted slightly upward to leave room for buttons
CIRCLE_WIDTH = 2  # Circle line width for celestial bodies

ACCELERATION = 0.0010  # Angular acceleration
FRICTION = 0.99  # Deceleration ratio

# Beam-related parameters
BEAM_SPEED = 2  # Beam expansion speed
BEAM_MAX_RADIUS = SCREEN_SIZE  # Maximum beam radius (used for alive check)

# Planet-related parameters
PLANET_SIZE = 12  # Planet radius
PLANET_ORBIT_RADIUS = 225  # Planet orbital radius
PLANET_INITIAL_ANGLE = math.pi / 2  # Initial planet angle (90 degrees, downward)

# Star-related parameters
STAR_SIZE = PLANET_SIZE * 3  # Star radius

# --- Machine-learning-related parameters ---
MAX_BEAMS = 39  # Max beams in state: (num cannons) x (BEAM_MAX_RADIUS - STAR_SIZE) / BEAM_SPEED / (fire interval in frames)
