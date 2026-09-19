from src.Creature import Creature, Cow, Wolf, Grass
import numpy as np

class Board:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        Board.size_x = size_x
        Board.size_y = size_y
        self.locations = {}
        self.creature_registry = {}
        self.locations_by_id = {}
        self.smell_map = np.zeros((size_y, size_x)) # gitter mit 0.0 für jeden eintrag des boards


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
        x_within_bounds = x >= 0 and x < Board.size_x
        y_within_bounds = y >= 0 and y < Board.size_y

        return x_within_bounds and y_within_bounds


    @staticmethod
    def is_fail_bounds(position):
        return not Board.is_valid_bounds(position)


    def analyse(self, creature, radius):
        x, y = self.locations_by_id[creature.id]
        relative_positions = {}
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if Board.is_valid_bounds((i, j)) and (i, j) in self.locations:
                    ids = self.locations[(i, j)]
                    cell = [self.creature_registry[id] for id in ids]
                    if (i, j) == (x, y):
                        cell = creature.withyou(cell)
                    relative_position = (i - x, j - y)
                    relative_positions[relative_position] = cell
        return relative_positions

    def smell_at(self, position):
        x, y = position
        return self.smell_map[y, x]

    def find_neighbors(self, x, y):
        possible_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(x + dx, y + dy) for dx, dy in possible_directions]

    def analyse_smell_surroundings(self, creature, radius=1):
        x, y = self.locations_by_id[creature.id]
        neighbors = self.find_neighbors(x, y)
        local_smells = {}
        for neighbor in neighbors:
            if Board.is_valid_bounds(neighbor):
                local_smells[neighbor] = self.smell_at(neighbor)
        return local_smells

    def tick(self):
        """
        Main functionality of Board, all actions happen here
        """
        # phase 0 gerüche halbieren
        self.smell_map *= 0.5 # evtl npch eigene funktion hierfür
        # phase 1 umgebung analysieren
        self.get_surroundings()
        self.movement()
        # kühe senden geruch ab
        self.emit_smell()
        self.interact()
        # geruch verteilt sich
        self.smell_map = self.propagate_smells()
        self.remove_the_dead()


    def interact(self):
        for position, ids in self.locations.items():
            cell = []
            for id in ids:
                cell.append(self.creature_registry[id])
            for creature in cell:
                if isinstance(creature, Wolf):
                    creature.hunt(cell)
                if isinstance(creature, Cow):
                    creature.eat(cell)

    def emit_smell(self):
        for creature in self.creature_registry.values():
            if isinstance(creature, Cow):
                x, y = self.locations_by_id[creature.id]
                self.smell_map[y, x] += 100


    def remove_the_dead(self):
        dead = [creature for creature in self.creature_registry.values() if creature.hp <= 0]
        for creature in dead:
            self.remove_creature(creature)


    def movement(self):
        creatures_to_move = list(self.creature_registry.values())
        for creature in creatures_to_move:
            current_position = self.locations_by_id[creature.id]
            new_position = creature.move_request(current_position)

            # check ob neue position gültig ist, sonst nicht dahin bewegen
            if (new_position != current_position) and Board.is_valid_bounds(new_position):
                new_x, new_y = new_position
                self.move_creature(creature, new_x, new_y)


    def get_surroundings(self):
        """
        calculate surronding for each cow, calculate smells around each wolf
        """
        for creature in self.creature_registry.values():
            if isinstance(creature, Cow):
                surroundings = self.analyse(creature, 4)
                creature.compute_environment(surroundings)

        for creature in self.creature_registry.values():
            if isinstance(creature, Wolf):
                local_smells = self.analyse_smell_surroundings(creature, 1)
                creature.compute_smell_environment(local_smells)


    def propagate_smells(self):
        # für jede einzelne zelle 1x pro tick schauen (4 er Umgebung, also nicht diagonal)
        old_smells = self.smell_map.copy()
        new_smells = self.smell_map.copy()

        # 1. Bedingung prüfen: Ist die Quelle stärker als das Ziel? (von stärker riechender zelle aus gesehen)
        mask_down = old_smells[:-1, :] > old_smells[1:, :]  # Von oben nach unten
        mask_up = old_smells[1:, :] > old_smells[:-1, :]  # Von unten nach oben
        mask_right = old_smells[:, :-1] > old_smells[:, 1:]  # Von links nach rechts
        mask_left = old_smells[:, 1:] > old_smells[:, :-1]  # Von rechts nach links

        # 2. Propagieren: Nur wo die Maske True ist, bekommt die Nachbarzelle 1/4 des Geruchs[cite: 1]
        # np.where(Bedingung, Wert_wenn_wahr, Wert_wenn_falsch)
        prop_down = np.where(mask_down, old_smells[:-1, :] / 4, 0)
        prop_up = np.where(mask_up, old_smells[1:, :] / 4, 0)
        prop_right = np.where(mask_right, old_smells[:, :-1] / 4, 0)
        prop_left = np.where(mask_left, old_smells[:, 1:] / 4, 0)

        new_smells[1:, :] += prop_down
        new_smells[:-1, :] += prop_up
        new_smells[:, 1:] += prop_right
        new_smells[:, :-1] += prop_left

        return new_smells
        # decay -> emission -> propagate smell