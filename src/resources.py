import pygame

from config import logging
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN
from utils import load_frames, load_frame

pygame.init()
logging.info("Initialized pygame successful")

if FULLSCREEN:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
logging.info("Set screen dimensions")

pygame.display.set_caption("Rex Royale")
logging.info("Set window caption")

pygame.display.set_icon(pygame.image.load("./textures/images/icon.png"))
logging.info("Set window icon")

clock = pygame.time.Clock()
logging.info("Initialized clock")

font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 48)
logging.info("Set font")

screen.fill((5, 5, 5))
text = font.render("Loading...", True, (255, 255, 255))
text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
screen.blit(text, text_rect)
logging.info("rendered text")

BIRD_FRAMES = load_frames("./textures/bird/frame_*.png", 17, (130, 115))
CACTUS_SMALL = load_frames("./textures/cactus_small/cactus_small_*.png", 3, (60, 70))
CACTUS_LARGE = load_frames("./textures/cactus_large/cactus_large_*.png", 3, (40, 130))
DINO_FRAMES = load_frames("./textures/dino/dino_frame_*.png", 9, (248, 128))
DINO_DUCK = load_frame("./textures/dino/dino_duck.png", (248, 128))
FIREBALL_FRAMES = load_frames("./textures/power_ups/fireball/fireball_*.png", 4, (180, 60))
COIN_IMAGES = [pygame.image.load(f"./textures/power_ups/multiplicator.png"),
               pygame.image.load(f"./textures/power_ups/immortality.png"),
               pygame.image.load(f"./textures/power_ups/fly.png"),
               pygame.image.load(f"./textures/power_ups/fireball.png")]
COIN_IMAGES = [pygame.transform.scale(image, (80, 80)).convert_alpha() for image in COIN_IMAGES]
logging.info("Loaded textures")