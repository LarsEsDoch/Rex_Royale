import pygame

from config import logging
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN

pygame.init()
logging.info("Initialized pygame successful")

if FULLSCREEN:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
logging.info("Set screen dimensions")

pygame.display.set_caption("Dino Game")
logging.info("Set window caption")

pygame.display.set_icon(pygame.image.load("textures/images/icon.png"))
logging.info("Set window icon")

clock = pygame.time.Clock()
logging.info("Initialized clock")

font = pygame.font.Font(None, 36)
logging.info("Set font")

BIRD_FRAMES = []
for i in range(17):
    frame_path = f"textures/bird/frame_{i+1}.png"
    logging.debug(f"Loading: {frame_path}")
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (130, 115)).convert_alpha()
    BIRD_FRAMES.append(image)
CACTUS_SMALL = []
for i in range(3):
    frame_path = f"textures/cactus_small/cactus_small_{i+1}.png"
    logging.debug(f"Loading: {frame_path}")
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (60, 70)).convert_alpha()
    CACTUS_SMALL.append(image)
CACTUS_LARGE = []
for i in range(3):
    frame_path = f"textures/cactus_large/cactus_large_{i+1}.png"
    logging.debug(f"Loading: {frame_path}")
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (40, 130)).convert_alpha()
    CACTUS_LARGE.append(image)
DINO_FRAMES = []
for i in range(9):
    frame_path = f"textures/dino/dino_frame_{i}.png"
    logging.debug(f"Loading: {frame_path}")
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (248, 128)).convert_alpha()
    DINO_FRAMES.append(image)
logging.info("Loaded textures")