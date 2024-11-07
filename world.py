import random
import pygame
from colors import colors
from config import WIDTH, HEIGHT

class World:
    def __init__(self, food_count, danger_count):
        self.food_locations = []
        for food in range(food_count):
            self.food_locations.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.danger_locations = []
        for danger in range(danger_count):
            self.danger_locations.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def add_food(self, x=None, y=None):
        if x is None:
            x = random.randint(0, WIDTH)
        if y is None:
            y = random.randint(0, HEIGHT)
        self.food_locations.append((x, y))
        #print(f"Jidlo pridano na pozici {x}, {y}")

    def draw(self, screen):
        for food_location in self.food_locations:
            pygame.draw.circle(screen, colors.ORANGE, food_location, 5)

        for danger_location in self.danger_locations:
            pygame.draw.circle(screen, colors.DARK_RED, danger_location, 5)