import random

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(["Multiplicator", "Immortality", "Speed", "Fly"])
        self.speed = 2
        self.multiplier = random.randint(1, 3)
        self.lifespan = random.randint(10, 20)
        self.current_time = 0
        self.y_velocity_boost = 0.5