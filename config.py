import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/game.log"),
        logging.StreamHandler()
    ]
)
logging.info("Started logging")

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FULLSCREEN = False
logging.info("Initialized screen dimensions")

WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
logging.info("Initialized colors")

GRAVITY = 0.6
GROUND_LEVEL = SCREEN_HEIGHT - 40
OBSTACLE_SPEED = 7
SPEED_INCREMENT = 0.001
FRAME_RATE = 60
logging.info("Initialized game constants")