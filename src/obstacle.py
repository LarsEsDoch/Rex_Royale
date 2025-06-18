import random

from resources import screen, BIRD_FRAMES, CACTUS_SMALL, CACTUS_LARGE, pygame, logging
from config import GROUND_LEVEL, SCREEN_WIDTH


class Obstacle:

    def __init__(self, score, power_up_type):
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
            if self.type == "bird":
                if power_up_type == "fly":
                    self.y = [GROUND_LEVEL - self.height[0] - random.randint(150, 600)]
                else:
                    self.y = [GROUND_LEVEL - self.height[0] - random.randint(80, 200)]
            else:
                self.y = [GROUND_LEVEL - self.height[0]]
        else:
            self.width, self.height = ([self.frame_images[0].get_width(), self.frame_images[1].get_width()], [self.frame_images[0].get_height(), self.frame_images[1].get_height()])
            self.y = [GROUND_LEVEL - self.height[0], GROUND_LEVEL - self.height[1]]

        self.mask = pygame.mask.from_surface(self.frame_images[0])
        if self.type == "bird":
            self.masks = [pygame.mask.from_surface(image) for image in self.frame_images]
        elif self.type == "double":
            self.masks = [pygame.mask.from_surface(self.frame_images[0]), pygame.mask.from_surface(self.frame_images[1])]
        self.current_frame = 0
        self.animation_timer = 0
        self.got_counted = False

    def update(self, speed):
        if self.type == "bird":
            self.x -= speed * 1.75
        else:
            self.x -= speed
        if self.type == "bird":
            self.animation_timer += 1000/60
            self.current_frame = int(self.animation_timer / 100) % len(self.frame_images)

    def render(self):
        if self.type == "bird":
            screen.blit(self.frame_images[self.current_frame], (self.x, self.y[0]))
        elif self.type == "double":
            screen.blit(self.frame_images[0], (self.x, self.y[0]))
            screen.blit(self.frame_images[1], (self.x + self.width[0] + 10, self.y[1]))
        else:
            screen.blit(self.frame_images[0], (self.x, self.y[0]))
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            if self.type == "double":
                mask_surface = self.masks[0].to_surface()
                mask_surface.set_colorkey((0,0,0))
                mask_surface2 = self.masks[1].to_surface()
                mask_surface2.set_colorkey((0,0,0))
                screen.blit(mask_surface, (self.x, self.y[0]))
                screen.blit(mask_surface2, (self.x + self.width[0] + 10, self.y[1]))
                return
            if self.type == "bird":
                mask_surface = self.masks[self.current_frame].to_surface()
            else:
                mask_surface = self.mask.to_surface()
            mask_surface.set_colorkey((0,0,0))
            screen.blit(mask_surface, (self.x, self.y[0]))

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

    def collides_with(self, dino, ducked):
        if ducked:
            mask = dino.duck_mask
        else:
            mask = dino.masks[dino.current_frame]
        if self.type == "double":
            obstacle_1 = self.mask.overlap(mask, (dino.x - self.x, dino.y - self.y[0]))
            obstacle_2 = self.mask.overlap(mask, (dino.x - self.x - self.width[0] - 10, dino.y - self.y[1]))
            return obstacle_1 is not None or obstacle_2 is not None
        elif self.type == "bird":
            return self.masks[self.current_frame].overlap(mask, (dino.x - self.x, dino.y - self.y[0])) is not None
        else:
            return self.mask.overlap(mask, (dino.x - self.x, dino.y - self.y[0])) is not None