from effects import AmbientEffect


GRAVITY = 9.8  # m/s^2
DEVELOPMENT_MODE = False
DEFAULT_WINDOWS_SIZE = (1280, 720)
EPSILON = 1e-8

SHOOT_MAX_SPEED = 400
TERRAIN_LINE_WIDTH = 1  # px
SEA_LEVEL = 200  # px
FPS = 60
MOUNTAINS = 3
VALLEYS = 2
BLACK = (0, 0, 0)
GRAY = (94, 94, 110)
TERRAIN_FALL_X_SPEED = 5.0
DAMAGE_PER_SPEED = 0.1  # expresses how much damage a tank must suffer for each m/s it carries at the moment of falling
X_SPEED = 4.0
TANK_RADIO = 18
DarkGreen = "#1C542D"
White = "#FFFFFF"

H_WINNER = (210, 60)
DESTWARNING = (900, 0)
TANK_WINNER = (650, 350)

TANK_OFFSET = 20  # tanks float this many pixels up

MAP_SEED = -1
SNOWFLAKES = 100
DEFAULT_NUMBER_OF_PLAYERS = 2
DEFAULT_ROUNDS = 1
DEFAULT_NUMBER_OF_BOTS = 0
DEFAULT_TYPE_EFFECT = AmbientEffect.NONE
# Menu constants
HUD_BACKGROUND = "#282828"
WIND_EFFECT_SCALE = 10.0
WIND_SPEED_CHANGE_SCALE = 5.0
