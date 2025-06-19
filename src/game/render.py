from src.utils.config import SCREEN_WIDTH, BLACK, GROUND_LEVEL, WHITE, BROWN, GOLD, SILVER, BRONZE, BLUE, SCREEN_HEIGHT, GRAY
from src.utils.utils import ease_out_sine
from src.utils.resources import screen, clock, font, font_large, pygame, logging, font_small

def render(self):
    render_background(self)

    for obstacle in self.obstacles:
        obstacle.render()

    for power_up in self.power_ups:
        power_up.render()

    for fireball in self.fireballs:
        fireball.render()
    self.dino.render(self.ducked)

    color = WHITE if self.pause or self.game_over else BLACK

    if self.power_up_type is not None and not self.game_over:
        render_power_up_info(self, color)

    if self.game_over:
        render_game_over_screen(self)

    if self.pause:
        render_pause_screen(self)

    render_user_info(self, color)

    if not self.pause and self.control_info_time >= 0 and self.show_control_info:
        render_control_info()

    if not self.pause and not self.game_over and self.score < 6000:
        render_progress_bars(self)

    if self.cursor_tick < 30:
        cursor = "|"
    else:
        cursor = " "

    if not self.username_existing and not self.unlocked_user and not self.checked_username:
        render_username_gui(self, cursor)

    if not self.unlocked_user and self.username_existing:
        render_password_gui(self, cursor)

    if self.show_list:
        render_high_score_list(self)

    if self.show_fps:
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, color)
        screen.blit(fps_text, (SCREEN_WIDTH - 110, 10))

    pygame.display.flip()

def render_background(self):
    if not self.background_flip:
        screen.blit(self.background_night_flipped, (self.background_x, 0))
        screen.blit(self.background_night, (self.background_x + SCREEN_WIDTH + 800, 0))
    else:
        screen.blit(self.background_night, (self.background_x, 0))
        screen.blit(self.background_night_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

    self.background_day.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
    if not self.background_flip:
        screen.blit(self.background_day_flipped, (self.background_x, 0))
        screen.blit(self.background_day, (self.background_x + SCREEN_WIDTH + 800, 0))
    else:
        screen.blit(self.background_day, (self.background_x, 0))
        screen.blit(self.background_day_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

    if not self.background_flip_2:
        screen.blit(self.background_night_2_flipped, (self.background_x_2, 410))
        screen.blit(self.background_night_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
    else:
        screen.blit(self.background_night_2, (self.background_x_2, 410))
        screen.blit(self.background_night_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

    self.background_day_2.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_2_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
    if not self.background_flip_2:
        screen.blit(self.background_day_2_flipped, (self.background_x_2, 410))
        screen.blit(self.background_day_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
    else:
        screen.blit(self.background_day_2, (self.background_x_2, 410))
        screen.blit(self.background_day_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

    if not self.background_flip_3:
        screen.blit(self.background_night_3_flipped, (self.background_x_3, 500))
        screen.blit(self.background_night_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
    else:
        screen.blit(self.background_night_3, (self.background_x_3, 500))
        screen.blit(self.background_night_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))

    self.background_day_3.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_3_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
    if not self.background_flip_3:
        screen.blit(self.background_day_3_flipped, (self.background_x_3, 500))
        screen.blit(self.background_day_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
    else:
        screen.blit(self.background_day_3, (self.background_x_3, 500))
        screen.blit(self.background_day_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))

    if not self.background_flip_4:
        screen.blit(self.background_night_4_flipped, (self.background_x_4, GROUND_LEVEL - 80))
        screen.blit(self.background_night_4, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))
    else:
        screen.blit(self.background_night_4, (self.background_x_4, GROUND_LEVEL - 80))
        screen.blit(self.background_night_4_flipped, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))

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

def render_game_over_screen(self):
    rect_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    rect_surface.set_alpha(self.game_over_fade_in * 255)
    rect_surface.fill(BLACK)
    screen.blit(rect_surface, (0, 0))
    progress = min(self.game_over_time / 8.0, 1.0)
    opacity_eased = ease_out_sine(progress)
    opacity = int(255 * opacity_eased)

    original_width = self.game_over_image.get_width()
    original_height = self.game_over_image.get_height()
    aspect_ratio = original_width / original_height
    scaled_height = int(70 * self.game_over_scale)
    scaled_width = int(scaled_height * aspect_ratio)

    game_over_screen = pygame.transform.scale(self.game_over_image,
                                              (min(scaled_width, 1119), min(scaled_height, 624)))
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
        screen.blit(change_account_text,
                    change_account_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 330)))

def render_pause_screen(self):
    screen.fill(BLACK)
    render_volume_sliders(self)
    game_text = font_large.render("Rex Royale", True, WHITE)
    pause_text = font.render("Paused", True, WHITE)
    continue_text = font.render("Press space to continue", True, WHITE)
    escape_text = font.render("Press escape to exit", True, WHITE)
    restart_text = font.render("Press enter to start from beginning", True, WHITE)
    hard_restart_text = font.render("Press backspace to change account", True, WHITE)
    high_score_text = font.render("Press F1 to see highscores", True, WHITE)
    screen.blit(game_text, game_text.get_rect(center=(SCREEN_WIDTH // 2, 50)))
    screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 - 100)))
    screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + 100)))
    screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
    screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50 + 100)))
    screen.blit(hard_restart_text, hard_restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + 100)))
    screen.blit(high_score_text, high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150 + 100)))

def render_user_info(self, color):
    score_text = font.render(f"Score: {self.score}", True, color)
    screen.blit(score_text, (10, 10))
    username_text = font.render(f"User: {self.username}", True, color)
    screen.blit(username_text, (10, 35))
    highest_score_text = font.render(f"High Score: {max(self.score, self.high_score)}", True, color)
    screen.blit(highest_score_text, (10, 60))

def render_control_info():
    control_info_text = font.render("Space or Arrow Up to jump", True, BLACK)
    screen.blit(control_info_text, (SCREEN_WIDTH - control_info_text.get_width() - 20, 200))
    control_info_text_2 = font.render("Shift or Arrow Down to duck", True, BLACK)
    screen.blit(control_info_text_2, (SCREEN_WIDTH - control_info_text_2.get_width() - 20, 225))
    control_info_text_3 = font.render("Enter or Arrow Right to shoot fireballs", True, BLACK)
    screen.blit(control_info_text_3, (SCREEN_WIDTH - control_info_text_3.get_width() - 20, 250))
    control_info_text_4 = font.render("Escape to pause the game", True, BLACK)
    screen.blit(control_info_text_4, (SCREEN_WIDTH - control_info_text_4.get_width() - 20, 275))

def render_power_up_info(self, color):
    power_up_text = font.render(f"Power Up: {self.power_up_type}", True, color)
    screen.blit(power_up_text, (10, 85))
    rect_surface = pygame.Surface((SCREEN_WIDTH // 4, 30), pygame.SRCALPHA)
    rect_surface.set_alpha(128)
    rect_surface.fill(WHITE)
    screen.blit(rect_surface, (10, 120))

    pygame.draw.rect(screen, color,
                     (10, 120, (1 - (self.power_up_timer / (60 * 15))) * SCREEN_WIDTH // 4, 30))
    pygame.draw.rect(screen, WHITE, (10, 120, SCREEN_WIDTH // 4, 30), 2)

def render_progress_bars(self):
    rect_surface = pygame.Surface((SCREEN_WIDTH // 2, 50), pygame.SRCALPHA)
    rect_surface.set_alpha(128)
    rect_surface.fill(WHITE)
    screen.blit(rect_surface, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10))

    pygame.draw.rect(screen, BROWN,
                     (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_birds * SCREEN_WIDTH // 2, 50))
    pygame.draw.rect(screen, BLUE,
                     (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_day * SCREEN_WIDTH // 2, 50))
    # pygame.draw.rect(screen, LIGHT_BLUE,
    #                  (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_sky * SCREEN_WIDTH // 2, 50))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, SCREEN_WIDTH // 2, 50), 2)

def render_username_gui(self, cursor):
    screen.fill(BLACK)

    game_text = font_large.render("Rex Royale", True, WHITE)
    pause_text = font.render("Enter your username!", True, WHITE)
    username_text = font.render(f"Username: {self.username}{cursor}", True, WHITE)
    enter_text = font.render("Press enter to confirm", True, WHITE)
    screen.blit(game_text, game_text.get_rect(center=(SCREEN_WIDTH // 2, 50)))
    screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
    screen.blit(username_text, username_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

def render_password_gui(self, cursor):
    screen.fill(BLACK)
    password = ""
    for i in range(len(self.password)):
        password += "*"

    if self.username in self.accounts:
        pause_text = font.render("User exists already!", True, WHITE)
    else:
        pause_text = font.render("Creating new account!", True, WHITE)
    game_text = font_large.render("Rex Royale", True, WHITE)
    info_text = font.render("Enter password to proceed", True, WHITE)
    password_text = font.render(f"Password: {password}{cursor}", True, WHITE)
    enter_text = font.render("Press enter to confirm", True, WHITE)
    restart_text = font.render("Press backspace to use another account", True, WHITE)
    return_text = font.render(f"Press 5 times to return: 5/{self.press_to_return}", True, WHITE)
    screen.blit(game_text, game_text.get_rect(center=(SCREEN_WIDTH // 2, 50)))
    screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
    screen.blit(info_text, info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
    screen.blit(password_text, password_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
    screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
    screen.blit(return_text, return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)))

def render_high_score_list(self):
    screen.fill(BLACK)
    game_text = font.render("Rex Royale", True, WHITE)
    screen.blit(game_text, game_text.get_rect(center=(75, 20)))
    header_text = font_large.render("All highscores", True, WHITE)
    screen.blit(header_text, header_text.get_rect(center=(SCREEN_WIDTH // 2, 50 + self.high_score_list_y)))
    accounts = sorted(self.accounts.items(), key=lambda x: x[1]["score"], reverse=True)
    for account, (username, score) in enumerate(accounts):
        colors = {2: BRONZE, 1: SILVER, 0: GOLD}
        color = colors.get(account, WHITE)
        score_text = font.render(f"{username}: {score['score']}", True, color)
        screen.blit(score_text,
                    score_text.get_rect(center=(SCREEN_WIDTH // 2, account * 50 + 120 + self.high_score_list_y)))

def render_volume_sliders(self):
    music_volume_text = font.render("Music Volume", True, WHITE)
    screen.blit(music_volume_text, music_volume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)))
    music_volume_text_value = font_small.render(f"{int(self.music_volume * 100)}%", True, WHITE)
    screen.blit(music_volume_text_value, music_volume_text_value.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)))

    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 105, 500, 30), 2)
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 248, SCREEN_HEIGHT // 2 - 103, 496 * self.music_volume, 26))
    pygame.draw.rect(screen, WHITE, ((SCREEN_WIDTH // 2 - 250) + 500 * self.music_volume - 5, SCREEN_HEIGHT // 2 - 107, 10, 34))

    sound_volume_text = font.render("SFX Volume", True, WHITE)
    screen.blit(sound_volume_text, sound_volume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
    sound_volume_text_value = font_small.render(f"{int(self.sound_volume * 100)}%", True, WHITE)
    screen.blit(sound_volume_text_value, sound_volume_text_value.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 5, 500, 30), 2)
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 248, SCREEN_HEIGHT // 2 - 3, 496 * self.sound_volume, 26))
    pygame.draw.rect(screen, WHITE,((SCREEN_WIDTH // 2 - 250) + 500 * self.sound_volume - 5, SCREEN_HEIGHT // 2 - 7, 10, 34))