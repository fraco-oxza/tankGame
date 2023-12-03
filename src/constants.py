from effects import AmbientEffect

# Default settings
DEFAULT_NUMBER_OF_PLAYERS = 2
DEFAULT_ROUNDS = 1
DEFAULT_NUMBER_OF_BOTS = 0
DEFAULT_TYPE_EFFECT = AmbientEffect.NONE
DEFAULT_GRAVITY = 9.8  # m/s^2
DEFAULT_WINDOWS_SIZE = (1280, 720)

# Colors
BLACK = (0, 0, 0)
GRAY = (94, 94, 110)
DarkGreen = "#1C542D"
White = "#FFFFFF"
HUD_BACKGROUND = "#282828"

# Limits
EPSILON = 0.0001
MIN_GRAVITY = 1.0
MAX_GRAVITY = 30.0
SHOOT_MAX_SPEED = 400
FPS = 75

# Terrain settings
SEA_LEVEL = 200  # px
MOUNTAINS = 3
VALLEYS = 2

# Speed settings
X_SPEED = 4.0
X_WIND_SPEED = 16.0
TERRAIN_FALL_X_SPEED = 5.0

# Development settings
DEVELOPMENT_MODE = False

# Tank settings
DAMAGE_PER_SPEED = 0.1  # expresses how much damage a tank must suffer for each m/s it carries at the moment of falling
TANK_RADIO = 18
TANK_OFFSET = 20  # tanks float this many pixels up
BOT_SLEEP_TIME = 1000  # ms

# Map settings
MAP_SEED = -1

# Weather settings
SNOWFLAKES = 100
WIND_EFFECT_SCALE = 10.0
WIND_SPEED_CHANGE_SCALE = 5.0
