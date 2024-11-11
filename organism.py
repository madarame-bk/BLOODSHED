from colors import colors
import random
import math
import pygame
from config import WIDTH, HEIGHT

class Organism:
    def __init__(self, x, y, speed=2, size=5, lifespan=100, age_factor=1, energy_cost=0.1, color=colors.BLACK):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.speed = speed
        self.size = size
        self.lifespan = lifespan
        self.age = 0
        self.age_factor = age_factor
        self.energy = 100
        self.energy_cost = energy_cost
        self.direction = random.uniform(0, 2* math.pi)
        self.color = color

    def move(self, delta_time=1, speed_multiplier=1):
        #random.uniform vrati random CISLO ne integer v rozsahu
        #toto efektivne vraci uhel v radianech
        

        #cos pro dany uhel urcuje pohyb horizontalne
        ax = math.cos(self.direction) * self.speed*delta_time*speed_multiplier
        #sin vertikalne 
        #0 -> nehybe se, 1 nebo -1 hybe se v pravem uhlu
        ay = math.sin(self.direction) * self.speed*delta_time*speed_multiplier

        #
        self.x += ax
        self.y += ay

        #zajistí, že nevyjede mimo screen
        """self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))"""
        if self.x > WIDTH or self.x < 0:
            self.direction = math.pi - self.direction
        if self.y > HEIGHT or self.y < 0:
            self.direction = -self.direction



        self.energy -= self.energy_cost*delta_time*speed_multiplier

        self.position=(self.x,self.y)

    #stazene, ted neresim!!
    def distance_to(self, other_position):
        # Calculate Euclidean distance to another position
        return math.sqrt((self.position[0] - other_position[0]) ** 2 + 
                         (self.position[1] - other_position[1]) ** 2)
    
    def find_nearest_object(self, objects):
        nearest_object = None
        nearest_distance = (math.inf)

        for obj in objects:
            distance = self.distance_to(obj)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_object = obj

        return nearest_object
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def is_alive(self):
        return self.energy > 0 and self.age < self.lifespan
    

#ORGANISMY

class Lizard(Organism):
    def __init__(self, x, y, speed=random.uniform(15,20), size=4, lifespan=100, age_factor=1, energy_cost=0.1, color=colors.DARK_GREEN):
        super().__init__(x,y, speed, size, lifespan, age_factor, energy_cost, color)
        self.name="Lizard"
        self.direction=random.uniform(0,2*math.pi)
        self.color = colors.DARK_GREEN
        
    def update(self, delta_time, ):
        self.x += math.cos(self.direction) * self.speed*delta_time
        self.y += math.sin(self.direction) * self.speed*delta_time
        if random.random() < 0.05:
            self.direction=random.uniform(0,2*math.pi)


class Dinosaur(Organism):
    def __init__(self, x, y, speed=random.uniform(10,15), size=8, lifespan=100, age_factor=1, energy_cost=0.15, color=colors.DARK_BLUE):
        super().__init__(x,y, speed, size, lifespan, age_factor, energy_cost, color)
        self.name="Dinosaur"
        self.color = colors.DARK_BLUE
    
    
    def update(self, objects, delta_time):
        if random.random() < 0.01:
            f = self.find_nearest_object(objects)
            if f is not None:
                angle = math.atan2(f[1] - self.y, f[0] - self.x)
                self.direction = angle
