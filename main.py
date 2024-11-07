import pygame
import random
import math
import time

from config import WIDTH, HEIGHT
from colors import colors
from organism import Organism, Lizard, Dinosaur
from world import World
from utils import *

pygame.init()



sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THERE WILL BE BLOODSHED")

env=World(food_count=30, danger_count=5)
population = []

#main

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)  # Choose font

density_factor=0.00001
start_density=HEIGHT*WIDTH*density_factor

for i in range(int(start_density)):
    population.append(Dinosaur(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    population.append(Lizard(random.randint(0, WIDTH), random.randint(0,HEIGHT)))

start_time = time.time()
last_time = 0
time_interval = 5

simulation_time = 0

speed_multiplier = 1  # Normal speed
fast_speed_multiplier = 500  # Fast speed (you can adjust this)
is_fast = False  # Toggle flag

def toggle_speed():
    print("toggled")
    global is_fast, speed_multiplier
    if is_fast:
        speed_multiplier = 1  # Set back to normal speed
        is_fast = False
    else:
        speed_multiplier = fast_speed_multiplier  # Set to fast speed
        is_fast = True


running = True
clock = pygame.time.Clock()

offscreen=[]

while running:
    #vybarvi obrazovku bilou
    sc.fill(colors.WHITE)

    #vytvori prostredi (jidlo, nebezpeci)
    env.draw(sc)

    delta_time = clock.get_time()/1000 #/1000 protoze get time vrati cas od zacatku sim v milisekundach
    simulation_time += delta_time * speed_multiplier

    

    

    current_time=pygame.time.get_ticks()
    for organism in population:
        if organism.is_alive():
            if simulation_time - last_time > time_interval: #na milisekundy *1000
                #print(f"cas mezi: {simulation_time - last_time}")
                organism.age += organism.age_factor *delta_time*speed_multiplier
                for i in range(5):
                    env.add_food()
                last_time = simulation_time

            if isinstance(organism, Dinosaur):
                organism.update(env.food_locations, delta_time=delta_time, speed_multiplier=speed_multiplier)
            else:
                organism.update(delta_time=delta_time, speed_multiplier=speed_multiplier)
            organism.move(delta_time=delta_time, speed_multiplier=speed_multiplier)
            organism.draw(sc)
            check_collision_food(organism, env)
            check_collision_danger(organism, env)
            check_for_reproduction(organism, population)
            if organism.position[0] < -5 or organism.position[0] > WIDTH+5 or organism.position[1] < -5 or organism.position[1] > HEIGHT+5:
                offscreen.append(organism)
            if organism in offscreen:
                if organism.position[0] > -5 or organism.position[0] < WIDTH+5 or organism.position[1] > -5 or organism.position[1] < HEIGHT+5:
                    offscreen.remove(organism)

        else:
            population.remove(organism)
            print(f"Organism {organism.name} died at age {organism.age}")

    #UI

    print(f"organismu: {len(population)}")

    font= pygame.font.SysFont("Arial", 30)

    #hodiny
    if speed_multiplier == 1:
        time_text = font.render(f"Čas: {format_second(int(simulation_time))}", True, colors.GREEN)  # Create a surface with the time
        sc.blit(time_text, (10, 10))  # Draw the text at position (10, 10)
    else:
        time_text = font.render(f"Čas: {format_second(int(simulation_time))}", True, colors.BLUE)  # Create a surface with the time
        sc.blit(time_text, (10, 10))  # Draw the text at position (10, 10)

    #fps
    fps_text = font.render(f"fps:{int(clock.get_fps())}", True, colors.GREEN)  # Create a surface with the time
    sc.blit(fps_text, (700, 10))  # Draw the text at position (10, 10)

    #kolik organismu
    organism_text = font.render(f"Ogranismu: {len(population)}", True, colors.GREEN)  # Create a surface with the time
    sc.blit(organism_text, (10, 40))  # Draw the text at position (10, 10)

    vykreslicisloorganismu(population, Dinosaur, "Dinosauru", sc, 20, 70)
    vykreslicisloorganismu(population, Lizard, "Lizardu", sc, 20, 85)

    #offscreen
    offscreen_text = font.render(f"offscreen: {len(offscreen)}", True, colors.RED)  # Create a surface with the time
    sc.blit(offscreen_text, (300, 10))  # Draw the text at position (10, 10)


    

    """#kolik dinosauru
    org_text = font.render(f"Dinosauru: {zpocitejorganismy(population, Dinosaur)}", True, colors.GREEN)  # Create a surface with the time
    sc.blit(org_text, (10, 70))  # Draw the text at position (10, 10)

    #kolik lizardu
    org_text = font.render(f"Lizardu: {zpocitejorganismy(population, Lizard)}", True, colors.GREEN)  # Create a surface with the time
    sc.blit(org_text, (10, 85))  # Draw the text at position (10, 10)"""

    pygame.display.flip()

    clock.tick(60)



    #zavreni okna
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_speed()


pygame.quit()
    



