import random
import hashlib
import os
import json

from . import handleEvents
from . import update
from . import draw
from ..config import SCREEN_WIDTH, BLACK, OBSTACLE_SPEED, RED, FRAME_RATE, SCREEN_HEIGHT
from ..resources import screen, clock, font, pygame
from ..resources import logging

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
        from ..dino import Dino
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

    def reset(self):
        self.running = True
        self.pause = False
        self.game_over = False
        self.score = 0
        self.obstacle_speed = self.original_obstacle_speed
        from ..dino import Dino
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

    def accounts_reset(self):
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
        self.pause = True
        logging.info("Accounts were reset")

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
                self.reset()
                self.accounts_reset()
                clock.tick(self.fps)
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
            handleEvents.handleEvents(self)
            update.update(self)
            draw.draw(self)
            clock.tick(self.fps)
        pygame.quit()