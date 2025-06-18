from src.utils.config import SCREEN_WIDTH
from src.utils.resources import FIREBALL_FRAMES, screen, logging, pygame


class Fireball():
    def __init__(self, y):
        self.x = 200
        self.y = y + 20
        self.frames = FIREBALL_FRAMES
        self.width, self.height = (self.frames[0].get_width(), self.frames[0].get_height())
        self.animation_timer = 0
        self.current_frame = 0
        self.masks = [pygame.mask.from_surface(image) for image in self.frames]

    def update(self):
        self.x += 5
        self.animation_timer += 1000/60
        self.current_frame = int(self.animation_timer / 100) % len(self.frames)

    def render(self):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            mask_surface = self.masks[self.current_frame].to_surface()
            mask_surface.set_colorkey((0, 0, 0))
            screen.blit(mask_surface, (self.x, self.y))

    def complete_off_screen(self):
        return self.x + self.width > SCREEN_WIDTH + 200

    def collides_with(self, obstacle):
        if obstacle.type == "double":
            obstacle_1 = obstacle.mask.overlap(self.masks[self.current_frame], (self.x - obstacle.x, self.y - obstacle.y[0]))
            obstacle_2 = obstacle.mask.overlap(self.masks[self.current_frame],
                                           (self.x - obstacle.x - obstacle.width[0] - 10, self.y - obstacle.y[1]))
            return obstacle_1 is not None or obstacle_2 is not None
        elif obstacle.type == "bird":
            return obstacle.masks[obstacle.current_frame].overlap(self.masks[self.current_frame],
                                                          (self.x - obstacle.x, self.y - obstacle.y[0])) is not None
        else:
            return obstacle.mask.overlap(self.masks[self.current_frame], (self.x - obstacle.x, self.y - obstacle.y[0])) is not None