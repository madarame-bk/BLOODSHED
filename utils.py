import math
import random
import pygame
from colors import *
from datetime import timedelta

#functions other
def check_collision_food(organism, env):
    for food in env.food_locations:
        #vzdalenost, nevim
        distance = math.sqrt((organism.x - food[0])**2 + (organism.y - food[1])**2)
        if distance < 10:
            organism.energy +=25
            env.food_locations.remove(food)
            #print(f"{organism.name} snedl jidlo!!")
            
def check_collision_danger(organism, env):
    for danger in env.danger_locations:
        distance = math.sqrt((organism.x - danger[0])**2 + (organism.y - danger[1])**2)
        if distance < 10:
            organism.energy -= 25
            #print(f"{organism.name} slapl na hrebik!")

def check_for_reproduction(organism, population):
    if organism.energy >= 150:
        organism.energy -= 60
        
        # Inherit the parent organism's attributes
        new_speed = organism.speed
        new_size = organism.size
        new_lifespan = organism.lifespan
        new_age_factor = organism.age_factor
        new_energy_cost = organism.energy_cost
        new_color = organism.color

        mutation = ""
        
        # Randomly mutate one of the attributes
        mutation = random.randint(1, 5)
        if mutation == 1:
            new_speed += new_speed / 4  
            mutation = "speed"
        elif mutation == 2:
            new_size += new_size / 4  
            mutation = "size"
        elif mutation == 3:
            new_lifespan += new_lifespan / 4  
            mutation = "lifespan"
        elif mutation == 4:
            new_age_factor += new_age_factor / 4 
            mutation = "age factor"
        elif mutation == 5:
            new_energy_cost += new_energy_cost / 4 
            mutation = "energy cost" 
        
        # Add evolved offspring to pupulation
        population.append(type(organism)(
            organism.x, organism.y, 
            speed=new_speed, 
            size=new_size, 
            lifespan=new_lifespan, 
            age_factor=new_age_factor, 
            energy_cost=new_energy_cost, 
            color=new_color
        ))
        print(f"{organism.name} se rozmnozil s {mutation}!")

def zpocitejorganismy(population, organismus):
    return sum(1 for organism in population if isinstance(organism, organismus))

def vykreslicisloorganismu(population, organismus, nazev, sc, x,y):
    font= pygame.font.SysFont("Arial", 20)
    org_text = font.render(f"{nazev}: {zpocitejorganismy(population, organismus)}", True, colors.GREEN)  # Create a surface with the time
    sc.blit(org_text, (x, y))  # Draw the text at position (10, 10)

def format_second(seconds):
    td=timedelta(seconds=seconds)
    return str(td)