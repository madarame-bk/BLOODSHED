import pygame
import random
import math
import time

pygame.init()

WIDTH = 800
HEIGHT = 600
lol = "lol"

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THERE WILL BE BLOODSHED")

class colors:
    WHITE = (255,255,255)
    GREEN = (0,255,0)
    RED = (255,0,0)
    BLUE = (0,0,255)
    PINK = (255,0,255)
    YELLOW = (255,255,0)
    CYAN = (0,255,255)
    ORANGE = (255,165,0)
    PURPLE = (128,0,128)
    BROWN = (165,42,42)
    BLACK = (0,0,0)
    NEON_GREEN = (57,255,20)
    NEON_BLUE = (20,57,255)
    NEON_PINK = (255,20,57)
    NEON_YELLOW = (255,255,20)
    NEON_RED = (255,20,20)
    LIGHT_BLUE = (173,216,230)
    LIGHT_GREEN = (144,238,144)
    LIGHT_YELLOW = (255,255,224)
    LIGHT_PINK = (255,182,193)
    LIGHT_PURPLE = (221,160,221)
    LIGHT_ORANGE = (255,228,196)
    LIGHT_BROWN = (210,105,30)
    LIGHT_CYAN = (224,255,255)
    LIGHT_RED = (255,192,203)
    LIGHT_BLACK = (105,105,105)
    CRIMSON = (220,20,60)
    DARK_RED = (139,0,0)
    DARK_GREEN = (0,100,0)
    DARK_BLUE = (0,0,139)
    DARK_YELLOW = (255,215,0)
    DARK_PINK = (199,21,133)
    DARK_PURPLE = (148,0,211)
    DARK_ORANGE = (255,140,0)
    DARK_BROWN = (139,69,19)
    DARK_CYAN = (0,139,139)
    DARK_BLACK = (0,0,0)
    GRAY = (128,128,128)
    LIGHT_GRAY = (211,211,211)
    DARK_GRAY = (169,169,169)
    SILVER = (192,192,192)
    GOLD = (255,215,0)
    BRONZE = (205,127,50)
    COPPER = (184,115,51)
    BRASS = (181,166,66)
    STEEL = (176,196,222)
    IRON = (183,187,191)
    TITANIUM = (167,169,172)
    PLATINUM = (229,228,226)
    DIAMOND = (185,242,255)
    EMERALD = (0,201,87)
    SAPPHIRE = (15,82,186)
    RUBY = (224,17,95)
    AMETHYST = (153,102,204)
    TOPAZ = (255,204,102)
    AQUAMARINE = (127,255,212)
    PERIDOT = (75,255,100)
    GARNET = (115,54,53)
    OPAL = (168,195,188)
    PEARL = (234,224,200)
    JADE = (0,168,107)
    ONYX = (53,56,57)
    BLOODSTONE = (111,11,11)
    MOONSTONE = (200,200,200)
    SUNSTONE = (255,166,77)
    STARSTONE = (0,0,0)
    COMETSTONE = (255,255,255)
    ASTEROIDSTONE = (128,128,128)
    METEORITE = (169,169,169)

class Organism:
    def __init__(self, x, y, speed, size, lifespan):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.speed = speed
        self.size = size
        self.lifespan = lifespan
        self.age = 0
        self.age_factor = 1
        self.energy = 100
        self.energy_cost = 0.1
        self.direction = random.uniform(0, 2* math.pi)
        self.color = colors.BLACK

    def move(self):
        #random.uniform vrati random CISLO ne integer v rozsahu
        #toto efektivne vraci uhel v radianech
        

        #cos pro dany uhel urcuje pohyb horizontalne
        ax = math.cos(self.direction) * self.speed
        #sin vertikalne 
        #0 -> nehybe se, 1 nebo -1 hybe se v pravem uhlu
        ay = math.sin(self.direction) * self.speed

        #
        self.x += ax
        self.y += ay

        #zajistí, že nevyjede mimo screen
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

        self.energy -= self.energy_cost

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

class World:
    def __init__(self, food_count, danger_count):
        self.food_locations = []
        for food in range(food_count):
            self.food_locations.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.danger_locations = []
        for danger in range(danger_count):
            self.danger_locations.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def draw(self, screen):
        for food_location in self.food_locations:
            pygame.draw.circle(screen, colors.ORANGE, food_location, 5)

        for danger_location in self.danger_locations:
            pygame.draw.circle(screen, colors.DARK_RED, danger_location, 5)


def check_collision_food(organism, env):
    for food in env.food_locations:
        distance = math.sqrt((organism.x - food[0])**2 + (organism.y - food[1])**2)
        if distance < 10:
            organism.energy += 25
            env.food_locations.remove(food)

env=World(food_count=30, danger_count=5)
population = []

class Lizard(Organism):
    def __init__(self, x, y):
        super().__init__(x,y, speed=random.uniform(2,4), size=4, lifespan = 100)
        self.direction=random.uniform(0,2*math.pi)
        self.color = colors.DARK_GREEN
    def update(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        if random.random() < 0.05:
            self.direction=random.uniform(0,2*math.pi)


class Dinosaur(Organism):
    def __init__(self, x, y):
        super().__init__(x,y, speed=random.uniform(2,4), size=8, lifespan=100)
        self.energy_cost = 0.15
        self.color = colors.DARK_BLUE
    
    
    def update(self, objects):
        if random.random() < 0.01:
            f = self.find_nearest_object(objects)
            if f is not None:
                angle = math.atan2(f[1] - self.y, f[0] - self.x)
                self.direction = angle
 

#main

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)  # Choose a font and size


for i in range(5):
    population.append(Dinosaur(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    population.append(Lizard(random.randint(0, WIDTH), random.randint(0,HEIGHT)))

start_time = time.time()
last_time = start_time
time_interval = 5

running = True
clock = pygame.time.Clock()

while running:
    #vybarvi obrazovku bilou
    sc.fill(colors.WHITE)

    #vytvori prostredi (jidlo, nebezpeci)
    env.draw(sc)

    #hodiny
    time_surface = font.render(f"{int(time.time()-start_time)}", True, colors.GREEN)  # Create a surface with the time
    sc.blit(time_surface, (10, 10))  # Draw the text at position (10, 10)

    for organism in population:
        if organism.is_alive():
            if time.time() - last_time > time_interval:
                organism.age += organism.age_factor
                last_time = time.time()

            if isinstance(organism, Dinosaur):
                organism.update(env.food_locations)
            else:
                organism.update()
            organism.move()
            organism.draw(sc)
            check_collision_food(organism, env)

    pygame.display.flip()

    clock.tick(30)

    #zavreni okna
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
    




