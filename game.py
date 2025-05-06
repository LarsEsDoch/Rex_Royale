import random
import hashlib
import os
import json

from config import SCREEN_WIDTH, BLACK, SPEED_INCREMENT, \
    GROUND_LEVEL, OBSTACLE_SPEED, WHITE, RED, FRAME_RATE, \
    SCREEN_HEIGHT
from utils import ease_out_sine, ease_out_cubic
from resources import screen, clock, font, pygame
from dino import Dino
from obstacle import Obstacle
from resources import logging

class Game:

    def __init__(self):
        self.running = True
        self.pause = True
        self.game_over = False
        self.score = 0
        self.obstacle_speed = OBSTACLE_SPEED
        self.dino = Dino()
        self.obstacles = []
        self.accounts = {}
        self.load_scores()
        self.high_score = 0
        self.username = ""
        self.password = ""
        self.hashed_password = ""
        self.username_existing = False
        self.checked_username = False
        self.unlocked_user = False
        self.spacing = 0
        self.cursor_tick = 0
        self.game_over_scale = 1
        self.game_over_time = 0
        self.blend_in_time = 0

        self.background_day = pygame.image.load('textures/desert_day/desert_day_background.png')
        self.background_day_flipped = pygame.transform.flip(self.background_day, True, False)
        self.background_day_2 = pygame.image.load('textures/desert_day/desert_day_background_2.png')
        self.background_day_2_flipped = pygame.transform.flip(self.background_day_2, True, False)
        self.background_day_3 = pygame.image.load('textures/desert_day/desert_day_background_3.png')
        self.background_day_3_flipped = pygame.transform.flip(self.background_day_3, True, False)
        self.background_day_4 = pygame.image.load('textures/desert_day/desert_day_background_4.png')
        self.background_day_4_flipped = pygame.transform.flip(self.background_day_4, True, False)

        self.background_night = pygame.image.load('textures/desert_night/desert_night_background.png')
        self.background_night_flipped = pygame.transform.flip(self.background_night, True, False)
        self.background_night_2 = pygame.image.load('textures/desert_night/desert_night_background_2.png')
        self.background_night_2_flipped = pygame.transform.flip(self.background_night_2, True, False)
        self.background_night_3 = pygame.image.load('textures/desert_night/desert_night_background_3.png')
        self.background_night_3_flipped = pygame.transform.flip(self.background_night_3, True, False)
        self.background_night_4 = pygame.image.load('textures/desert_night/desert_night_background_4.png')
        self.background_night_4_flipped = pygame.transform.flip(self.background_night_4, True, False)

        self.game_over_image = pygame.image.load('textures/texts/game_over.png')

        self.background_flip = True
        self.background_flip_2 = True
        self.background_flip_3 = True
        self.background_flip_4 = True
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        self.background_x_4 = 0

        self.transition = False
        self.day_to_night_transition_progress = 0
        self.transition_speed = 0.02
        logging.info("Prepared game")

    def hard_reset(self):
        self.running = True
        self.pause = True
        self.game_over = False
        self.score = 0
        self.obstacle_speed = OBSTACLE_SPEED
        self.dino = Dino()
        self.obstacles.clear()
        self.accounts = {}
        self.load_scores()
        self.high_score = 0
        self.username = ""
        self.password = ""
        self.hashed_password = ""
        self.username_existing = False
        self.checked_username = False
        self.unlocked_user = False
        self.spacing = 0
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

        self.transition = False
        self.day_to_night_transition_progress = 0
        self.transition_speed = 0.01
        logging.info("Cache cleared and game was reset and prepared")

    def reset(self):
        self.running = True
        self.pause = False
        self.game_over = False
        self.score = 0
        self.obstacle_speed = OBSTACLE_SPEED
        self.dino = Dino()
        self.obstacles.clear()
        self.spacing = 0
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

        self.transition = False
        self.day_to_night_transition_progress = 0
        self.transition_speed = 0.01
        logging.info("Game was reset and prepared")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.save_scores()
                logging.info("Exit")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False if self.game_over or self.pause else True
                    self.pause = not self.pause
                    if not self.running:
                        self.save_scores()
                        logging.info("Exit")
                    else:
                        logging.info("Paused")

                if event.key == pygame.K_BACKSPACE and self.game_over and self.username_existing or event.key == pygame.K_BACKSPACE and self.pause and self.username_existing:
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
                        self.reset()
                        logging.info("Reset Score")
                    else:
                        self.dino.start_jump()

                if not self.username_existing:
                    if event.key == pygame.K_RETURN and self.username.strip() != "":
                        self.username_existing = True
                        logging.info(f"Got username: {self.username}")
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                        self.username += event.unicode
                    self.cursor_tick = 0

                if self.username_existing and not self.checked_username:
                    if event.key == pygame.K_RETURN and self.password.strip() != "":
                        logging.info(f"Got password: {self.password}")
                        self.unlock_user()

                    elif event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                        self.password += event.unicode
                    self.cursor_tick = 0

    def update(self):
        self.cursor_tick += 1
        if self.cursor_tick >= 60:
            self.cursor_tick = 0

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

        if not self.obstacles or self.obstacles[-1].x < SCREEN_WIDTH - random.randint(600, 800) - self.spacing:
            self.spacing += 2
            self.obstacles.append(Obstacle(self.score))

        if -300 >= self.background_x:
            self.transition = True

        if self.background_x <= -500 and (self.day_to_night_transition_progress == 1 or self.day_to_night_transition_progress == 0) :
            self.transition = False

        if self.transition:
            if 5000 <= self.score <= 7000:
                self.day_to_night_transition_progress = min(
                    self.day_to_night_transition_progress + self.transition_speed, 1)
            if self.score >= 10000:
                self.day_to_night_transition_progress = max(
                    self.day_to_night_transition_progress - self.transition_speed, 0)


        for obstacle in self.obstacles[:]:
            obstacle.update(self.obstacle_speed)

            if obstacle.complete_off_screen():
                self.obstacles.remove(obstacle)

            if obstacle.off_screen() and not obstacle.got_counted:
                obstacle.got_counted = True
                self.score += 100

                logging.info(f"Score: {self.score}")

            if obstacle.collides_with(self.dino):
                logging.info("Dino collided")

                self.save_scores()
                self.game_over = True

            self.obstacle_speed += SPEED_INCREMENT

    def draw(self):
        screen.fill(BLACK)

        if not self.background_flip:
            screen.blit(self.background_day_flipped, (self.background_x, 0))
            screen.blit(self.background_day, (self.background_x + SCREEN_WIDTH + 800, 0))
        else:
            screen.blit(self.background_day, (self.background_x, 0))
            screen.blit(self.background_day_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

        if not self.background_flip_2:
            screen.blit(self.background_day_2_flipped, (self.background_x_2, 410))
            screen.blit(self.background_day_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
        else:
            screen.blit(self.background_day_2, (self.background_x_2, 410))
            screen.blit(self.background_day_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

        if not self.background_flip_3:
            screen.blit(self.background_day_3_flipped, (self.background_x_3, 500))
            screen.blit(self.background_day_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
        else:
            screen.blit(self.background_day_3, (self.background_x_3, 500))
            screen.blit(self.background_day_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))

        if not self.background_flip_4:
            screen.blit(self.background_day_4_flipped, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_day_4, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))
        else:
            screen.blit(self.background_day_4, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_day_4_flipped, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))

        self.background_night.set_alpha(int(self.day_to_night_transition_progress * 255))
        self.background_night_flipped.set_alpha(int(self.day_to_night_transition_progress * 255))
        if not self.background_flip:
            screen.blit(self.background_night_flipped, (self.background_x, 0))
            screen.blit(self.background_night, (self.background_x + SCREEN_WIDTH + 800, 0))
        else:
            screen.blit(self.background_night, (self.background_x, 0))
            screen.blit(self.background_night_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

        self.background_night_2.set_alpha(int(self.day_to_night_transition_progress * 255))
        self.background_night_2_flipped.set_alpha(int(self.day_to_night_transition_progress * 255))
        if not self.background_flip_2:
            screen.blit(self.background_night_2_flipped, (self.background_x_2, 410))
            screen.blit(self.background_night_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
        else:
            screen.blit(self.background_night_2, (self.background_x_2, 410))
            screen.blit(self.background_night_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

        self.background_night_3.set_alpha(int(self.day_to_night_transition_progress * 255))
        self.background_night_3_flipped.set_alpha(int(self.day_to_night_transition_progress * 255))
        if not self.background_flip_3:
            screen.blit(self.background_night_3_flipped, (self.background_x_3, 500))
            screen.blit(self.background_night_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
        else:
            screen.blit(self.background_night_3, (self.background_x_3, 500))
            screen.blit(self.background_night_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))

        self.background_night_4.set_alpha(int(self.day_to_night_transition_progress * 255))
        self.background_night_4_flipped.set_alpha(int(self.day_to_night_transition_progress * 255))
        if not self.background_flip_4:
            screen.blit(self.background_night_4_flipped, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_night_4, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))
        else:
            screen.blit(self.background_night_4, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_night_4_flipped, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))

        for obstacle in self.obstacles:
            obstacle.draw()

        self.dino.draw()

        color = WHITE if self.pause or self.game_over else BLACK

        if self.game_over:
            screen.fill(BLACK)

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
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
            screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)))
            screen.blit(hard_restart_text, hard_restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)))

        score_text = font.render(f"Score: {self.score}", True, color)
        screen.blit(score_text, (10, 10))
        username_text = font.render(f"User: {self.username}", True, color)
        screen.blit(username_text, (10, 35))
        highest_score_text = font.render(f"High Score: {max(self.score, self.high_score)}", True, color)
        screen.blit(highest_score_text, (10, 60))

        if self.cursor_tick < 30:
            cursor = "|"
        else:
            cursor = " "

        if not self.username_existing and not self.unlocked_user and not self.checked_username:
            screen.fill(BLACK)

            pause_text = font.render("Enter your username!", True, WHITE)
            username_text = font.render(f"Username: {self.username}{cursor}", True, WHITE)
            enter_text = font.render("Press enter to confirm", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(username_text, username_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        if not self.unlocked_user and self.username_existing:
            screen.fill(BLACK)

            if self.username in self.accounts:
                pause_text = font.render("User exists already!", True, WHITE)
            else:
                pause_text = font.render("Creating new account!", True, WHITE)
            info_text = font.render("Enter password to proceed", True, WHITE)
            password_text = font.render(f"Password: {self.password}{cursor}", True, WHITE)
            enter_text = font.render("Press enter to confirm", True, WHITE)
            restart_text = font.render("Press backspace to use another account", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(info_text, info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(password_text, password_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
            screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)))
            screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)))


        if self.username_existing and not self.checked_username and not self.unlocked_user:
            self.check_username()
        if self.username_existing and self.checked_username and not self.unlocked_user:
            self.unlock_user()

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
        elif self.score > scores[self.username]["score"]:
            scores[self.username]["score"] = self.score
            scores[self.username]["password"] = self.hashed_password

        if not self.username in scores or self.score > self.high_score:
            with open("highscores.json", "w") as file:
                json.dump(scores, file, indent=4)
            logging.info(f"Saved highscore: {self.score} for user: {self.username}")
        else:
            logging.info(f"No new highscore: user: {self.username}")

    def load_scores(self):
        if os.path.exists("highscores.json"):
            with open("highscores.json", "r") as file:
                self.accounts = json.load(file)

        logging.info(f"Loaded all accounts")

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

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FRAME_RATE)
        pygame.quit()