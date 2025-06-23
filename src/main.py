import os
import argparse
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import config
from src.utils.config import logging, FRAME_RATE, DIFFICULTY_SPEEDS, \
    DIFFICULTY_GRAVITIES, DIFFICULTY_VELOCITIES
from src.game.game import Game

def validate_resources():
    required_files = [
        "./assets/textures/backgrounds/day/day_background_0.png",
        "./assets/textures/backgrounds/day/day_background_1.png",
        "./assets/textures/backgrounds/day/day_background_2.png",
        "./assets/textures/backgrounds/day/day_background_3.png",
        "./assets/textures/backgrounds/night/night_background_0.png",
        "./assets/textures/backgrounds/night/night_background_1.png",
        "./assets/textures/backgrounds/night/night_background_2.png",
        "./assets/textures/backgrounds/night/night_background_3.png",
        "./assets/textures/texts/game_over.png",
        "./assets/textures/bird/frame_0.png",
        "./assets/textures/bird/frame_1.png",
        "./assets/textures/bird/frame_2.png",
        "./assets/textures/bird/frame_3.png",
        "./assets/textures/bird/frame_4.png",
        "./assets/textures/bird/frame_5.png",
        "./assets/textures/bird/frame_6.png",
        "./assets/textures/bird/frame_7.png",
        "./assets/textures/bird/frame_8.png",
        "./assets/textures/bird/frame_9.png",
        "./assets/textures/bird/frame_10.png",
        "./assets/textures/bird/frame_11.png",
        "./assets/textures/bird/frame_12.png",
        "./assets/textures/bird/frame_13.png",
        "./assets/textures/bird/frame_14.png",
        "./assets/textures/bird/frame_15.png",
        "./assets/textures/bird/frame_16.png",
        "./assets/textures/bird/frame_17.png",
        "./assets/textures/cactus_small/cactus_small_0.png",
        "./assets/textures/cactus_small/cactus_small_1.png",
        "./assets/textures/cactus_small/cactus_small_2.png",
        "./assets/textures/cactus_small/cactus_small_3.png",
        "./assets/textures/cactus_large/cactus_large_0.png",
        "./assets/textures/cactus_large/cactus_large_1.png",
        "./assets/textures/cactus_large/cactus_large_2.png",
        "./assets/textures/cactus_large/cactus_large_3.png",
        "./assets/textures/dino/dino_frame_0.png",
        "./assets/textures/dino/dino_frame_1.png",
        "./assets/textures/dino/dino_frame_2.png",
        "./assets/textures/dino/dino_frame_3.png",
        "./assets/textures/dino/dino_frame_4.png",
        "./assets/textures/dino/dino_frame_5.png",
        "./assets/textures/dino/dino_frame_6.png",
        "./assets/textures/dino/dino_frame_7.png",
        "./assets/textures/dino/dino_frame_8.png",
        "./assets/textures/dino/dino_frame_9.png",
        "./assets/textures/dino/dino_duck.png",
        "./assets/textures/power_ups/multiplicator.png",
        "./assets/textures/power_ups/immortality.png",
        "./assets/textures/power_ups/fly.png",
        "./assets/textures/power_ups/fireball.png",
        "./assets/textures/power_ups/fireball/fireball_0.png",
        "./assets/textures/power_ups/fireball/fireball_1.png",
        "./assets/textures/power_ups/fireball/fireball_2.png",
        "./assets/textures/power_ups/fireball/fireball_3.png",
        "./assets/textures/power_ups/fireball/fireball_4.png"]
    missing_files = [file for file in required_files if not os.path.exists(file)]

    if missing_files:
        logging.error(f"Missing required game files: {', '.join(missing_files)}")
        exit(1)
    logging.info("All resources validated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Dino Game")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--show-fps", action="store_true", help="Show fps in the game window")
    parser.add_argument("--difficulty", choices=["easy", "normal", "hard"], default="normal",
                        help="Set the difficulty level (default: normal)")
    parser.add_argument("--fps", type=int, default=FRAME_RATE, help="Set the frame rate (FPS) for the game (default: 60)")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Debug mode enabled")

    validate_resources()

    custom_obstacle_speed = DIFFICULTY_SPEEDS[args.difficulty]
    config.GRAVITY = DIFFICULTY_GRAVITIES[args.difficulty]
    config.VELOCITY = DIFFICULTY_VELOCITIES[args.difficulty]
    logging.info(f"Set obstacle speed to: {config.OBSTACLE_SPEED}")
    fps = args.fps

    logging.info(f"Difficulty level set to: {args.difficulty}")
    logging.info(f"Running the game at {args.fps} FPS")

    logging.info("Starting the game...")
    Game(args.show_fps, custom_obstacle_speed, fps).run()