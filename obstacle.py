import random

from resources import screen, clock, BIRD_FRAMES, CACTUS_SMALL, CACTUS_LARGE, pygame, logging
from config import GROUND_LEVEL, SCREEN_WIDTH

class Obstacle:

    def __init__(self, score):
        self.frame_images = []
        if score < 5000:
            self.type = random.choice(["small", "large", "double"])
        else:
            self.type = random.choice(["small", "large", "double", "bird"])

        if self.type == "bird":
            self.x = SCREEN_WIDTH*1.6
            frame_images = BIRD_FRAMES
            for bird_image in frame_images:
                self.frame_images.append(bird_image)
        elif self.type == "small":
            self.x = SCREEN_WIDTH + random.randint(50, 400)
            self.frame_images = [CACTUS_SMALL[random.randint(0, len(CACTUS_SMALL) - 1)]]
        elif self.type == "large" :
            self.x = SCREEN_WIDTH + random.randint(50, 500)
            self.frame_images = [CACTUS_LARGE[random.randint(0, len(CACTUS_LARGE) - 1)]]
        else:
            double_type = random.randint(0, 3)
            self.x = SCREEN_WIDTH + random.randint(50, 500)
            if double_type == 0:
                self.frame_images = [CACTUS_SMALL[random.randint(0, len(CACTUS_SMALL) - 1)],
                                     CACTUS_SMALL[random.randint(0, len(CACTUS_SMALL) - 1)]]
            elif double_type == 1:
                self.frame_images = [CACTUS_LARGE[random.randint(0, len(CACTUS_LARGE) - 1)],
                                     CACTUS_LARGE[random.randint(0, len(CACTUS_LARGE) - 1)]]
            elif double_type == 2:
                self.frame_images = [CACTUS_SMALL[random.randint(0, len(CACTUS_SMALL) - 1)],
                                     CACTUS_LARGE[random.randint(0, len(CACTUS_LARGE) - 1)]]
            else:
                self.frame_images = [CACTUS_LARGE[random.randint(0, len(CACTUS_LARGE) - 1)],
                                     CACTUS_SMALL[random.randint(0, len(CACTUS_SMALL) - 1)]]

        if not self.type == "double":
            self.width, self.height = ([self.frame_images[0].get_width()], [self.frame_images[0].get_height()])
            self.y = [GROUND_LEVEL - self.height[0] - 200 if self.type == "bird" else GROUND_LEVEL - self.height[0]]
        else:
            self.width, self.height = ([self.frame_images[0].get_width(), self.frame_images[1].get_width()], [self.frame_images[0].get_height(), self.frame_images[1].get_height()])
            self.y = [GROUND_LEVEL - self.height[0], GROUND_LEVEL - self.height[1]]

        self.current_frame = 0
        self.animation_timer = 0
        self.got_counted = False

    def update(self, speed):
        if self.type == "bird":
            self.x -= speed * 1.75
        else:
            self.x -= speed

    def draw(self):
        if self.type == "bird":
            self.animation_timer += clock.get_time()
            self.current_frame = int(self.animation_timer / 100) % len(self.frame_images)
            screen.blit(self.frame_images[self.current_frame], (self.x, self.y[0]))
        elif self.type == "double":
            screen.blit(self.frame_images[0], (self.x, self.y[0]))
            screen.blit(self.frame_images[1], (self.x + self.width[0], self.y[1]))
        else:
            screen.blit(self.frame_images[0], (self.x, self.y[0]))
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            if self.type == "double":
                pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y[0], self.width[0], self.height[0]), 2)
                pygame.draw.rect(screen, (255, 0, 0),
                                 (self.x + self.width[0], self.y[1], self.width[1], self.height[1]), 2)
                return
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y[0], self.width[0], self.height[0]), 2)

    def off_screen(self):
        if self.type == "double":
            return self.x + self.width[0]*2 < 50
        else:
            return self.x + self.width[0] < 50

    def complete_off_screen(self):
        if self.type == "double":
            return self.x + self.width[0]*2 < -200
        else:
            return self.x + self.width[0] < -200

    def collides_with(self, dino):
        if self.type == "bird":
            return dino.x < self.x + self.width[0] and dino.x + dino.hitbox_width > self.x and self.y[0] < dino.hitbox_y + dino.hitbox_height < self.y[0] + self.height[0 ]
        if self.type == "double":
            first_hitbox = (
                    dino.x < self.x + self.width[0]
                    and dino.x + dino.hitbox_width > self.x
                    and self.y[0] < dino.hitbox_y + dino.hitbox_height
                    and dino.hitbox_y < self.y[0] + self.height[0]
            )
            second_hitbox = (
                    dino.x < self.x + self.width[0] + self.width[1]
                    and dino.x + dino.hitbox_width > self.x + self.width[0]
                    and self.y[1] < dino.hitbox_y + dino.hitbox_height
                    and dino.hitbox_y < self.y[1] + self.height[1]
            )
            return first_hitbox or second_hitbox
        else:
            return dino.x < self.x + self.width[0] and dino.x + dino.hitbox_width > self.x and dino.hitbox_y + dino.hitbox_height > self.y[0]