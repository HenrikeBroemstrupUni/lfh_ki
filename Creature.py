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

    def random_move_request(self, current_position):
        x, y = current_position
        dx =  random.randint(-1, 1)
        dy =  random.randint(-1, 1)
        new_position = (x + dx, y + dy)
        return new_position


class Plant(Creature):

    def eaten(self):
        self.hp = max(self.hp - 5, 0)

class Grass(Plant):
    def __init__(self, name):
        super().__init__(name, 50)


class Animal(Creature):
    def eaten(self):
        self.hp = 0   # nach hp <= 0 checken bei Tick um tote Tiere zu entfernen

class Herbivore(Animal):
    pass

class Carnivore(Animal):
    pass

class Cow(Herbivore):
    def __init__(self, name):
        super().__init__(name, 200)
        self.start_hp = self.hp

    def eat(self, cell):
        other_creatures = self.withyou(cell)
        for plant in other_creatures:
            if isinstance(plant, Plant):
                self.hp = min(self.hp + 10, self.start_hp*2 )
                plant.eaten()
                break

class Wolf(Carnivore):
    def __init__(self, name):
        super().__init__(name, 100)
        self.start_hp = self.hp


    def hunt(self, cell):
        other_creatures = self.withyou(cell)
        for cow in other_creatures:
            if isinstance(cow, Cow):
                self.hp = min(self.hp +50, self.start_hp*2)
                cow.eaten() # hier die Kuh töten
                break # nur die erste kuh fressen



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