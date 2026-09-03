import os
from Creature import Creature, Cow, Wolf, Grass

class Board():
    # dict 80 * 24 zellen.
    def __init__(self, size_x, size_y):
        Board.size_x = size_x # 0 bis 79
        Board.size_y = size_y # 0 bis 23
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
        if Board.is_fail_bounds((position_x, position_y)):
            raise ValueError(f"Position ({position_x}, {position_y}) liegt außerhalb des Boards")

    @staticmethod
    def is_valid_bounds(position):
        x, y = position
        x_within_bounds = x >= 0 and x < Board.size_x # true or false
        y_within_bounds = y >= 0 and y < Board.size_y

        return x_within_bounds and y_within_bounds

    @staticmethod
    def is_fail_bounds(position):
        return not Board.is_valid_bounds(position)


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


    def tick(self):
        # phase 1 movement
        creatures_to_move = list(self.creature_registry.values())
        for creature in creatures_to_move:
            if isinstance(creature, Grass):
                continue # gras bewegt sich nicht

            current_position = self.locations_by_id[creature.id]
            new_position = creature.random_move_request(current_position)

            # check ob neue position gültig ist, sonst nicht dahin bewegen
            if Board.is_valid_bounds(new_position):
                new_x, new_y = new_position
                self.move_creature(creature, new_x, new_y)

        # phase 2 for interaction, zb eating
        for position, ids in self.locations.items():
            cell = []
            for id in ids:
                cell.append(self.creature_registry[id])
            for creature in cell:
                if isinstance(creature, Wolf):
                    creature.hunt(cell)
                if isinstance(creature, Cow):
                    creature.eat(cell)

        # phase 3 remove the dead
        dead = [creature for creature in self.creature_registry.values() if creature.hp <= 0]
        for creature in dead:
            self.remove_creature(creature)
