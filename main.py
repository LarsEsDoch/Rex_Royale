import os
import argparse

import config
from config import logging
from game import Game

def validate_resources():
    logging.info("Validating resources...")
    required_files = ["textures/dino/dino_texture.png", "highscores.json", "textures/desert_day/desert_day_background.png",
                      "textures/desert_night/desert_night_background.png", "textures/desert_day/desert_day_background_2.png",
                      "textures/desert_night/desert_night_background_2.png", "textures/desert_day/desert_day_background_3.png",
                      "textures/desert_night/desert_night_background_3.png", "textures/desert_day/desert_day_background_4.png",
                      "textures/desert_night/desert_night_background_4.png", "textures/texts/game_over.png",
                      "textures/bird/frame_1.png", "textures/bird/frame_2.png", "textures/bird/frame_3.png",
                      "textures/bird/frame_4.png", "textures/bird/frame_5.png", "textures/bird/frame_6.png",
                      "textures/bird/frame_7.png", "textures/bird/frame_8.png", "textures/bird/frame_9.png",
                      "textures/bird/frame_10.png", "textures/bird/frame_11.png", "textures/bird/frame_12.png",
                      "textures/bird/frame_13.png", "textures/bird/frame_14.png", "textures/bird/frame_15.png",
                      "textures/bird/frame_16.png", "textures/bird/frame_17.png", "textures/bird/frame_18.png",
                      "textures/cactus_small/cactus_small_1.png", "textures/cactus_small/cactus_small_2.png",
                      "textures/cactus_small/cactus_small_3.png", "textures/cactus_small/cactus_small_4.png",
                      "textures/cactus_large/cactus_large_1.png", "textures/cactus_large/cactus_large_2.png",
                      "textures/cactus_large/cactus_large_3.png", "textures/cactus_large/cactus_large_4.png",]
    missing_files = [file for file in required_files if not os.path.exists(file)]

    if missing_files:
        logging.error(f"Missing required files: {', '.join(missing_files)}")
        exit(1)
    logging.info("All resources validated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Dino Game")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--show-fps", action="store_true", help="Show fps in the game window")
    parser.add_argument("--difficulty", choices=["easy", "normal", "hard"], default="normal",
                        help="Set the difficulty level (default: normal)")
    parser.add_argument("--fps", type=int, default=60, help="Set the frame rate (FPS) for the game (default: 60)")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Debug mode enabled.")

    validate_resources()

    difficulty_speeds = {
        "easy": 5,
        "normal": 7,
        "hard": 9
    }
    difficulty_gravity = {
        "easy": 0.4,
        "normal": 0.6,
        "hard": 0.9
    }
    difficulty_velocity = {
        "easy": -18,
        "normal": -17,
        "hard": -16
    }
    custom_obstacle_speed = difficulty_speeds[args.difficulty]
    config.GRAVITY = difficulty_gravity[args.difficulty]
    config.VELOCITY = difficulty_velocity[args.difficulty]
    logging.info(f"Set OBSTACLE_SPEED to: {config.OBSTACLE_SPEED}")
    config.FRAME_RATE = args.fps

    logging.info(f"Difficulty level set to: {args.difficulty}")
    logging.info(f"Running the game at {args.fps} FPS")

    logging.info("Starting the game...")

    Game(args.show_fps, custom_obstacle_speed).run()