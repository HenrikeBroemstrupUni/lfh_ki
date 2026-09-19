# Author: CG
# Butchered by: OL

# Imports
import random
from time import sleep
import pygame

pygame.init()
screen = pygame.display.set_mode([1400, 1000])

tilesize = 16
margin = 1

tickrate = 10
tick = 1

mapsize_x = 80
#mapsize_y = 24
mapsize_y = 50

# Heatmaps
maxval = 100
decayrate = 0.03
heatmap = {}
coldmap = {}

roundlog = []

# Create an empty heatmap with zeroes or overwriting existing heatmaps with zeroes
def dict_null(dict):
    for row in range(0, mapsize_y+1):
        for column in range(0, mapsize_x+1):
            dict[(column, row)] = 0

dict_null(heatmap)
dict_null(coldmap)

# Decay the heatmap every tick
def dict_decay(dict):
    for row in range(0, mapsize_y+1):
        for column in range(0, mapsize_x+1):
            dict[(column, row)] = dict[(column, row)]*(1-decayrate)

            # Optional: Regard values under x as gone
            # Otherwise the cells are calculated infinitely (we're using floats here, it never gets 0)
            if dict[(column, row)] <= 10.0 and dict[(column, row)] > 0: dict[(column, row)] = 0.0


class Creature:
    name= ""

    def WithYou(entity, index):
        return None
    
    def __init__(self):
        Id = "test"
        self.hp = 0

class Animal(Creature):
    Id = "test"

    def RandomMoveRequest(entity, index):
        return None

    def run_or_hunt(entity, index):
        return None
    
class Plant(Creature):
    name = "plant"

    # Image
    img = pygame.image.load("../pictures/plant.png")
    img = pygame.transform.scale(img,(tilesize,tilesize))

    def __init__(self):
        Id = "test"
        self.hp = 50
        self.posx = random.randint(1, mapsize_x)
        self.posy = random.randint(1, mapsize_y)

class Cow(Animal):
    name = "cow"
    radius = 10
    sensitivity = 10
    run = True
    hunt = False

    # Image
    img = pygame.image.load("../pictures/cow.png")
    img = pygame.transform.scale(img,(tilesize,tilesize))

    def __init__(self):
        Id = "test"
        self.hp = 200
        self.hp_max = 400
        self.posx = random.randint(1, mapsize_x)
        self.posy = random.randint(1, mapsize_y)

class Wolf(Animal):
    name = "wolf"
    radius = 8
    sensitivity = 50
    run = False
    hunt = True

    # Image
    img = pygame.image.load("../pictures/wolf.png")
    img = pygame.transform.scale(img,(tilesize,tilesize))

    def __init__(self):
        Id = "test"
        self.hp = 100
        self.hp_max = 200
        self.posx = random.randint(0, mapsize_x)
        self.posy = random.randint(0, mapsize_y)

# Helper functions
def clamp(num, min_value, max_value):
        num = max(min(num, max_value), min_value)
        return num

# Define the map
Map=[Cow(), Cow(), Cow(), Plant(), Plant(), Cow(), Wolf(), Wolf(), Cow(), Cow(), Cow(), Plant(), Plant(), Cow(), Wolf(), Wolf(), Cow(), Cow(), Cow(), Plant(), Plant(), Cow(), Wolf(), Wolf(), Cow(), Cow(), Cow(), Plant(), Plant(), Cow(), Wolf(), Wolf()]

# Notes: https://stackoverflow.com/questions/55617119/how-would-i-make-a-heatmap-in-pygame-on-a-grid

font = pygame.font.SysFont('arial', 14)
color = (50, 50, 50)

running = True
while running:

    # Events
    for event in pygame.event.get():
        # Close event
        if event.type == pygame.QUIT:
            running = False

    # Helper functions for drawing to specific positions
    def draw_objects(object, x, y):
        screen.blit(object.img,((margin + tilesize) * (y) + margin, (margin + tilesize) * (x) + margin))
    def draw_text(content, x, y):
        text = font.render(content, True, (255,255,255))
        screen.blit(text, [(margin + tilesize) * (y) + margin,(margin + tilesize) * (x) + margin])

    # Draw the grid
    def create_map():
        # Background
        screen.fill((0,0,0))

        for row in range(0, mapsize_y):
            for column in range(0, mapsize_x):

                pygame.draw.rect(screen,
                                color,
                                [(margin + tilesize) * column + margin,
                                (margin + tilesize) * row + margin,
                                tilesize,
                                tilesize])

    # Create heatmap
    def make_heatmap():
        # Variant 2: With decay
        dict_decay(heatmap)
        dict_decay(coldmap)

        # Draw the map
        for entity in Map:
            print(entity.name) # do something more clever?

        # For every item in the coldmap draw it
        for i in coldmap:
            s = pygame.Surface((tilesize,tilesize), pygame.SRCALPHA)
            s.fill((0,0,255,coldmap[(i[0], i[1])]*0.01*255))
            screen.blit(s, ((margin + tilesize) * (i[0]) + margin, (margin + tilesize) * (i[1]) + margin))
            # Or pygame.HWSURFACE for acceleration

    # Draw the creatures
    def make_creatures():
        for row in range(0, mapsize_y):
            for column in range(0, mapsize_x):

                # Find all the entities on the tile
                found = []
                for entity in Map:
                    if entity.posx == column and entity.posy == row:
                        found.append(entity)

                # Case 1: No entity on the tile
                if len(found) == 0:
                    pass
                # Case 2: One entity on the tile
                elif len(found) == 1:
                    draw_objects(found[0], row, column)
                # Case 3: Multiple entities on the tile
                else:
                    draw_text(str(len(found)), row, column)

    tick = 0

    # Run calculations per tick
    while True:

        # Draw the map
        create_map()

        # Draw heatmap
        make_heatmap()

        # Draw the creatures
        make_creatures()

        # Draw the screen
        pygame.display.flip()

        # Tickrate
        sleep(1/tickrate)

        # Clear the roundlog (for fast tickrates only every nth tick)
        if tickrate > 1:
            tick += 1
            if tick >= tickrate * 2:
                roundlog.clear()
                tick = 1
        else:
            roundlog.clear()

        # Calculate the actions
        for index, i in enumerate(Map):
            if i.__class__.__name__ == "Cow":
                # Movement
                Animal.RandomMoveRequest(i, index)
            
            if i.__class__.__name__ == "Wolf":
                # Hunt
                Animal.run_or_hunt(i, index)

            # Tile awareness 
            Creature.WithYou(i, index)

# Quit
pygame.quit()
