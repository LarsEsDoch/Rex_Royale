from src.utils.config import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entities.fireball import Fireball
from src.utils.resources import pygame, SHOT_FIREBALL_SOUND, SELECT_SOUND, IMMORTALITY_SOUND, logging
from src.game import update

def handleEvents(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_window(self)

        if event.type == pygame.MOUSEBUTTONDOWN:
            event_mouse_button_down(self, event)

        if event.type == pygame.MOUSEBUTTONUP:
            event_mouse_button_up(self, event)

        if self.holding_mouse_music_control or self.holding_mouse_sound_control:
            update_volume(self)

        if event.type == pygame.KEYDOWN:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                event_debug(self, event)
            event_key_down(self, event)

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_DOWN or event.key == pygame.K_LSHIFT) and not self.pause and not self.game_over:
                self.ducked = False

def exit_window(self):
    self.running = False
    self.save_scores()
    SELECT_SOUND.set_volume(self.sound_volume)
    SELECT_SOUND.play()
    logging.info("Exit")

def event_mouse_button_down(self, event):
    if self.show_list:
        if event.button == 4 and self.target_high_score_list_y <= -40:
            self.target_high_score_list_y += 40
            logging.debug("Mouse scrolled up")
        elif event.button == 5 and self.target_high_score_list_y >= len(
                self.accounts) * -50 + 120 + SCREEN_HEIGHT // 1.5:
            self.target_high_score_list_y -= 40
            logging.debug("Mouse scrolled down")

    if self.pause and not self.game_over and self.unlocked_user and event.button == 1:
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if SCREEN_WIDTH // 2 - 250 <= mouse_x <= SCREEN_WIDTH // 2 + 250:

            if SCREEN_HEIGHT // 2 - 105 <= mouse_y <= SCREEN_HEIGHT // 2 - 105 + 30:
                self.holding_mouse_music_control = True
                logging.debug("Holding Music volume")
            elif SCREEN_HEIGHT // 2 - 5 <= mouse_y <= SCREEN_HEIGHT // 2 - 5 + 30:
                self.holding_mouse_sound_control = True
                logging.debug("Holding Sound volume")

def event_mouse_button_up(self, event):
    if self.pause and not self.game_over and self.unlocked_user and event.button == 1:
        if self.holding_mouse_sound_control:
            SELECT_SOUND.set_volume(self.sound_volume)
            SELECT_SOUND.play()
        self.holding_mouse_music_control = False
        self.holding_mouse_sound_control = False
        logging.debug("Mouse released")
        return

def update_volume(self):
    mouse_x = pygame.mouse.get_pos()[0]

    offset = mouse_x - SCREEN_WIDTH // 2 - 250
    percentage = max(min(100 + (offset / 500) * 100, 100), 0)

    if self.holding_mouse_music_control:
        self.music_volume = percentage / 100
        logging.debug(f"Set music volume: {percentage:.2f}%")
    else:
        self.sound_volume = percentage / 100
        logging.debug(f"Set sound volume: {percentage:.2f}%")

def event_key_down(self, event):
    if event.key == pygame.K_ESCAPE:
        event_escape(self)

    if event.key == pygame.K_F1:
        toggle_high_score_list(self)

    if event.key == pygame.K_BACKSPACE and self.game_over and self.username_existing or event.key == pygame.K_BACKSPACE and self.pause and self.username_existing and self.password.strip() == "" or event.key == pygame.K_BACKSPACE and self.pause and self.unlocked_user:
        complete_reset(self)

    if event.key == pygame.K_RETURN and self.game_over and self.game_over_fade_in >= 1 or event.key == pygame.K_RETURN and self.pause and self.unlocked_user:
        score_reset(self)

    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
        jump(self)

    if (event.key == pygame.K_DOWN or event.key == pygame.K_LSHIFT) and not self.pause and not self.game_over:
        self.ducked = True

    if (event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT) and not self.pause and self.power_up_type == "fireball" and len(
            self.fireballs) < 2:
        add_fireball(self)

    if not self.username_existing:
        username_input(self, event)

    if self.username_existing and not self.checked_username:
        password_input(self, event)

def event_debug(self, event):
    if event.key == pygame.K_q:
        self.fps = 60
        logging.debug(f"Set FPS to 60")
    if event.key == pygame.K_w:
        self.fps = 30
        logging.debug(f"Set FPS to 30")
    if event.key == pygame.K_e:
        self.fps = 20
        logging.debug(f"Set FPS to 20")
    if event.key == pygame.K_r:
        self.fps = 10
        logging.debug(f"Set FPS to 10")
    if event.key == pygame.K_t:
        self.fps = 5
        logging.debug(f"Set FPS to 5")
    if event.key == pygame.K_z:
        self.fps = 1
        logging.debug(f"Set FPS to 1")
    if event.key == pygame.K_k and not self.pause:
        self.freeze = not self.freeze
        logging.debug(f"Freeze: {self.freeze}")
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

def event_escape(self):
    if self.show_list:
        self.show_list = False
        logging.info(f"Toggle high score list")
        SELECT_SOUND.set_volume(self.sound_volume)
        SELECT_SOUND.play()
        return
    self.running = False if self.game_over or self.pause else True
    self.pause = not self.pause
    if not self.running:
        self.save_scores()
        SELECT_SOUND.set_volume(self.sound_volume)
        SELECT_SOUND.play()
        logging.info("Exit")
    else:
        self.last_played_title = "pause_music.wav"
        self.music_positon_game += pygame.mixer.music.get_pos() / 1000
        pygame.mixer.music.load('./assets/sounds/music/pause_music.wav')
        pygame.mixer.music.play(-1, start=self.music_positon_pause, fade_ms=500)
        IMMORTALITY_SOUND.stop()
        SELECT_SOUND.set_volume(self.sound_volume)
        SELECT_SOUND.play()
        logging.info("Paused")

def toggle_high_score_list(self):
    self.show_list = not self.show_list
    if self.show_list:
        logging.info(f"Show high score list")
    else:
        logging.info(f"Hide high score list")
    if not self.last_played_title == "pause_music.wav":
        self.last_played_title = "pause_music.wav"
        self.music_positon_game += pygame.mixer.music.get_pos() / 1000
        pygame.mixer.music.load('./assets/sounds/music/pause_music.wav')
        pygame.mixer.music.play(-1, start=self.music_positon_pause, fade_ms=500)
    IMMORTALITY_SOUND.stop()
    SELECT_SOUND.set_volume(self.sound_volume)
    SELECT_SOUND.play()
    logging.info("Paused")
    return

def complete_reset(self):
    if self.press_to_return >= 5 or (self.unlocked_user and self.username_existing):
        self.music_positon_pause += pygame.mixer.music.get_pos() / 1000
        self.reset(False)
        self.accounts_reset()
        SELECT_SOUND.set_volume(self.sound_volume)
        SELECT_SOUND.play()
        logging.info("Complete reset")
    else:
        self.press_to_return += 1
        return

def score_reset(self):
    self.save_scores()
    self.reset(True)
    self.pause = False
    SELECT_SOUND.set_volume(self.sound_volume)
    SELECT_SOUND.play()
    logging.info("Reset Score")

def jump(self):
    if self.pause and self.username_existing and self.checked_username and self.unlocked_user:
        self.pause = False
        self.show_list = False
        self.music_positon_pause += pygame.mixer.music.get_pos() / 1000
        self.last_played_title = "game_music.wav"
        pygame.mixer.music.load('./assets/sounds/music/game_music.wav')
        pygame.mixer.music.play(-1, start=self.music_positon_game, fade_ms=500)
        self.save_scores()
        self.holding_mouse = False
        logging.info("Resumed")
    elif self.game_over:
        if self.game_over_fade_in >= 1:
            self.reset(True)
            SELECT_SOUND.set_volume(self.sound_volume)
            SELECT_SOUND.play()
            logging.info("Reset Score")
    elif self.unlocked_user:
        logging.debug("Jump")
        if self.dino.y > 50:
            self.dino.start_jump(self.power_up_type, self.sound_volume)

def add_fireball(self):
    self.fireballs.append(Fireball(self.dino.y))
    SHOT_FIREBALL_SOUND.set_volume(self.sound_volume)
    SHOT_FIREBALL_SOUND.play()
    logging.debug("Fireball spawned")

def username_input(self, event):
    if event.key == pygame.K_RETURN and self.username.strip() != "":
        self.username_existing = True
        SELECT_SOUND.set_volume(self.sound_volume)
        SELECT_SOUND.play()
        update.check_username(self)
        logging.info(f"Got username: {self.username}")
    elif event.key == pygame.K_BACKSPACE:
        self.username = self.username[:-1]
        logging.debug("Backspace")
    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
        self.username += event.unicode
        logging.debug(f"Key pressed: {event.key}")
    self.cursor_tick = 0

def password_input(self, event):
    if event.key == pygame.K_RETURN and self.password.strip() != "":
        logging.info(f"Got password: {self.password}")
        SELECT_SOUND.set_volume(self.sound_volume)
        SELECT_SOUND.play()
        update.unlock_user(self)
    elif event.key == pygame.K_BACKSPACE:
        self.password = self.password[:-1]
        logging.debug("Backspace")
    elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
        self.password += event.unicode
        logging.debug(f"Key pressed: {event.key}")
        self.press_to_return = 0
    self.cursor_tick = 0