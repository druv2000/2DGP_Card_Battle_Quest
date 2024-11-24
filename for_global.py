# for_global.py

# HUGE_NUMBER
HUGE_NUMBER = float('inf')
HUGE_TIME = float('inf')

# SCREEN_SIZE
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# HIT_ANIMATION
TIME_PER_HIT_ANIMATION = 0.2
HIT_ANIMATION_PER_TIME = 1.0 / TIME_PER_HIT_ANIMATION
FRAME_PER_HIT_ANIMATION = 8

# TAUNT_ANIMATION
TIME_PER_TAUNT_ANIMATION = 1.0
TAUNT_ANIMATION_PER_TIME = 1.0 / TIME_PER_HIT_ANIMATION
FRAME_PER_TAUNT_ANIMATION = 2

# CHARACTER_ANIMATION
TIME_PER_CHARACTER_ANIMATION = 0.3
CHARACTER_ANIMATION_PER_TIME = 1.0 / TIME_PER_CHARACTER_ANIMATION
FRAME_PER_CHARACTER_ANIMATION = 8

# ATTACK_ANIMATION
TIME_PER_ATTACK_ANIMATION = 0.3
ATTACK_ANIMATION_PER_TIME = 1.0 / TIME_PER_ATTACK_ANIMATION
FRAME_PER_ATTACK_ANIMATION = 8

# mouse_position
mouse_x = 0
mouse_y = 0

# card space
CARD_SPACE_X1 = 500
CARD_SPACE_Y1 = 0
CARD_SPACE_X2 = 1100
CARD_SPACE_Y2 = 160

# CARD_EFFECT_ANIMATION
TIME_PER_CARD_EFFECT_ANIMATION = 0.5
CARD_EFFECT_ANIMATION_PER_TIME = 1.0 / TIME_PER_CARD_EFFECT_ANIMATION
FRAME_PER_CARD_EFFECT_ANIMATION = 8

# FOR CARDS
KNIGHT_BODY_TACKLE_RUSH_SPEED = 1500
KNIGHT_BODY_TACKLE_RADIUS = 100
KNIGHT_BODY_TACKLE_KNOCKBACK_DISTANCE = 200

BOWMAN_ROLLING_SPEED = 1000
BOWMAN_ROLLING_ROTATE_SPEED = 2000
BOWMAN_ROLLING_ATK_SPEED_INCREMENT = 30
BOWMAN_ROLLING_ATK_SPEED_DURATION = 3.0

knight_revival_count = 0
knight_revival_radius = 0

mage_revival_count = 0
mage_revival_radius = 0

bowman_revival_count = 0
bowman_revival_radius = 0

MAX_REVIVAL_COUNT = 3

# MANA
MAX_MANA = 10
cur_mana = 5