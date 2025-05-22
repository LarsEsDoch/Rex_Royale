import random

from config import SCREEN_WIDTH, GROUND_LEVEL
from resources import COIN_IMAGES, screen, logging, pygame


class PowerUp:
    def __init__(self):
        self.type = random.choice(["multiplicator", "immortality", "fly"])
        self.image = COIN_IMAGES[0] if self.type == "multiplicator" else COIN_IMAGES[1] if self.type == "immortality" else COIN_IMAGES[2]
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

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def complete_off_screen(self):
        return self.x + self.width < -200


    def collides_with(self, dino):
        return dino.x < self.x + self.width and dino.x + dino.hitbox_width > self.x and dino.hitbox_y + dino.hitbox_height > self.y