class Creature:
    counter = 0
    def __init__(self, name, start_hp):
        self.name = name
        self.hp = start_hp
        self.id = Creature.counter
        Creature.counter += 1

    def __eq__(self, other):
        if isinstance(other, Creature):
            return self.id == other.id
        else:
            return False

class Plant(Creature):
    pass
class Grass(Plant):
    def __init__(self, name):
        super().__init__(name, 50)

class Animal(Creature):
    pass

class Herbivore(Animal):
    pass

class Carnivore(Animal):
    pass

class Cow(Herbivore):
    def __init__(self, name):
        super().__init__(name, 200)

class Wolf(Carnivore):
    def __init__(self, name):
        super().__init__(name, 100)

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


"""
def main():
    wolf1 = Wolf('wolf1')
    print(wolf1.name)
    print(wolf1.hp)
    print(wolf1.id)

    wolf2 = Wolf('wolf2')
    print(wolf1.__eq__(wolf2))
    print(wolf1 == wolf2)  # ist genau wie __eq__

    creature1 = Creature('creature1', 100)
    creature2 = Creature('creature2', 100)
    print(wolf1 == creature1)
    print(creature1 == creature2)

    # true:
    print(wolf1 == wolf1)

if __name__ == '__main__':
    main()
"""