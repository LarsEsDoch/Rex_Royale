from src.utils.resources import screen, pygame, DINO_FRAMES, logging, DINO_DUCK, JUMP_SOUND, WING_FLAP_SOUND
from src.utils.config import GROUND_LEVEL, GRAVITY, DINO_VELOCITY, SCREEN_HEIGHT
from src.utils.resources import LANDING_SOUND


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
        self.duck_image = DINO_DUCK
        self.masks = [pygame.mask.from_surface(image) for image in self.frames]
        self.duck_mask = pygame.mask.from_surface(self.duck_image)
        self.animation_timer = 0
        self.current_frame = 0
        self.gravity_multiplier = 1.1
        logging.info("Initialized dino")

    def update(self, score, sound_volume):
        self.animation_timer += 1000/60
        if self.y >= GROUND_LEVEL - self.height - 10:
            self.current_frame = int(self.animation_timer / 50) % len(self.frames)
        else:
            self.current_frame = int(self.animation_timer / 100) % len(self.frames)
        if self.jump:
            self.y += self.velocity_y
            self.hitbox_y = self.y - self.hitbox_y_offset

            if score > 4000:
                self.gravity_multiplier = min(1.1 + score / 40000, 2)

            self.velocity_y += GRAVITY * self.gravity_multiplier

            if self.y >= GROUND_LEVEL - self.height - 40 and self.velocity_y >= 1:
                self.y = GROUND_LEVEL - self.height - 40
                self.hitbox_y = self.y - self.hitbox_y_offset
                self.jump = False
                LANDING_SOUND.set_volume(sound_volume)
                LANDING_SOUND.play()

        if self.y >= GROUND_LEVEL - self.height - 40:
            self.y = min(self.y + self.velocity_y, GROUND_LEVEL - self.height)

    def render(self, ducked):
        if ducked:
            screen.blit(self.duck_image, (self.x, self.y))
            if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                mask_surface = self.duck_mask.to_surface()
                mask_surface.set_colorkey((0,0,0))
                screen.blit(mask_surface, (self.x, self.y))
        else:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))
            if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                mask_surface = self.masks[self.current_frame].to_surface()
                mask_surface.set_colorkey((0,0,0))
                screen.blit(mask_surface, (self.x, self.y))


    def start_jump(self, power_up_type, sound_volume):
        if power_up_type == "fly" and self.y >= GROUND_LEVEL - self.height - 10:
            self.jump = True
            self.velocity_y = DINO_VELOCITY
            JUMP_SOUND.set_volume(sound_volume)
            JUMP_SOUND.play()
            logging.debug("Flying started")
        elif power_up_type == "fly" and self.y < SCREEN_HEIGHT - self.height - 10:
            self.jump = True
            self.velocity_y = DINO_VELOCITY/2
            WING_FLAP_SOUND.set_volume(sound_volume)
            WING_FLAP_SOUND.play()
            logging.debug("Flying started")
        if not self.jump:
            self.jump = True
            self.velocity_y = DINO_VELOCITY
            JUMP_SOUND.set_volume(sound_volume)
            JUMP_SOUND.play()
            logging.debug("Jump started")