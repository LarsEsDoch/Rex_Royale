from src.utils.config import SCREEN_HEIGHT
from src.entities.fireball import Fireball
from src.utils.resources import pygame, SHOT_FIREBALL_SOUND, SELECT_SOUND
from src.utils.resources import logging

def handleEvents(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
            self.save_scores()
            SELECT_SOUND.set_volume(self.sound_volume)
            SELECT_SOUND.play()
            logging.info("Exit")

        if event.type == pygame.MOUSEBUTTONDOWN and self.show_list:
            if event.button == 4 and self.target_high_score_list_y <= -40:
                self.target_high_score_list_y += 40
                logging.debug("Mouse scrolled up")
            elif event.button == 5 and self.target_high_score_list_y >= len(
                    self.accounts) * -50 + 120 + SCREEN_HEIGHT // 1.5:
                self.target_high_score_list_y -= 40
                logging.debug("Mouse scrolled down")

        if event.type == pygame.KEYDOWN:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                if event.key == pygame.K_q:
                    self.fps = 60
                if event.key == pygame.K_w:
                    self.fps = 30
                if event.key == pygame.K_e:
                    self.fps = 20
                if event.key == pygame.K_r:
                    self.fps = 10
                if event.key == pygame.K_t:
                    self.fps = 5
                if event.key == pygame.K_z:
                    self.fps = 1

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
                    pygame.mixer.music.load('./assets/sounds/music/pause_music.wav')
                    pygame.mixer.music.play(-1)
                    SELECT_SOUND.set_volume(self.sound_volume)
                    SELECT_SOUND.play()
                    logging.info("Paused")

            if event.key == pygame.K_F1:
                self.show_list = not self.show_list
                logging.info(f"Toggle high score list")
                SELECT_SOUND.set_volume(self.sound_volume)
                SELECT_SOUND.play()
                return

            if event.key == pygame.K_BACKSPACE and self.game_over and self.username_existing or event.key == pygame.K_BACKSPACE and self.pause and self.username_existing and self.password.strip() == "" or event.key == pygame.K_BACKSPACE and self.pause and self.unlocked_user:
                if not self.unlocked_user and self.username_existing:
                    if self.press_to_return >= 5:
                        self.reset()
                        self.accounts_reset()
                        SELECT_SOUND.set_volume(self.sound_volume)
                        SELECT_SOUND.play()
                        logging.info("Reset")
                    self.press_to_return += 1
                    return

                self.reset()
                self.accounts_reset()
                SELECT_SOUND.set_volume(self.sound_volume)
                SELECT_SOUND.play()
                logging.info("Reset")

            if event.key == pygame.K_RETURN and self.game_over or event.key == pygame.K_RETURN and self.pause and self.unlocked_user:
                self.save_scores()
                self.reset()
                SELECT_SOUND.set_volume(self.sound_volume)
                SELECT_SOUND.play()
                logging.info("Reset Score")

            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if self.pause and self.username_existing and self.checked_username and self.unlocked_user:
                    self.pause = False
                    pygame.mixer.music.load('./assets/sounds/music/game_music.wav')
                    pygame.mixer.music.play(-1)
                    logging.info("Resumed")
                elif self.game_over:
                    if self.game_over_fade_in >= 1:
                        self.reset()
                        SELECT_SOUND.set_volume(self.sound_volume)
                        SELECT_SOUND.play()
                        logging.info("Reset Score")
                else:
                    logging.debug("Jump")
                    if self.dino.y > 50:
                        self.dino.start_jump(self.power_up_type, self.sound_volume)
            if (event.key == pygame.K_DOWN or event.key == pygame.K_LSHIFT) and not self.pause and not self.game_over:
                self.ducked = True
            if (event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT) and not self.pause and self.power_up_type == "fireball" and len(self.fireballs) < 5:
                self.fireballs.append(Fireball(self.dino.y))
                SHOT_FIREBALL_SOUND.set_volume(self.sound_volume)
                SHOT_FIREBALL_SOUND.play()
                logging.debug("Fireball spawned")

            if not self.username_existing:
                if event.key == pygame.K_RETURN and self.username.strip() != "":
                    self.username_existing = True
                    SELECT_SOUND.set_volume(self.sound_volume)
                    SELECT_SOUND.play()
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
                    SELECT_SOUND.set_volume(self.sound_volume)
                    SELECT_SOUND.play()
                    self.unlock_user()
                elif event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                    logging.debug("Backspace")
                elif not event.key == pygame.K_RETURN and not event.key == pygame.K_SPACE:
                    self.password += event.unicode
                    logging.debug(f"Key pressed: {event.key}")
                    self.press_to_return = 0
                self.cursor_tick = 0

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_DOWN or event.key == pygame.K_LSHIFT) and not self.pause and not self.game_over:
                self.ducked = False