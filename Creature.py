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

    def move_request(self, current_position):
        return self.random_move_request(current_position) # to be implemented for each animal


class Plant(Creature):

    def eaten(self):
        self.hp = max(self.hp - 5, 0)

    def move_request(self, current_position):
        return current_position # gras doesnt move

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
        self.surroundings = {}

    def eat(self, cell):
        other_creatures = self.withyou(cell)
        for plant in other_creatures:
            if isinstance(plant, Plant):
                self.hp = min(self.hp + 10, self.start_hp*2 )
                plant.eaten()
                break

    def compute_environment(self, surroundings):
        self.surroundings = surroundings


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

