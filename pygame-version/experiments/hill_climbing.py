def calculate_smell(x, y):
    smell = -(x - 5) ** 2 - (y - 5) ** 2  # soll lokale maxima haben
    return smell


def hill_climbing(start_x, start_y):
    current_x, current_y = start_x, start_y
    smell = calculate_smell(start_x, start_y)

    possible_movements = find_neighbors(current_x, current_y)
    # has_improved = False

    for movement in possible_movements:
        new_smell = calculate_smell(movement[0], movement[1])
        if new_smell > smell:
            smell = new_smell
            current_x, current_y = movement
            # has_improved = True

    return current_x, current_y



# Auch diagonal laufen!
def find_neighbors(x, y):
    possible_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(x + dx, y + dy) for dx, dy in possible_directions]


"""
function HILL-CLIMBING(problem):
    current ← MAKE-NODE(INIT-STATE[problem])

    loop:
        next ← HIGHEST-VALUE-SUCCESSOR(current)

        if VALUE(next) ≤ VALUE(current):
            return current

        current ← next 
"""


def main():
    print(hill_climbing(start_x=0, start_y=0))
    print(hill_climbing(start_x=10, start_y=10))
    print(hill_climbing(start_x=20, start_y=20))
    print(hill_climbing(start_x=30, start_y=30))
    print(hill_climbing(start_x=40, start_y=40))


if __name__ == '__main__':
    main()
