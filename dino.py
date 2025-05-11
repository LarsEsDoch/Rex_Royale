from resources import screen, pygame, DINO_FRAMES, clock
from config import GROUND_LEVEL, GRAVITY, DINO_VELOCITY
from resources import logging

class Dino:

    def __init__(self):
        self.width = 248
        self.height = 128
        self.hitbox_width = 215
        self.hitbox_height = 80
        self.x = 50
        self.y = GROUND_LEVEL - self.height
        self.hitbox_y_offset = 20
        self.hitbox_y = self.y - self.hitbox_y_offset
        self.velocity_y = 0
        self.jump = False
        self.frames = DINO_FRAMES
        self.animation_timer = 0
        self.current_frame = 0
        self.gravity_multiplier = 1.1
        logging.info("Initialized dino")

    def update(self, score):
        if self.y >= GROUND_LEVEL - self.height - 10:
            self.animation_timer += clock.get_time()
            self.current_frame = int(self.animation_timer / 50) % len(self.frames)
        else:
            self.current_frame = 8
        if self.jump:
            self.y += self.velocity_y
            self.hitbox_y = self.y - self.hitbox_y_offset

            if score > 4000:
                self.gravity_multiplier = min(1.1 + score / 40000, 2)

            self.velocity_y += GRAVITY * self.gravity_multiplier

            if self.y >= GROUND_LEVEL - self.height:
                self.y = GROUND_LEVEL - self.height
                self.hitbox_y = self.y - self.hitbox_y_offset
                self.jump = False

    def draw(self):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), (self.x + (self.width - self.hitbox_width) // 2,
                                                   self.hitbox_y + (self.height - self.hitbox_height) // 2,
                                                   self.hitbox_width, self.hitbox_height), 2)


    def start_jump(self):
        if self.y >= GROUND_LEVEL - self.height - 50 and self.velocity_y >= 1:
            self.velocity_y = DINO_VELOCITY + 1
            logging.debug("Jump started")
        if not self.jump:
            self.jump = True
            self.velocity_y = DINO_VELOCITY
            logging.debug("Jump started")