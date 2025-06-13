import random
import hashlib
import os
import json

from config import SCREEN_WIDTH, BLACK, SPEED_INCREMENT, \
    GROUND_LEVEL, OBSTACLE_SPEED, WHITE, RED, BROWN, GOLD, SILVER, BRONZE, LIGHT_BLUE, BLUE, FRAME_RATE, \
    SCREEN_HEIGHT
from fireball import Fireball
from powerUp import PowerUp
from utils import ease_out_sine, ease_out_cubic
from resources import screen, clock, font, pygame
from obstacle import Obstacle
from resources import logging

class Game:

    def __init__(self, show_fps, custom_obstacle_speed, fps):
        logging.info("Initializing game...")
        self.fps = fps
        self.running = True
        self.pause = True
        self.game_over = False
        self.score = 0
        if custom_obstacle_speed is None:
            self.obstacle_speed = OBSTACLE_SPEED
            self.original_obstacle_speed = OBSTACLE_SPEED
        else:
            self.obstacle_speed = custom_obstacle_speed
            self.original_obstacle_speed = custom_obstacle_speed
        from dino import Dino
        self.dino = Dino()
        self.obstacles = []
        self.power_ups = []
        self.fireballs = []
        self.power_up_timer = random.randint(30 * 60, 45 * 60)
        self.power_up_timer = -self.power_up_timer
        self.power_up_type = None
        self.power_up_spacing = 0
        self.accounts = {}
        self.load_scores()
        self.high_score = 0
        self.username = ""
        self.password = ""
        self.hashed_password = ""
        self.username_existing = False
        self.checked_username = False
        self.unlocked_user = False
        self.show_list = False
        self.high_score_list_y = 0
        self.target_high_score_list_y = 0
        self.spacing = 0
        self.cursor_tick = 0
        self.game_over_scale = 1
        self.game_over_time = 0
        self.game_over_fade_in = 0
        self.blend_in_time = 0
        self.show_fps = show_fps
        self.press_to_return = 0

        self.background_day = pygame.image.load('./textures/desert_day/desert_day_background.png').convert_alpha()
        self.background_day_flipped = pygame.transform.flip(self.background_day, True, False).convert_alpha()
        self.background_day_2 = pygame.image.load('./textures/desert_day/desert_day_background_2.png').convert_alpha()
        self.background_day_2_flipped = pygame.transform.flip(self.background_day_2, True, False).convert_alpha()
        self.background_day_3 = pygame.image.load('./textures/desert_day/desert_day_background_3.png').convert_alpha()
        self.background_day_3_flipped = pygame.transform.flip(self.background_day_3, True, False).convert_alpha()
        self.background_day_4 = pygame.image.load('./textures/desert_day/desert_day_background_4.png').convert_alpha()
        self.background_day_4_flipped = pygame.transform.flip(self.background_day_4, True, False).convert_alpha()

        self.background_night = pygame.image.load(
            './textures/desert_night/desert_night_background.png').convert_alpha()
        self.background_night_flipped = pygame.transform.flip(self.background_night, True, False).convert_alpha()
        self.background_night_2 = pygame.image.load(
            './textures/desert_night/desert_night_background_2.png').convert_alpha()
        self.background_night_2_flipped = pygame.transform.flip(self.background_night_2, True, False).convert_alpha()
        self.background_night_3 = pygame.image.load(
            './textures/desert_night/desert_night_background_3.png').convert_alpha()
        self.background_night_3_flipped = pygame.transform.flip(self.background_night_3, True, False).convert_alpha()
        self.background_night_4 = pygame.image.load(
            './textures/desert_night/desert_night_background_4.png').convert_alpha()
        self.background_night_4_flipped = pygame.transform.flip(self.background_night_4, True, False).convert_alpha()

        self.game_over_image = pygame.image.load('./textures/texts/game_over.png')

        self.background_flip = True
        self.background_flip_2 = True
        self.background_flip_3 = True
        self.background_flip_4 = True
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        self.background_x_4 = 0

        self.progress_birds = 0
        self.birds_score = 5000
        self.progress_day = 0
        self.day_score = 5600
        self.progress_sky = 0
        self.sky_score = 10000
        self.progress_smoothed = 0

        self.night_to_day_transition = False
        self.night_to_day_transition_progress = 0
        self.night_to_day_transition_speed = 0.02
        logging.info("Prepared game")

    def hard_reset(self):
        self.running = True
        self.pause = True
        self.game_over = False
        self.score = 0
        self.obstacle_speed = self.original_obstacle_speed
        from dino import Dino
        self.dino = Dino()
        self.obstacles.clear()
        self.power_ups.clear()
        self.fireballs.clear()
        self.power_up_timer = random.randint(30 * 60, 45 * 60)
        self.power_up_timer = -self.power_up_timer
        self.power_up_type = None
        self.power_up_spacing = 0
        self.accounts = {}
        self.load_scores()
        self.high_score = 0
        self.username = ""
        self.password = ""
        self.hashed_password = ""
        self.username_existing = False
        self.checked_username = False
        self.unlocked_user = False
        self.show_list = False
        self.high_score_list_y = 0
        self.target_high_score_list_y = 0
        self.spacing = 0
        self.press_to_return = 0

        self.background_flip = True
        self.background_flip_2 = True
        self.background_flip_3 = True
        self.background_flip_4 = True
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        self.background_x_4 = 0

        self.game_over_scale = 1
        self.game_over_time = 0
        self.game_over_fade_in = 0

        self.progress_birds = 0
        self.birds_score = 5000
        self.progress_day = 0
        self.day_score = 5600
        self.progress_sky = 0
        self.sky_score = 10000
        self.progress_smoothed = 0

        self.night_to_day_transition = False
        self.night_to_day_transition_progress = 0
        self.night_to_day_transition_speed = 0.01
        logging.info("Cache cleared and game was reset and prepared")

    def reset(self):
        self.running = True
        self.pause = False
        self.game_over = False
        self.score = 0
        self.obstacle_speed = self.original_obstacle_speed
        from dino import Dino
        self.dino = Dino()
        self.obstacles.clear()
        self.power_ups.clear()
        self.fireballs.clear()
        self.power_up_timer = random.randint(30 * 60, 45 * 60)
        self.power_up_timer = -self.power_up_timer
        self.power_up_type = None
        self.power_up_spacing = 0
        self.spacing = 0
        self.press_to_return = 0

        self.background_flip = True
        self.background_flip_2 = True
        self.background_flip_3 = True
        self.background_flip_4 = True
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        self.background_x_4 = 0

        self.game_over_scale = 1
        self.game_over_time = 0
        self.game_over_fade_in = 0

        self.high_score_list_y = 0
        self.target_high_score_list_y = 0

        self.progress_birds = 0
        self.birds_score = 5000
        self.progress_day = 0
        self.day_score = 5600
        self.progress_sky = 0
        self.sky_score = 10000
        self.progress_smoothed = 0

        self.night_to_day_transition = False
        self.night_to_day_transition_progress = 0
        self.night_to_day_transition_speed = 0.01
        logging.info("Game was reset and prepared")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.save_scores()
                logging.info("Exit")

            if event.type == pygame.MOUSEBUTTONDOWN and self.show_list:
                if event.button == 4 and self.target_high_score_list_y <= -40:
                    self.target_high_score_list_y += 40
                    logging.debug("Mouse scrolled up")
                elif event.button == 5 and self.target_high_score_list_y >= len(self.accounts)*-50 + 120 + SCREEN_HEIGHT//1.5:
                    self.target_high_score_list_y -= 40
                    logging.debug("Mouse scrolled down")

            if event.type == pygame.KEYDOWN:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    if event.key == pygame.K_1:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 1
                        logging.debug(f"Obstacle jump: 1")
                    if event.key == pygame.K_2:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 2
                        logging.debug(f"Obstacle jump: 2")
                    if event.key == pygame.K_3:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 5
                        logging.debug(f"Obstacle jump: 5")
                    if event.key == pygame.K_4:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 10
                        logging.debug(f"Obstacle jump: 10")
                    if event.key == pygame.K_5:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 20
                        logging.debug(f"Obstacle jump: 20")
                    if event.key == pygame.K_6:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 50
                        logging.debug(f"Obstacle jump: 50")
                    if event.key == pygame.K_7:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 100
                        logging.debug(f"Obstacle jump: 100")
                    if event.key == pygame.K_8:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 200
                        logging.debug(f"Obstacle jump: 200")
                    if event.key == pygame.K_9:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 500
                        logging.debug(f"Obstacle jump: 500")
                if event.key == pygame.K_ESCAPE:
                    if self.show_list:
                        self.show_list = False
                        logging.info(f"Toggle high score list")
                        return
                    self.running = False if self.game_over or self.pause else True
                    self.pause = not self.pause
                    if not self.running:
                        self.save_scores()
                        logging.info("Exit")
                    else:
                        logging.info("Paused")

                if event.key == pygame.K_F1:
                    self.show_list = not self.show_list
                    logging.info(f"Toggle high score list")
                    return

                if event.key == pygame.K_BACKSPACE and self.game_over and self.username_existing or event.key == pygame.K_BACKSPACE and self.pause and self.username_existing and self.password.strip() == "" or event.key == pygame.K_BACKSPACE and self.pause and self.unlocked_user:
                    if not self.unlocked_user and self.username_existing:
                        if self.press_to_return >= 5:
                            self.hard_reset()
                            logging.info("Reset")
                        self.press_to_return += 1
                        return

                    self.hard_reset()
                    logging.info("Reset")

                if event.key == pygame.K_RETURN and self.game_over or event.key == pygame.K_RETURN and self.pause and self.unlocked_user:
                    self.save_scores()
                    self.reset()
                    logging.info("Reset Score")

                if event.key == pygame.K_SPACE:
                    if self.pause and self.username_existing and self.checked_username and self.unlocked_user:
                        self.pause = False
                        logging.info("Resumed")
                    elif self.game_over:
                        if self.game_over_fade_in >= 1:
                            self.reset()
                            logging.info("Reset Score")
                    else:
                        logging.debug("Jump")
                        if self.dino.y > 50:
                            self.dino.start_jump(self.power_up_type)

                if event.key == pygame.K_RETURN and not self.pause and self.power_up_type == "fireball" and len(self.fireballs) < 5:
                    self.fireballs.append(Fireball(self.dino.y))
                    logging.debug("Fireball spawned")

                if not self.username_existing:
                    if event.key == pygame.K_RETURN and self.username.strip() != "":
                        self.username_existing = True
                        logging.info(f"Got username: {self.username}")
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                        logging.debug("Backspace")
                    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                        self.username += event.unicode
                        logging.debug(f"Key pressed: {event.key}")
                    self.cursor_tick = 0

                if self.username_existing and not self.checked_username:
                    if event.key == pygame.K_RETURN and self.password.strip() != "":
                        logging.info(f"Got password: {self.password}")
                        self.unlock_user()
                    elif event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                        logging.debug("Backspace")
                    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                        self.password += event.unicode
                        logging.debug(f"Key pressed: {event.key}")
                        self.press_to_return = 0
                    self.cursor_tick = 0

    def update(self):
        self.cursor_tick += 1
        if self.cursor_tick >= 60:
            self.cursor_tick = 0

        if self.username_existing and not self.checked_username and not self.unlocked_user:
            self.check_username()
        if self.username_existing and self.checked_username and not self.unlocked_user:
            self.unlock_user()

        if self.show_list:
            self.pause = True
            step = (self.target_high_score_list_y - self.high_score_list_y) * 0.2
            if abs(step) > 0.5:
                self.high_score_list_y += step

        if self.pause or self.game_over:
            return

        self.dino.update(self.score)

        if not self.pause and not self.game_over:
            self.background_x -= self.obstacle_speed * 0.20
            if self.background_x <= -SCREEN_WIDTH - 800:
                self.background_x = 0
                self.background_flip = not self.background_flip
            self.background_x_2 -= self.obstacle_speed * 0.25
            if self.background_x_2 <= -SCREEN_WIDTH - 800:
                self.background_x_2 = 0
                self.background_flip_2 = not self.background_flip_2
            self.background_x_3 -= self.obstacle_speed * 0.50
            if self.background_x_3 <= -SCREEN_WIDTH - 800:
                self.background_x_3 = 0
                self.background_flip_3 = not self.background_flip_3
            self.background_x_4 -= self.obstacle_speed
            if self.background_x_4 <= -SCREEN_WIDTH - 800:
                self.background_x_4 = 0
                self.background_flip_4 = not self.background_flip_4

            self.progress_birds = min((self.score + self.progress_smoothed) / self.birds_score, 1)
            self.progress_day = min((self.score + self.progress_smoothed) / self.day_score, 1)
            self.progress_sky = min((self.score + self.progress_smoothed) / self.sky_score, 1)
            if self.score < 100:
                self.progress_smoothed = self.progress_smoothed + 0.5
            else:
                self.progress_smoothed = self.progress_smoothed + 0.9

        if not self.obstacles or self.obstacles[-1].x < SCREEN_WIDTH - random.randint(650, 850) - self.spacing:
            self.spacing += 2.5
            self.obstacles.append(Obstacle(self.score))
            logging.debug(f"Placed new obstacle")

        if -300 >= self.background_x:
            self.night_to_day_transition = True

        if self.background_x <= -500 and (self.night_to_day_transition_progress == 1 or self.night_to_day_transition_progress == 0) :
            self.night_to_day_transition = False

        if self.night_to_day_transition:
            if 5000 <= self.score <= 7000:
                self.night_to_day_transition_progress = min(
                    self.night_to_day_transition_progress + self.night_to_day_transition_speed, 1)

        for fireball in self.fireballs[:]:
            fireball.update()
            if fireball.complete_off_screen():
                logging.debug(f"Fireball complete off screen: {fireball.x + fireball.width < 0}")
                self.fireballs.remove(fireball)
                logging.debug("Removed fireball")

        for obstacle in self.obstacles[:]:
            obstacle.update(self.obstacle_speed)

            for fireball in self.fireballs[:]:
                if fireball.collides_with(obstacle):
                    logging.debug("Obstacle collided with fireball")
                    self.score += 100
                    self.obstacles.remove(obstacle)
                    self.fireballs.remove(fireball)
                    logging.debug("Removed obstacle")

            if obstacle.complete_off_screen():
                logging.debug(f"Obstacle complete off screen: {obstacle.x + obstacle.width[0] < 0}")
                self.obstacles.remove(obstacle)
                logging.debug("Removed obstacle")

            if obstacle.off_screen() and not obstacle.got_counted:
                logging.debug(f"Obstacle off screen: {obstacle.x + obstacle.width[0] < 0}")
                multiplicator = 2 if self.power_up_type == "multiplicator" else 1
                if obstacle.type == "double":
                    self.score += 150 * multiplicator
                else:
                    self.score += 100 * multiplicator
                obstacle.got_counted = True
                self.progress_smoothed = 0

                logging.info(f"Score: {self.score}")

            if obstacle.collides_with(self.dino) and not self.power_up_type == "immortality":
                logging.info("Dino collided with obstacle")
                self.save_scores()
                self.game_over = True

            self.obstacle_speed += SPEED_INCREMENT

        if not self.obstacles or self.obstacles[-1].x <= SCREEN_WIDTH - 400:
            self.power_up_spacing = True
        else:
            self.power_up_spacing = False

        if self.power_up_timer < 0:
            self.power_up_timer += 1

        if self.power_up_timer >= 0 and self.power_up_spacing and self.power_up_type is None:
            logging.debug(f"Placed new power up ({self.power_up_timer})")
            self.power_ups.append(PowerUp(self.score))
            self.power_up_timer = random.randint(30 * 60, 45 * 60)
            self.power_up_timer = -self.power_up_timer

        for power_up in self.power_ups[:]:
            power_up.update(self.obstacle_speed)
            if power_up.complete_off_screen():
                logging.debug(f"Power up complete off screen: {power_up.x + power_up.width < 0}")
                self.power_ups.remove(power_up)
                self.power_up_timer = random.randint(30 * 60, 45 * 60)
                self.power_up_timer = -self.power_up_timer
                logging.debug("Removed power up")

            if power_up.collides_with(self.dino) and self.power_up_type is None:
                logging.debug("Dino collided with power up")
                if power_up.type == "multiplicator":
                    self.power_up_type = "multiplicator"
                    logging.info(f"Multiplicator power up")
                elif power_up.type == "immortality":
                    self.power_up_type = "immortality"
                    logging.info("Immortality power up")
                elif power_up.type == "fly":
                    self.power_up_type = "fly"
                    logging.info("Fly power up")
                elif power_up.type == "fireball":
                    self.power_up_type = "fireball"
                    logging.info("Fireball power up")
                self.power_ups.remove(power_up)
                self.power_up_timer = 0
                logging.debug("Removed power up")

        if self.power_up_type is not None and self.power_up_timer >= 0:
            self.power_up_timer += 1
            if self.power_up_timer > 15 * 60:
                self.power_up_timer = random.randint(30 * 60, 45 * 60)
                self.power_up_timer = -self.power_up_timer
                self.power_up_type = None
                logging.debug("Power up completed")

    def draw(self):
        if not self.background_flip:
            screen.blit(self.background_night_flipped, (self.background_x, 0))
            screen.blit(self.background_night, (self.background_x + SCREEN_WIDTH + 800, 0))
        else:
             screen.blit(self.background_night, (self.background_x, 0))
             screen.blit(self.background_night_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

        if not self.background_flip_2:
            screen.blit(self.background_night_2_flipped, (self.background_x_2, 410))
            screen.blit(self.background_night_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
        else:
            screen.blit(self.background_night_2, (self.background_x_2, 410))
            screen.blit(self.background_night_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

        if not self.background_flip_3:
            screen.blit(self.background_night_3_flipped, (self.background_x_3, 500))
            screen.blit(self.background_night_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
        else:
            screen.blit(self.background_night_3, (self.background_x_3, 500))
            screen.blit(self.background_night_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))


        if not self.background_flip_4:
            screen.blit(self.background_night_4_flipped, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_night_4, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))
        else:
            screen.blit(self.background_night_4, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_night_4_flipped, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))

        self.background_day.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip:
            screen.blit(self.background_day_flipped, (self.background_x, 0))
            screen.blit(self.background_day, (self.background_x + SCREEN_WIDTH + 800, 0))
        else:
            screen.blit(self.background_day, (self.background_x, 0))
            screen.blit(self.background_day_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

        self.background_day_2.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_2_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip_2:
            screen.blit(self.background_day_2_flipped, (self.background_x_2, 410))
            screen.blit(self.background_day_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
        else:
            screen.blit(self.background_day_2, (self.background_x_2, 410))
            screen.blit(self.background_day_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

        self.background_day_3.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_3_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip_3:
            screen.blit(self.background_day_3_flipped, (self.background_x_3, 500))
            screen.blit(self.background_day_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
        else:
            screen.blit(self.background_day_3, (self.background_x_3, 500))
            screen.blit(self.background_day_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))

        self.background_day_4.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_4_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip_4:
            screen.blit(self.background_day_4_flipped, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_day_4, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))
        else:
            screen.blit(self.background_day_4, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_day_4_flipped, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))

        if logging.root.level == logging.DEBUG:
            pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 2)

        for obstacle in self.obstacles:
            obstacle.draw()

        for power_up in self.power_ups:
            power_up.draw()

        for fireball in self.fireballs:
            fireball.draw()
        self.dino.draw()

        color = WHITE if self.pause or self.game_over else BLACK

        if self.game_over:
            self.game_over_fade_in += 0.01
            rect_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            rect_surface.set_alpha(self.game_over_fade_in * 255)
            rect_surface.fill(BLACK)
            screen.blit(rect_surface, (0, 0))

            self.game_over_time += clock.get_time() / 500.0
            progress = min(self.game_over_time / 8.0, 1.0)
            scale_eased = ease_out_cubic(progress)
            opacity_eased = ease_out_sine(progress)

            self.game_over_scale = 1 + scale_eased * 8
            opacity = int(255 * opacity_eased)

            original_width = self.game_over_image.get_width()
            original_height = self.game_over_image.get_height()
            aspect_ratio = original_width / original_height
            scaled_height = int(70 * self.game_over_scale)
            scaled_width = int(scaled_height * aspect_ratio)

            game_over_screen = pygame.transform.scale(self.game_over_image, (min(scaled_width,1100), min(scaled_height, 600)))
            game_over_screen.set_alpha(opacity)
            screen.blit(game_over_screen, game_over_screen.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            if scaled_width > 1100:
                self.blend_in_time += clock.get_time() / 500.0
                progress_text = min(self.blend_in_time / 4.0, 1.0)
                opacity_eased_text = ease_out_sine(progress_text)
                opacity_text = int(255 * opacity_eased_text)
                text_color = (255, 255, 255, opacity_text)

                restart_text = font.render("Press space or enter to try again", True, text_color)
                escape_text = font.render("Press escape to exit", True, text_color)
                change_account_text = font.render("Press backspace to change account", True, text_color)

                restart_text.set_alpha(opacity_text)
                escape_text.set_alpha(opacity_text)
                change_account_text.set_alpha(opacity_text)
                screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 230)))
                screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 280)))
                screen.blit(change_account_text, change_account_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 330)))

        if self.pause:
            screen.fill(BLACK)
            pause_text = font.render("Paused", True, WHITE)
            continue_text = font.render("Press space to continue", True, WHITE)
            escape_text = font.render("Press escape to exit", True, WHITE)
            restart_text = font.render("Press enter to start from beginning", True, WHITE)
            hard_restart_text = font.render("Press backspace to change account", True, WHITE)
            high_score_text = font.render("Press F1 to see highscores", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
            screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(hard_restart_text, hard_restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
            screen.blit(high_score_text, high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)))

        score_text = font.render(f"Score: {self.score}", True, color)
        screen.blit(score_text, (10, 10))
        username_text = font.render(f"User: {self.username}", True, color)
        screen.blit(username_text, (10, 35))
        highest_score_text = font.render(f"High Score: {max(self.score, self.high_score)}", True, color)
        screen.blit(highest_score_text, (10, 60))
        if self.power_up_type is not None:
            power_up_text = font.render(f"Power Up: {self.power_up_type}", True, color)
            screen.blit(power_up_text, (10, 85))
            rect_surface = pygame.Surface((SCREEN_WIDTH // 4, 30), pygame.SRCALPHA)
            rect_surface.set_alpha(128)
            rect_surface.fill(WHITE)
            screen.blit(rect_surface, (10, 120))

            pygame.draw.rect(screen, BLACK,
                             (10, 120, (1-(self.power_up_timer/(60*15))) * SCREEN_WIDTH // 4, 30))
            pygame.draw.rect(screen, WHITE, (10, 120, SCREEN_WIDTH // 4, 30), 2)

        if not self.pause and not self.game_over:
            rect_surface = pygame.Surface((SCREEN_WIDTH // 2, 50), pygame.SRCALPHA)
            rect_surface.set_alpha(128)
            rect_surface.fill(WHITE)
            screen.blit(rect_surface, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10))

            pygame.draw.rect(screen, BROWN,
                             (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_birds * SCREEN_WIDTH // 2, 50))
            pygame.draw.rect(screen, BLUE,
                             (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_day * SCREEN_WIDTH // 2, 50))
            pygame.draw.rect(screen, LIGHT_BLUE,
                             (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_sky * SCREEN_WIDTH // 2, 50))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, SCREEN_WIDTH // 2, 50), 2)


        if self.cursor_tick < 30:
            cursor = "|"
        else:
            cursor = " "

        if not self.username_existing and not self.unlocked_user and not self.checked_username:
            screen.fill(BLACK)

            pause_text = font.render("Enter your username!", True, WHITE)
            username_text = font.render(f"Username: {self.username}{cursor}", True, WHITE)
            enter_text = font.render("Press enter to confirm", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            screen.blit(username_text, username_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

        if not self.unlocked_user and self.username_existing:
            screen.fill(BLACK)
            password = ""
            for i in range(len(self.password)):
                password += "*"

            if self.username in self.accounts:
                pause_text = font.render("User exists already!", True, WHITE)
            else:
                pause_text = font.render("Creating new account!", True, WHITE)
            info_text = font.render("Enter password to proceed", True, WHITE)
            password_text = font.render(f"Password: {password}{cursor}", True, WHITE)
            enter_text = font.render("Press enter to confirm", True, WHITE)
            restart_text = font.render("Press backspace to use another account", True, WHITE)
            return_text = font.render(f"Press 5 times to return: 5/{self.press_to_return}", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
            screen.blit(info_text, info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            screen.blit(password_text, password_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
            screen.blit(return_text, return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)))

        if self.show_list:
            screen.fill(BLACK)
            header_text = pygame.font.Font(None, 48).render("All highscores", True, WHITE)
            screen.blit(header_text, header_text.get_rect(center=(SCREEN_WIDTH // 2, 50 + self.high_score_list_y)))
            accounts = sorted(self.accounts.items(), key=lambda x: x[1]["score"], reverse=True)
            for account, (username, score) in enumerate(accounts):
                prefix = "👑 " if account <= 2 else ""
                colors = {2: BRONZE, 1: SILVER, 0: GOLD}
                color = colors.get(account, WHITE)
                score_text = font.render(f"{prefix}{username}: {score['score']}", True, color)
                screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, account * 50 + 120 + self.high_score_list_y)))

        if self.show_fps:
            fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, color)
            screen.blit(fps_text, (SCREEN_WIDTH - 110, 10))

        pygame.display.flip()

    def save_scores(self):
        if self.username == "":
            return
        scores = self.accounts
        if not self.username in scores:
            scores[self.username] = {
                "score": self.score,
                "password": self.hashed_password
            }
            logging.info(f"Created new account: {self.username}")
        elif self.score > scores[self.username]["score"]:
            scores[self.username]["score"] = self.score
            scores[self.username]["password"] = self.hashed_password

        if not self.username in scores or self.score > self.high_score:
            with open("./saves/highscores.json", "w") as file:
                json.dump(scores, file, indent=4)
            logging.info(f"Saved highscore: {self.score} for user: {self.username}")
            self.high_score = self.score
        else:
            logging.info(f"No new highscore: user: {self.username}")

    def load_scores(self):
        if os.path.exists("./saves/highscores.json"):
            with open("./saves/highscores.json", "r") as file:
                self.accounts = json.load(file)
            logging.info(f"Loaded all accounts")
        else:
            logging.info("No accounts found")

    def check_username(self):
        if self.username in self.accounts:
            self.unlocked_user = False

    def unlock_user(self):
        self.create_password()

        if self.username in self.accounts:
            if self.hashed_password == self.accounts[self.username]["password"]:
                self.high_score = self.accounts[self.username]["score"]
                logging.info(f"Loaded highscore ({self.high_score}) for user ({self.username}) out of storage")
            else:
                logging.info("Wrong password")

                screen.fill(BLACK)
                enter_text = font.render("Wrong password!", True, RED)
                screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

                pygame.display.flip()
                clock.tick(1)
                self.hard_reset()
                clock.tick(FRAME_RATE)
                return
        self.pause = False
        self.checked_username = True
        self.unlocked_user = True
        logging.info(f"Started game")

    def create_password(self):
        self.hashed_password = hashlib.sha512(self.password.encode('utf-8')).hexdigest()
        logging.debug(f"Hashed password: {self.hashed_password}")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(self.fps)
        pygame.quit()