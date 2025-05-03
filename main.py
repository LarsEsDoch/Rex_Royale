import pygame
import random
import os
import json
import hashlib

pygame.init()
print("Initialized pygame successful")


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

GRAVITY = 0.9
GROUND_LEVEL = SCREEN_HEIGHT - 50
OBSTACLE_SPEED = 7
SPEED_INCREMENT = 0.1
print("Initialized game constants")

font = pygame.font.Font(None, 36)
print("Set font")


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
        if not self.jump:
            self.jump = True
            self.velocity_y = -20


class Obstacle:

    def __init__(self, score):
        if score < 5000:
            self.type = random.choice(["small", "large", "double"])
        else:
            self.type = random.choice(["small", "large", "double", "bird"])

        self.width, self.height = (40, 50) if self.type == "small" else (30, 80) if self.type == "large" else (20, 90) if self.type == "double" else (40, 40)

        if self.type == "bird":
            self.image = pygame.image.load(f'textures/bird.png')
            self.y = GROUND_LEVEL - self.height - 170
            self.x = SCREEN_WIDTH + random.randint(50, 300)
        else:
            self.image = pygame.image.load(f'textures/cactus_{1 if self.type == "small" else 2 if self.type == "large" else 3}.png')
            self.y = GROUND_LEVEL - self.height
            self.x = SCREEN_WIDTH + random.randint(50, 300)

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.first_drawn = False

    def update(self, speed):
        if self.type == "bird":
            if not self.first_drawn:
                self.x = SCREEN_WIDTH*2.5
                self.first_drawn = True
            self.x -= speed * 1.5

        self.x -= speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.x + self.width < 0

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
        self.background_day = pygame.image.load('textures/desert_day_background.png')
        self.background_night = pygame.image.load('textures/desert_night_background.png')
        self.background_x = 0
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

                if event.type == pygame.KEYDOWN and not self.username_existing:
                    if event.key == pygame.K_RETURN and self.username.strip() != "":
                        self.username_existing = True
                        print(f"Got username: {self.username}")
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                        self.username += event.unicode
                    self.cursor_tick = 0

                if event.type == pygame.KEYDOWN and self.username_existing and not self.checked_username:
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

        if not self.obstacles or self.obstacles[-1].x < SCREEN_WIDTH - random.randint(300, 600) - self.spacing:
            self.spacing += 2
            self.obstacles.append(Obstacle(self.score))

        for obstacle in self.obstacles[:]:
            obstacle.update(self.obstacle_speed)

            if obstacle.off_screen():
                self.obstacles.remove(obstacle)
                self.score += 100
                self.obstacle_speed += SPEED_INCREMENT

                print(f"Score: {self.score}")

            if obstacle.collides_with(self.dino):
                print("Dino collided")

                self.save_scores()
                self.game_over = True

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
            self.background_x -= self.obstacle_speed * 0.25
            if self.background_x <= -SCREEN_WIDTH:
                self.background_x = 0

        screen.blit(self.background_day, (self.background_x, 0))
        screen.blit(self.background_day, (self.background_x + SCREEN_WIDTH, 0))
        pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 3)
        self.dino.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

        color = WHITE if self.pause or self.game_over else BLACK

        if self.game_over:
            screen.fill(BLACK)

            game_over_text = font.render("Game Over", True, WHITE)
            restart_text = font.render("Press space to restart", True, WHITE)
            escape_text = font.render("Press escape to exit", True, WHITE)
            screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

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
                clock.tick(60)
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
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
