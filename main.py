import os
import logging
import argparse

import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH, FULLSCREEN
from game import Game

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


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
        print(f"Missing required files: {', '.join(missing_files)}")
        exit(1)
    logging.info("All resources validated successfully.")
    print("All resources validated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Dino Game")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--fullscreen", action="store_true", help="Run game in fullscreen mode")
    parser.add_argument("--difficulty", choices=["easy", "normal", "hard"], default="normal",
                        help="Set the difficulty level (default: normal)")
    parser.add_argument("--fps", type=int, default=60, help="Set the frame rate (FPS) for the game (default: 60)")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled.")
        print("Debug mode enabled.")

    validate_resources()

    if args.fullscreen:
        SCREEN_WIDTH = 1920
        SCREEN_HEIGHT = 1080
        FULLSCREEN = True
        print("Running in fullscreen mode...")

    print(f"Difficulty level set to: {args.difficulty}")
    print(f"Running the game at {args.fps} FPS")

    logging.info("Starting the game...")
    print("Starting the game...")
    Game().run()