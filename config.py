from math import sin, pi

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FULLSCREEN = False
print("Initialized screen dimensions")

WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
print("Initialized colors")

GRAVITY = 0.6
GROUND_LEVEL = SCREEN_HEIGHT - 40
OBSTACLE_SPEED = 7
SPEED_INCREMENT = 0.001
FRAME_RATE = 60
print("Initialized game constants")


# Utility functions
def ease_out_cubic(t):
    return 1 - (1 - t)**3

def ease_out_sine(t):
    return sin((t * pi) / 2)