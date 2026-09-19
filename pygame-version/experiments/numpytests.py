import numpy as np


smells = np.array([
    [0, 0, 100, 0, 0, 0],
    [0, 40, 0, 0, 0, 100],
    [0, 0, 0, 0, 0, 0]
], dtype=float)

def propagate_smells(smells):
    old_smells = smells.copy()
    results = smells.copy()
    for y in range(smells.shape[0]):
        for x in range(smells.shape[1]):
            # print(x, y, smells[x, y])
            current_smell = old_smells[y, x]

            down = y + 1
            up = y - 1
            left = x - 1
            right = x + 1

            if down < smells.shape[0]:
                neighbor = old_smells[down, x]
                if neighbor > current_smell:
                    results[y, x] += neighbor / 4

            if up >= 0:
                neighbor = old_smells[up, x]
                if neighbor > current_smell:
                    results[y, x] += neighbor / 4

            if left >= 0:
                neighbor = old_smells[y, left]
                if neighbor > current_smell:
                    results[y, x] += neighbor / 4

            if right < smells.shape[1]:
                neighbor = old_smells[y, right]
                if neighbor > current_smell:
                    results[y, x] += neighbor / 4

    return results


print(propagate_smells(smells))

""" andere optionen, einmal auch mit doppelter schleife, dann mit numpy funktionen"""
import numpy as np
import time

smellmap = np.array([[0, 0, 100, 0, 0, 0],
                     [0, 40, 0, 0, 0, 100],
                     [0, 0, 0, 0, 0, 0]], dtype=float)


def printArr(arr: np.array) -> None:
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            print(f"{arr[y, x]:>6}", end="")
        print("")


def generateTestMap(size_x, size_y):
    map = np.random.choice(np.arange(100, dtype=np.double), size=(size_x, size_y))
    return map


smellmap = generateTestMap(64, 37)


print(smellmap)
print("")


# print(smellmap.shape)


def calcSmell(arr: np.array):
    arrCopy = arr.copy()

    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            # oben
            if y - 1 >= 0:
                if arr[y, x] > arr[y - 1, x]:
                    arrCopy[y - 1, x] += arr[y, x] / 4
                    # unten
            if y + 1 < arr.shape[0]:
                if arr[y, x] > arr[y + 1, x]:
                    arrCopy[y + 1, x] += arr[y, x] / 4
            # links
            if x - 1 >= 0:
                if arr[y, x] > arr[y, x - 1]:
                    arrCopy[y, x - 1] += arr[y, x] / 4
            # rechts
            if x + 1 < arr.shape[1]:
                if arr[y, x] > arr[y, x + 1]:
                    arrCopy[y, x + 1] += arr[y, x] / 4

    return arrCopy


startTime = time.time()
testsmelle = calcSmell(smellmap)
print(f"Time taken: {time.time() -startTime}")
# print(testsmelle)


startTime = time.time()

new_smell = smellmap.copy()

# 1. Bedingung prüfen: Ist die Quelle stärker als das Ziel?
mask_down = smellmap[:-1, :] > smellmap[1:, :]  # Von oben nach unten
mask_up = smellmap[1:, :] > smellmap[:-1, :]  # Von unten nach oben
mask_right = smellmap[:, :-1] > smellmap[:, 1:]  # Von links nach rechts
mask_left = smellmap[:, 1:] > smellmap[:, :-1]  # Von rechts nach links

# 2. Propagieren: Nur wo die Maske True ist, bekommt die Nachbarzelle 1/4 des Geruchs[cite: 1]
# np.where(Bedingung, Wert_wenn_wahr, Wert_wenn_falsch)
prop_down = np.where(mask_down, smellmap[:-1, :] / 4, 0)
prop_up = np.where(mask_up, smellmap[1:, :] / 4, 0)
prop_right = np.where(mask_right, smellmap[:, :-1] / 4, 0)
prop_left = np.where(mask_left, smellmap[:, 1:] / 4, 0)

# print(prop_down)


# 3. Werte eintragen: np.maximum stellt sicher, dass wir den stärksten ankommenden
# Geruch nehmen, falls eine Zelle von mehreren Seiten gleichzeitig Geruch empfängt.
new_smell[1:, :] += prop_down
new_smell[:-1, :] += prop_up
new_smell[:, 1:] += prop_right
new_smell[:, :-1] += prop_left
print(f"Time taken: {time.time() - startTime}")

print(new_smell)

print(f"Same result? : {not (False in (new_smell == testsmelle))}")
