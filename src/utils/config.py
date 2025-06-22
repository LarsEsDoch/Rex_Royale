import logging
import os

from datetime import datetime

os.makedirs("./logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(
            f"./logs/{datetime.now().strftime('%d.%m.%Y')}_{len([f for f in os.listdir('./logs') if f.startswith(datetime.now().strftime('%d.%m.%Y'))]) + 1}.log"),
        logging.StreamHandler()
    ]
)
logging.info("Started logging")

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FULLSCREEN = False
logging.info("Initialized screen dimensions")

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (40, 40, 40)
BROWN = (150, 100, 50)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (150, 100, 0)
LIGHT_BLUE = (100, 150, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
logging.info("Initialized colors")

GRAVITY = 0.5
GROUND_LEVEL = SCREEN_HEIGHT - 40
OBSTACLE_SPEED = 7
DINO_VELOCITY = -17
SPEED_INCREMENT = 0.001
FRAME_RATE = 60
DIFFICULTY_SPEEDS = {
    "easy": 5,
    "normal": OBSTACLE_SPEED,
    "hard": 9
}
DIFFICULTY_GRAVITIES = {
    "easy": 0.4,
    "normal": GRAVITY,
    "hard": 0.9
}
DIFFICULTY_VELOCITIES = {
    "easy": -18,
    "normal": DINO_VELOCITY,
    "hard": -16
}
logging.info("Initialized game constants")