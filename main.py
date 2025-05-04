import pygame
import random
import os
import json
import hashlib

pygame.init()
print("Initialized pygame successful")

BIRD_FRAMES = []
for i in range(17):
    frame_path = f"textures/bird/frame_{i+1}.png"
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (130, 115))
    BIRD_FRAMES.append(image)
CACTUS_SMALL = []
for i in range(3):
    frame_path = f"textures/cactus_small/cactus_small_{i+1}.png"
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (60, 70))
    CACTUS_SMALL.append(image)
CACTUS_LARGE = []
for i in range(3):
    frame_path = f"textures/cactus_large/cactus_large_{i+1}.png"
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, (40, 130))
    CACTUS_LARGE.append(image)
print("Loaded textures")

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")
print("Set screen dimensions")


clock = pygame.time.Clock()
print("Initialized clock")

WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
print("Initialized colors")

GRAVITY = 0.5
GROUND_LEVEL = SCREEN_HEIGHT - 50
OBSTACLE_SPEED = 7
SPEED_INCREMENT = 0.001
FRAME_RATE = 60
print("Initialized game constants")

font = pygame.font.Font(None, 36)
print("Set font")

def ease_out_cubic(t):
    return 1 - (1 - t)**3

def ease_out_sine(t):
    from math import sin, pi
    return sin((t * pi) / 2)
print("Initialized math functions")

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
        self.image = pygame.image.load('textures/dino_texture.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.gravity_multiplier = 1.1

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
        self.velocity_y = -16
        if self.y >= GROUND_LEVEL - self.height - 50:
            self.velocity_y = -16
        if not self.jump:
            self.jump = True
            self.velocity_y = -16


class Obstacle:

    def __init__(self, score):
        self.frame_images = []
        if score < 5000:
            self.type = random.choice(["small", "large"])
        else:
            self.type = random.choice(["small", "large", "bird"])

        self.width, self.height = (60, 70) if self.type == "small" else (40, 130) if self.type == "large" else (130, 115)

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

        self.y = GROUND_LEVEL - self.height - 200 if self.type == "bird" else GROUND_LEVEL - self.height
        self.current_frame = 0
        self.animation_timer = 0
        self.got_counted = False

    def update(self, speed):
        if self.type == "bird":
            self.x -= speed * 1.5
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

    def off_screen(self):
        return self.x + self.width < 50

    def complete_off_screen(self):
        return self.x + self.width < -200

    def collides_with(self, dino):
        if self.type == "bird":
            return dino.x < self.x + self.width and dino.x + dino.hitbox_width > self.x and self.y < dino.y + dino.hitbox_height < self.y + self.height

        return dino.x < self.x + self.width and dino.x + dino.hitbox_width > self.x and dino.y + dino.hitbox_height > self.y


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

        self.background_day = pygame.image.load('textures/desert_day_background.png')
        self.background_day_flipped = pygame.transform.flip(self.background_day, True, False)
        self.background_day_2 = pygame.image.load('textures/desert_day_background_2.png')
        self.background_day_2_flipped = pygame.transform.flip(self.background_day_2, True, False)
        self.background_day_3 = pygame.image.load('textures/desert_day_background_3.png')
        self.background_day_3_flipped = pygame.transform.flip(self.background_day_3, True, False)

        self.background_night = pygame.image.load('textures/desert_night_background.png')
        self.background_night_flipped = pygame.transform.flip(self.background_night, True, False)

        self.game_over_image = pygame.image.load('textures/game_over.png')

        self.background_flip = True
        self.background_flip_2 = True
        self.background_flip_3 = True
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        print("Prepared game")

    def reset(self):
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
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        self.game_over_scale = 1
        self.game_over_time = 0
        print("Game was reset and prepared")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.save_scores()
                print("Exit")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False if self.game_over or self.pause else True
                    self.pause = not self.pause
                    if not self.running:
                        self.save_scores()
                        print("Exit")
                    else:
                        print("Paused")

                if event.key == pygame.K_SPACE:
                    if self.pause and self.username_existing and self.checked_username and self.unlocked_user:
                        self.pause = False
                        print("Resumed")
                    elif self.game_over:
                        self.reset()
                        print("Reset")
                    else:
                        self.dino.start_jump()

                if not self.username_existing:
                    if event.key == pygame.K_RETURN and self.username.strip() != "":
                        self.username_existing = True
                        print(f"Got username: {self.username}")
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                        self.username += event.unicode
                    self.cursor_tick = 0

                if self.username_existing and not self.checked_username:
                    if event.key == pygame.K_RETURN and self.password.strip() != "":
                        print(f"Got password: {self.password}")
                        self.unlock_user()

                    elif event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                        self.password += event.unicode
                    self.cursor_tick = 0

    def update(self):
        if self.pause or self.game_over:
            return

        self.dino.update(self.score)

        if not self.obstacles or self.obstacles[-1].x < SCREEN_WIDTH - random.randint(600, 800) - self.spacing:
            self.spacing += 2
            self.obstacles.append(Obstacle(self.score))

        for obstacle in self.obstacles[:]:
            obstacle.update(self.obstacle_speed)

            if obstacle.complete_off_screen():
                self.obstacles.remove(obstacle)

            if obstacle.off_screen() and not obstacle.got_counted:
                obstacle.got_counted = True
                self.score += 100

                print(f"Score: {self.score}")

            if obstacle.collides_with(self.dino):
                print("Dino collided")

                self.save_scores()
                self.game_over = True

            self.obstacle_speed += SPEED_INCREMENT

    def draw(self):
        if self.cursor_tick < 30:
            cursor = "|"
        else:
            cursor = " "
        self.cursor_tick += 1
        if self.cursor_tick >= 60:
            self.cursor_tick = 0


        screen.fill(BLACK)

        if not self.pause and not self.game_over:
            self.background_x -= self.obstacle_speed * 0.20
            if self.background_x <= -SCREEN_WIDTH - 800:
                self.background_x = 0
                self.background_flip = not self.background_flip
            self.background_x_2 -= self.obstacle_speed * 0.25
            if self.background_x_2 <= -SCREEN_WIDTH - 800:
                self.background_x_2 = 0
                self.background_flip_2 = not self.background_flip_2
            self.background_x_3 -= self.obstacle_speed * 0.30
            if self.background_x_3 <= -SCREEN_WIDTH - 800:
                self.background_x_3 = 0
                self.background_flip_3 = not self.background_flip_3

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
            screen.blit(self.background_day_3_flipped, (self.background_x_3, 550))
            screen.blit(self.background_day_3, (self.background_x_3 + SCREEN_WIDTH + 800, 550))
        else:
            screen.blit(self.background_day_3, (self.background_x_3, 550))
            screen.blit(self.background_day_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 550))
        self.dino.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

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

                restart_text = font.render("Press space to restart", True, text_color)
                escape_text = font.render("Press escape to exit", True, text_color)

                restart_text.set_alpha(opacity_text)
                escape_text.set_alpha(opacity_text)
                screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250)))
                screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300)))

        if self.pause:
            screen.fill(BLACK)

            pause_text = font.render("Paused", True, WHITE)
            continue_text = font.render("Press space to continue", True, WHITE)
            escape_text = font.render("Press escape to exit", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        score_text = font.render(f"Score: {self.score}", True, color)
        screen.blit(score_text, (10, 10))
        username_text = font.render(f"User: {self.username}", True, color)
        screen.blit(username_text, (10, 35))
        highest_score_text = font.render(f"High Score: {max(self.score, self.high_score)}", True, color)
        screen.blit(highest_score_text, (10, 60))

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
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(info_text, info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(password_text, password_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
            screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)))


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
            print(f"Saved highscore: {self.score} for user: {self.username}")
        else:
            print(f"No new highscore: user: {self.username}")

    def load_scores(self):
        if os.path.exists("highscores.json"):
            with open("highscores.json", "r") as file:
                self.accounts = json.load(file)

        print(f"Loaded all accounts")

    def check_username(self):
        if self.username in self.accounts:
            self.unlocked_user = False

    def unlock_user(self):
        self.create_password()

        if self.username in self.accounts:
            if self.hashed_password == self.accounts[self.username]["password"]:
                self.high_score = self.accounts[self.username]["score"]
                print(f"Loaded highscore ({self.high_score}) for user ({self.username}) out of storage")
            else:
                print("Wrong password")

                screen.fill(BLACK)
                enter_text = font.render("Wrong password!", True, RED)
                screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))


                pygame.display.flip()
                clock.tick(1)
                self.reset()
                clock.tick(FRAME_RATE)
                return
        self.pause = False
        self.checked_username = True
        self.unlocked_user = True
        print(f"Started game")

    def create_password(self):
        self.hashed_password = hashlib.sha512(self.password.encode('utf-8')).hexdigest()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FRAME_RATE)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
