import random

from resources import screen, clock, BIRD_FRAMES, CACTUS_SMALL, CACTUS_LARGE, pygame, logging
from config import GROUND_LEVEL, SCREEN_WIDTH

class Obstacle:

    def __init__(self, score):
        self.frame_images = []
        if score < 5000:
            self.type = random.choice(["small", "large"])
        else:
            self.type = random.choice(["small", "large", "bird"])

        if self.type == "bird":
            self.x = SCREEN_WIDTH*2.2
            frame_images = BIRD_FRAMES
            for bird_image in frame_images:
                self.frame_images.append(bird_image)
        elif self.type == "small":
            self.x = SCREEN_WIDTH + random.randint(50, 400)
            self.frame_images = [CACTUS_SMALL[random.randint(0, len(CACTUS_SMALL) - 1)]]
        else:
            self.x = SCREEN_WIDTH + random.randint(50, 500)
            self.frame_images = [CACTUS_LARGE[random.randint(0, len(CACTUS_LARGE) - 1)]]

        self.width, self.height = (self.frame_images[0].get_width(), self.frame_images[0].get_height())
        self.y = GROUND_LEVEL - self.height - 200 if self.type == "bird" else GROUND_LEVEL - self.height
        self.current_frame = 0
        self.animation_timer = 0
        self.got_counted = False

    def update(self, speed):
        if self.type == "bird":
            self.x -= speed * 1.2
        self.x -= speed

    def draw(self):
        if self.type == "bird":
            self.animation_timer += clock.get_time()
            self.current_frame = int(self.animation_timer / 100) % len(self.frame_images)
            screen.blit(self.frame_images[self.current_frame], (self.x, self.y))
            if self.current_frame == 17:
                self.current_frame = 0
        else:
            screen.blit(self.frame_images[0], (self.x, self.y))
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def off_screen(self):
        return self.x + self.width < 50

    def complete_off_screen(self):
        return self.x + self.width < -200

    def collides_with(self, dino):
        if self.type == "bird":

            return dino.x < self.x + self.width and dino.x + dino.hitbox_width > self.x and self.y < dino.y + dino.hitbox_height < self.y + self.height

        return dino.x < self.x + self.width and dino.x + dino.hitbox_width > self.x and dino.y + dino.hitbox_height > self.y