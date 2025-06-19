import pygame

from src.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, logging
from src.utils.utils import load_frames_scaled, load_frame, load_frames

pygame.init()
pygame.mixer.init()
logging.info("Initialized pygame and pygame mixer successful")

if FULLSCREEN:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
logging.info("Set screen dimensions")

pygame.display.set_caption("Rex Royale")
logging.info("Set window caption")

pygame.display.set_icon(pygame.image.load("./assets/textures/images/icon.png"))
logging.info("Set window icon")

clock = pygame.time.Clock()
logging.info("Initialized clock")

font_small = pygame.font.Font(None, 24)
font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 48)
logging.info("Set font")

screen.fill((5, 5, 5))
text = font.render("Loading...", True, (255, 255, 255))
text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
screen.blit(text, text_rect)
logging.info("rendered text")

GAME_OVER_IMAGE = load_frame("./assets/textures/texts/game_over.png", (1200, 675))
BACKGROUNDS_DAY = load_frames("./assets/textures/backgrounds/day/day_background_*.png", 4)
BACKGROUNDS_NIGHT = load_frames("./assets/textures/backgrounds/night/night_background_*.png", 4)

BIRD_FRAMES = load_frames_scaled("./assets/textures/bird/frame_*.png", 17, (130, 115))
CACTUS_SMALL = load_frames_scaled("./assets/textures/cactus_small/cactus_small_*.png", 3, (60, 70))
CACTUS_LARGE = load_frames_scaled("./assets/textures/cactus_large/cactus_large_*.png", 3, (40, 130))
DINO_FRAMES = load_frames_scaled("./assets/textures/dino/dino_frame_*.png", 9, (248, 128))
DINO_DUCK = load_frame("./assets/textures/dino/dino_duck.png", (248, 128))
FIREBALL_FRAMES = load_frames_scaled("./assets/textures/power_ups/fireball/fireball_*.png", 4, (180, 60))
COIN_IMAGES = [pygame.image.load(f"./assets/textures/power_ups/multiplicator.png"),
               pygame.image.load(f"./assets/textures/power_ups/immortality.png"),
               pygame.image.load(f"./assets/textures/power_ups/fly.png"),
               pygame.image.load(f"./assets/textures/power_ups/fireball.png")]
COIN_IMAGES = [pygame.transform.scale(image, (80, 80)).convert_alpha() for image in COIN_IMAGES]
logging.info("Loaded textures")

JUMP_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/jump_sound.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/game_over_sound.wav")
LANDING_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/landing_sound.wav")
SELECT_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/select_sound.wav")
COLLIDE_FIREBALL_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/collide_fireball_sound.wav")
SHOT_FIREBALL_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/shot_fireball_sound.wav")
CLAIM_COIN_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/claim_coin_sound.wav")
IMMORTALITY_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/immortality_sound.wav")
WING_FLAP_SOUND = pygame.mixer.Sound("./assets/sounds/sound_effects/wing_flap_sound.wav")
logging.info("Loaded sounds")

logging.debug("Initialized resources successful")