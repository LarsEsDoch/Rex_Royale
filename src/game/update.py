import random

from src.utils.config import SCREEN_WIDTH, SPEED_INCREMENT, BLACK, RED, SCREEN_HEIGHT
from src.entities.powerUp import PowerUp
from src.entities.obstacle import Obstacle
from src.utils.resources import logging, clock, GAME_OVER_SOUND, IMMORTALITY_SOUND, CLAIM_COIN_SOUND, COLLIDE_FIREBALL_SOUND, screen, font, pygame
from src.utils.utils import ease_out_cubic, hash_password


def update(self):
    # Aktualisiert die Musiklautstärke und überprüft die Musikposition
    update_music(self)

    # Aktualisiert den cursor tick
    update_pause_values(self)

    # Aktualisiert die High-Score-Liste
    if self.show_list:
        update_high_score_list(self)

    # Wenn das Spiel zu Ende ist, wird der Game-Over-Bildschirm aktualisiert
    if self.game_over:
        update_game_over_screen(self)

    # Wenn das Spiel pausiert oder zu Ende ist, werden keine weiteren Updates gemacht
    if self.pause or self.game_over:
        return

    # Falls der Account neu ist, wird Steuerungsinfo aktiviert
    if not self.username in self.accounts:
        self.show_control_info = True

    # Aktualisiert den Dino (z. B. Animation, Position)
    self.dino.update(self.score, self.sound_volume)

    # Aktualisiert Variablen wie Punktestand und Fortschritt
    update_game_variables(self)

    # Verarbeitet die Hintergrundbewegung
    update_background(self)

    # Verarbeitet die Feuerbälle (Bewegung, Entfernen, Kollisionsprüfung)
    update_fireballs(self)

    # Verarbeitet Hindernisse (Erzeugung, Kollisionen, Entfernen)
    update_obstacles(self)

    # Verarbeitet Power-Ups (Erzeugung, Kollisionen, Aktivierung)
    update_power_ups(self)

    # Wenn ein Power-Up aktiv ist, wird es aktualisiert
    if self.power_up_type is not None and self.power_up_timer >= 0:
        update_active_power_up(self)


def update_music(self):
    # Falls die Position der Spielmusik das Ende erreicht, wird sie zurückgesetzt
    if self.music_positon_game >= 108.877:
        self.music_positon_game -= 108.877

    # Falls die Pausenmusik das Ende erreicht, wird sie zurückgesetzt
    if self.music_positon_pause >= 240.0:
        self.music_positon_pause -= 240.0

    # Musiklautstärke einstellen
    pygame.mixer.music.set_volume(self.music_volume)


def update_pause_values(self):
    # Erhöht den Cursor-Tick um 1 und setzt ihn nach 60 zurück, für Animation
    self.cursor_tick += 1
    if self.cursor_tick >= 60:
        self.cursor_tick = 0


def update_high_score_list(self):
    # Aktiviert den Pausenzustand beim High-Score-Bildschirm
    self.pause = True

    # Bewegt die High-Score-Liste schrittweise für flüssige Scroll-Animation
    step = (self.target_high_score_list_y - self.high_score_list_y) * 0.2
    if abs(step) > 0.5:
        self.high_score_list_y += step


def update_game_over_screen(self):
    # Steigert die Einblendrate ("Fade-In") des Game-Over-Screens
    self.game_over_fade_in += 0.015

    # Verarbeitet die Verweilzeit für die Animation des Texts
    self.game_over_time += clock.get_time() / 300.0
    progress = min(self.game_over_time / 8.0, 1.0)
    scale_eased = ease_out_cubic(progress)

    # Skaliert den Text auf dem Game-Over-Bildschirm
    self.game_over_scale = 1 + scale_eased * 8

    # Zeitverfolgung für Screen Blending
    self.blend_in_time += clock.get_time() / 500.0


def update_game_variables(self):
    # Reduziert den Timer für Steuerungsinformationen
    self.control_info_time -= 1

    # Fortschrittsberechnung für Vögel, Tag/Nacht-Wechsel, (Welten Änderung zur Himmelwelt)
    self.progress_birds = min((self.score + self.progress_smoothed) / self.birds_score, 1)
    self.progress_day = min((self.score + self.progress_smoothed) / self.day_score, 1)
    self.progress_sky = min((self.score + self.progress_smoothed) / self.sky_score, 1)

    # Erhöht geglätteten Fortschrittswert basierend auf dem Punktestand
    if self.score < 100:
        self.progress_smoothed += 0.5
    else:
        self.progress_smoothed += 0.9


def update_background(self):
    # Bewegen der Hintergrundschichten mit verschiedenen Geschwindigkeiten:
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

    # Nacht-zu-Tag-Übergang, falls der Hintergrund mittig ist, da die Seiten sich unterscheiden
    if -400 >= self.background_x:
        self.night_to_day_transition = True

    if self.background_x <= -500 and (
            self.night_to_day_transition_progress == 1 or self.night_to_day_transition_progress == 0):
        self.night_to_day_transition = False

    if self.night_to_day_transition:
        if 5000 <= self.score <= 7000:
            self.night_to_day_transition_progress = min(
                self.night_to_day_transition_progress + self.night_to_day_transition_speed, 1)

    # Aktuellen Fortschritt im Übergang anwenden, indem die Opazität geändert wird
    self.background_day.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_2.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_2_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_3.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_3_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_4.set_alpha(int(self.night_to_day_transition_progress * 255))
    self.background_day_4_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))


def update_fireballs(self):
    # Iteriert über alle Feuerbälle und aktualisiert deren Zustand
    for fireball in self.fireballs[:]:
        fireball.update()  # Bewegt den Feuerball
        if fireball.complete_off_screen():
            # Entfernt Feuerbälle, die komplett außerhalb des Bildschirms sind
            logging.debug(f"Fireball complete off screen: {fireball.x + fireball.width < 0}")
            self.fireballs.remove(fireball)
            logging.debug("Removed fireball")


def update_obstacles(self):
    # Prüft, ob ein neues Hindernis generiert werden sollte
    if not self.obstacles or self.obstacles[-1].x < SCREEN_WIDTH - random.randint(650, 850) - self.spacing:
        self.spacing += 2.5  # Erhöht den Abstand zwischen Hindernissen schrittweise
        self.obstacles.append(Obstacle(self.score, self.power_up_type))  # Fügt ein neues Hindernis hinzu
        logging.debug(f"Placed new obstacle")

    # Iteration über die Hindernisse
    for obstacle in self.obstacles[:]:
        obstacle.update(self.obstacle_speed)  # Bewegt das Hindernis basierend auf der Geschwindigkeit

        # Überprüft Kollisionen zwischen Feuerbällen und Hindernissen
        for fireball in self.fireballs[:]:
            if fireball.collides_with(obstacle):
                # Punkte erhöhen und beide Objekte entfernen, wenn eine Kollision erkannt wird
                logging.debug("Obstacle collided with fireball")
                self.score += 50 # Nur 50 Punkte sonst zu einfach
                self.obstacles.remove(obstacle)
                self.fireballs.remove(fireball)
                COLLIDE_FIREBALL_SOUND.set_volume(self.sound_volume)
                COLLIDE_FIREBALL_SOUND.play()
                logging.debug("Removed obstacle")

        # Entfernt Hindernisse, die außerhalb des Bildschirms sind
        if obstacle.complete_off_screen():
            logging.debug(f"Obstacle complete off screen: {obstacle.x + obstacle.width[0] < 0}")
            self.obstacles.remove(obstacle)
            logging.debug("Removed obstacle")

        # Überprüft, ob ein Hindernis überwunden wurde
        if obstacle.conquered() and not obstacle.got_counted:
            logging.debug(f"Obstacle conquered: {obstacle.x + obstacle.width[0] < 0}")
            multiplicator = 2 if self.power_up_type == "multiplicator" else 1  # Multiplikator für Punkte erhöhen, wenn Power up aktiv ist
            if obstacle.type == "double":
                self.score += 150 * multiplicator
            else:
                self.score += 100 * multiplicator
            obstacle.got_counted = True  # Markiert das Hindernis als gezählt
            self.progress_smoothed = 0  # Setzt den geglätteten Fortschritt zurück
            logging.info(f"Score: {self.score}")

        # Überprüft, ob der Dino mit einem Hindernis kollidiert (außer Unsterblichkeits-Power-Up ist aktiv)
        if obstacle.collides_with(self.dino, self.ducked) and not self.power_up_type == "immortality":
            logging.info("Dino collided with obstacle")
            self.save_scores()  # Speichert den aktuellen Punktestand
            self.game_over = True  # Setzt den Spielzustand auf Game Over
            pygame.mixer.music.stop()  # Stopt die Musik
            GAME_OVER_SOUND.set_volume(self.sound_volume)  # Spielt Game Over Sound
            GAME_OVER_SOUND.play()

        # Erhöht die Geschwindigkeit von Hindernissen schrittweise
        self.obstacle_speed += SPEED_INCREMENT


def update_power_ups(self):
    # Prüft, ob Power-Ups erzeugt werden können (abhängig von Hindernissen)
    if not self.obstacles or self.obstacles[-1].x <= SCREEN_WIDTH - 400 - self.spacing:
        self.power_up_spacing = True
    else:
        self.power_up_spacing = False

    # Timer für die Erzeugung von Power-Ups erhöhen
    if self.power_up_timer < 0:
        self.power_up_timer += 1

    # Erzeugt ein Power-Up, wenn der Timer abgelaufen ist und kein Power-Up aktiv ist
    if self.power_up_timer >= 0 and self.power_up_spacing and self.power_up_type is None:
        logging.debug(f"Placed new power up ({self.power_up_timer})")
        self.power_ups.append(PowerUp(self.score))
        self.power_up_timer = random.randint(30 * 60, 45 * 60)  # Setzt den Timer neu
        self.power_up_timer = -self.power_up_timer

    # Iteriert über die aktiven Power-Ups
    for power_up in self.power_ups[:]:
        power_up.update(self.obstacle_speed)  # Bewegt das Power-Up
        if power_up.complete_off_screen():
            # Entfernt Power-Ups, die außerhalb des Bildschirms sind
            logging.debug(f"Power up complete off screen: {power_up.x + power_up.width < 0}")
            self.power_ups.remove(power_up)
            self.power_up_timer = random.randint(30 * 60, 45 * 60)  # Setzt den Erzeugungs-Timer zurück
            self.power_up_timer = -self.power_up_timer
            logging.debug("Removed power up")

        # Überprüft, ob der Dino ein Power-Up einsammelt
        if power_up.collides_with(self.dino) and self.power_up_type is None:
            logging.debug("Dino collided with power up")
            CLAIM_COIN_SOUND.set_volume(self.sound_volume)
            CLAIM_COIN_SOUND.play()
            # Aktiviert den Effekt basierend auf Typ des Power-Ups
            if power_up.type == "multiplicator":
                self.power_up_type = "multiplicator" # Aktiviert Multiplikator
                logging.info(f"Multiplicator power up")
            elif power_up.type == "immortality":
                self.power_up_type = "immortality"  # Aktiviert Unsterblichkeit
                self.music_positon_game += pygame.mixer.music.get_pos() / 1000  # Stoppt ältere Musik
                pygame.mixer.music.stop()
                IMMORTALITY_SOUND.set_volume(self.music_volume)
                IMMORTALITY_SOUND.play()
                logging.info("Immortality power up")
            elif power_up.type == "fly":
                self.power_up_type = "fly" # Aktiviert Unendliches Fliegen
                logging.info("Fly power up")
            elif power_up.type == "fireball":
                self.power_up_type = "fireball" # Aktiviert Feuerball-Schießen
                logging.info("Fireball power up")

            # Entfernt das eingesammelte Power-Up
            self.power_ups.remove(power_up)
            self.power_up_timer = 0
            logging.debug("Removed power up")


def update_active_power_up(self):
    # Zählt den Timer für das aktive Power-Up hoch
    self.power_up_timer += 1
    if self.power_up_timer > 15 * 60:  # Deaktiviert das Power-Up nach Ablauf von 15 Sekunden
        if self.power_up_type == "immortality":
            self.last_played_title = "game_music.wav"
            pygame.mixer.music.load('./assets/sounds/music/game_music.wav')  # Lädt standard Spiel Musik
            pygame.mixer.music.play(-1, start=self.music_positon_game, fade_ms=500)
        self.power_up_timer = random.randint(30 * 60, 45 * 60)  # Setzt den Timer zurück
        self.power_up_timer = -self.power_up_timer
        self.power_up_type = None
        logging.debug("Power up completed")


def unlock_user(self):
    # Verschlüsselt das Passwort und prüft Übereinstimmung mit gespeicherten Accounts
    self.hashed_password = hash_password(self.password)

    if self.username in self.accounts:
        if self.hashed_password == self.accounts[self.username]["password"]:
            # Lädt Benutzerinformationen wie Highscore und Lautstärkedaten wenn vorhanden
            self.high_score = self.accounts[self.username]["score"]
            logging.info(f"Loaded highscore ({self.high_score}) for user ({self.username})")
            if "music_volume" in self.accounts[self.username]:
                self.music_volume = self.accounts[self.username]["music_volume"]
                logging.info(f"Loaded music volume ({self.music_volume})")
            else:
                self.music_volume = 0.2
            if "sound_volume" in self.accounts[self.username]:
                self.sound_volume = self.accounts[self.username]["sound_volume"]
                logging.info(f"Loaded sound volume ({self.sound_volume})")
            else:
                self.sound_volume = 0.2
        else:
            # Zeigt Fehlernachricht bei falschem Passwort
            logging.info("Wrong password")
            screen.fill(BLACK)
            enter_text = font.render("Wrong password!", True, RED)
            screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            pygame.display.flip()
            clock.tick(1)
            self.reset(False)  # Setzt den Spielzustand zurück
            self.accounts_reset()
            clock.tick(self.fps)
            return

    # Setzt Benutzer erfolgreich frei, wenn Password korrekt war
    self.pause = False
    self.unlocked_user = True
    self.music_positon_pause += pygame.mixer.music.get_pos() / 1000
    self.last_played_title = "game_music.wav"
    pygame.mixer.music.load('./assets/sounds/music/game_music.wav')
    pygame.mixer.music.play(-1, start=self.music_positon_game, fade_ms=500)
    logging.info(f"Started game")