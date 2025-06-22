import hashlib

from src.utils.config import logging
from src.utils.resources import pygame

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_out_sine(t):
    from math import sin, pi
    return sin((t * pi) / 2)

def load_frames_scaled(frame_path, frame_length, size):
    frames = []
    for i in range(frame_length):
        current_path = frame_path.replace('*', str(i))
        logging.debug(f"Loading: {current_path}")
        image = pygame.image.load(current_path)
        image = pygame.transform.scale(image, size).convert_alpha()
        frames.append(image)
    return frames

def load_frames(frame_path, frame_length):
    frames = []
    for i in range(frame_length):
        current_path = frame_path.replace('*', str(i))
        logging.debug(f"Loading: {current_path}")
        image = pygame.image.load(current_path).convert_alpha()
        frames.append(image)
    return frames

def load_frame(frame_path, size):
    logging.debug(f"Loading: {frame_path}")
    image = pygame.image.load(frame_path)
    image = pygame.transform.scale(image, size).convert_alpha()
    return image

def hash_password(password):
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    logging.debug(f"Hashed password: {hashed_password}")
    return hashed_password