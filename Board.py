import time

from Creature import *
import os

class Board():
    # dict 80 * 24 zellen.
    def __init__(self, size_x, size_y):
        self.size_x = size_x # 0 bis 79
        self.size_y = size_y # 0 bis 23
        self.locations = {}
        self.creature_registry = {}
        self.locations_by_id = {}

    def place_creature(self, creature: Creature, position_x, position_y):
        self.check_boarders(position_x, position_y)
        if (position_x, position_y) not in self.locations:
            self.locations[(position_x, position_y)] = []
        self.locations[(position_x, position_y)].append(creature.id)
        self.creature_registry[creature.id] = creature
        self.locations_by_id[creature.id] = (position_x, position_y)

    def move_creature(self, creature: Creature, position_x: int, position_y: int):
        self.remove_creature(creature)
        self.place_creature(creature, position_x, position_y)

    def remove_creature(self, creature: Creature):
        position_x, position_y = self.locations_by_id.pop(creature.id)
        self.locations[(position_x, position_y)].remove(creature.id)
        self.creature_registry.pop(creature.id)
        if not self.locations[(position_x, position_y)]:
            del self.locations[(position_x, position_y)]

    def check_boarders(self, position_x: int, position_y: int):
        if position_x >= self.size_x or position_x < 0 or position_y >= self.size_y or position_y < 0:
            raise ValueError(f"Position ({position_x}, {position_y}) liegt außerhalb des Boards")


    ### AB HIER TERMINAL AUSGABE ###
    def draw(self):
        os.system('clear')
        for y in range(self.size_y):
            row = ""
            for x in range(self.size_x):
                if (x, y) in self.locations:
                    ids = self.locations[(x, y)]
                    creature = self.creature_registry[ids[0]] # nur die 1. zeichenen fall merhere auf einer stelel
                    if isinstance(creature, Cow):
                        row += "C"
                    if isinstance(creature, Wolf):
                        row += "W"
                    if isinstance(creature, Grass):
                        row += "G"
                else:
                    row += "_"
            print(row)

import time
import os
import random

def main():
    board = Board(80, 24)
    speed = 0.3

    animals = [
        [Cow(name="muh"),     0,  0],
        [Wolf(name="boeser"), 1,  2],
        [Cow(name="muh2"),    5,  0],
        [Wolf(name="rudel"), 40, 10],
        [Grass(name="g"),    10, 20],
        [Cow(name="muh3"), 60, 5]
    ]

    for animal, x, y in animals:
        board.place_creature(animal, x, y)

    for step in range(90):
        os.system('clear')
        board.draw()
        time.sleep(speed)

        for entry in animals:
            animal, x, y = entry
            if isinstance(animal, Grass):
                continue                      # plants stay put

            # random -1, 0 or +1 in each direction
            new_x = x + random.randint(-1, 1)
            new_y = y + random.randint(-1, 1)

            # keep within bounds
            new_x = max(0, min(new_x, 79))
            new_y = max(0, min(new_y, 23))

            board.move_creature(animal, new_x, new_y)
            entry[1], entry[2] = new_x, new_y

if __name__ == "__main__":
    main()