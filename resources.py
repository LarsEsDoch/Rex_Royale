import pygame

from config import logging
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN

pygame.init()
logging.info("Initialized pygame successful")

BIRD_FRAMES = []
for i in range(17):
    frame_path = f"textures/bird/frame_{i+1}.png"
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (130, 115))
    BIRD_FRAMES.append(image)
CACTUS_SMALL = []
for i in range(3):
    frame_path = f"textures/cactus_small/cactus_small_{i+1}.png"
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (60, 70))
    CACTUS_SMALL.append(image)
CACTUS_LARGE = []
for i in range(3):
    frame_path = f"textures/cactus_large/cactus_large_{i+1}.png"
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (40, 130))
    CACTUS_LARGE.append(image)
logging.info("Loaded textures")

if FULLSCREEN:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
logging.info("Set screen dimensions")

pygame.display.set_caption("Dino Game")
logging.info("Set window caption")

#pygame.display.set_icon(pygame.image.load("textures/icon.png"))
logging.info("Set window icon")

clock = pygame.time.Clock()
logging.info("Initialized clock")

font = pygame.font.Font(None, 36)
logging.info("Set font")