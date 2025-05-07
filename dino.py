from resources import screen, pygame
from config import GROUND_LEVEL, GRAVITY
from resources import logging

class Dino:

    def __init__(self):
        self.width = 150
        self.height = 150
        self.hitbox_width = 120
        self.hitbox_height = 120
        self.x = 50
        self.y = GROUND_LEVEL - self.height
        self.velocity_y = 0
        self.jump = False
        self.image = pygame.image.load('textures/dino/dino_texture.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.gravity_multiplier = 1.1
        logging.info("Initialized dino")

    def update(self, score):
        if self.jump:
            self.y += self.velocity_y

            if score > 4000:
                self.gravity_multiplier = min(1.1 + score / 40000, 2)

            self.velocity_y += GRAVITY * self.gravity_multiplier

            if self.y >= GROUND_LEVEL - self.height:
                self.y = GROUND_LEVEL - self.height
                self.jump = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def start_jump(self):
        if self.y >= GROUND_LEVEL - self.height - 70 and self.velocity_y >= 1:
            self.velocity_y = -16
        if not self.jump:
            self.jump = True
            self.velocity_y = -17