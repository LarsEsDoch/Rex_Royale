import random

from src.utils.config import SCREEN_WIDTH, GROUND_LEVEL
from src.utils.resources import COIN_IMAGES, screen, logging, pygame


class PowerUp:

    def __init__(self, score):
        if score < 5000:
            self.type = random.choice(["fly", "immortality", "fireball"])
        else:
            self.type = random.choice(["multiplicator", "immortality", "fly", "fireball"])
        self.image = COIN_IMAGES[0] if self.type == "multiplicator" else COIN_IMAGES[1] if self.type == "immortality" else COIN_IMAGES[2] if self.type == "fly" else COIN_IMAGES[3]
        self.mask = pygame.mask.from_surface(self.image)
        self.width, self.height = (self.image.get_width(), self.image.get_width())
        self.x = SCREEN_WIDTH
        self.y = GROUND_LEVEL - self.height - 10
        self.multiplier = random.randint(1, 3)
        self.lifespan = random.randint(10, 20)
        self.current_time = 0
        self.y_velocity_boost = 0.5
        logging.debug("Placed power up")


    def update(self, speed):
        self.x -= speed


    def render(self):
        screen.blit(self.image, (self.x, self.y))
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            mask_surface = self.mask.to_surface()
            mask_surface.set_colorkey((0,0,0))
            screen.blit(mask_surface, (self.x, self.y))


    def complete_off_screen(self):
        return self.x + self.width < -200


    def collides_with(self, dino):
        return self.mask.overlap(dino.masks[dino.current_frame], (dino.x - self.x, dino.y - self.y)) is not None