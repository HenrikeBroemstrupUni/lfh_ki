def calculate_smell(x, y):
    smell = -(x-5)**2 - (y-5)**2    # soll lokale maxima haben
    return smell

def hill_climbing(start_x, start_y):
    current_x, current_y = start_x, start_y
    smell = calculate_smell(start_x, start_y)

    while True:
        possible_movements = find_neighbors(current_x, current_y)
        has_improved = False

        for movement in possible_movements:
            new_smell = calculate_smell(movement[0], movement[1])
            if new_smell > smell:  # führt einer der 4 möglichen schritte zur verbeserung des smells?
                smell = new_smell
                current_x, current_y = movement
                has_improved = True

        if not has_improved:
            return current_x, current_y

def find_neighbors(x, y):
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

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

