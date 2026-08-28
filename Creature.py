import random
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

    def withyou(self, cell):
        other_creatures = []
        for other in cell:
            if other == self:
                continue
            else:
                other_creatures.append(other)
        return other_creatures

    def random_move_request(self):
        dx =  random.randint(-1, 1)
        dy =  random.randint(-1, 1)
        return dx, dy

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