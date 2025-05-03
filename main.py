import pygame
import random
import os

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
        print("Spawned Dino")

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
        print("Spawned obstacle")

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
        self.pause = False
        self.game_over = False
        self.score = 0
        self.obstacle_speed = OBSTACLE_SPEED
        self.dino = Dino()
        self.obstacles = []
        self.high_score = 0
        self.spacing = 0
        print("Prepared game")

    def reset(self):
        self.game_over = False
        self.dino = Dino()
        self.score = 0
        self.obstacle_speed = OBSTACLE_SPEED
        self.obstacles.clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.pause:
                        self.pause = False
                    elif self.game_over:
                        self.reset()
                        print("Reset")
                    else:
                        self.dino.start_jump()
                if event.key == pygame.K_ESCAPE:
                    self.running = False if self.game_over or self.pause else True
                    self.pause = not self.pause

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
                self.high_score = max(self.score, self.high_score)
                self.game_over = True

    def draw(self):
        screen.fill(WHITE)
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

        if not self.username_existing:
            screen.fill(BLACK)

            pause_text = font.render("Enter your username!", True, WHITE)
            continue_text = font.render(f"Username: {self.username}", True, WHITE)
            escape_text = font.render("Press enter to confirm", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        if self.username_existing and not self.checked_username:
            self.check_username()

        pygame.display.flip()

    def save_scores(self):
        scores = self.high_scores

        if self.score > scores.get(self.username, 0):
            scores[self.username] = self.score

            with open("highscores.json", "w") as file:
                json.dump(scores, file, indent=4)
            print(f"Saved highscore: {self.score} for user: {self.username}")


    def load_scores(self):
        if os.path.exists("highscores.json"):
            with open("highscores.json", "r") as file:
                self.high_scores = json.load(file)

        print(f"Loaded all highscores")

    def check_username(self):
        if self.username in self.high_scores:
            self.high_score = self.high_scores.get(self.username, 0)
            print(f"Set highscore ({self.high_score}) for user ({self.username}) out of storage")
        self.pause = False
        self.checked_username = True


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
