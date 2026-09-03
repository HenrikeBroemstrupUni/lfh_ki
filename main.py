import time
import os
import random
from Board import Board
from Creature import Cow, Wolf, Grass


def main():
    board = Board(80, 24)
    speed = 0.3

    animals = [
        # ursprüngliche
        [Cow(name="muh"), 0, 0],
        [Wolf(name="boeser"), 1, 2],
        [Cow(name="muh2"), 5, 0],
        [Wolf(name="rudel"), 40, 10],
        [Grass(name="g"), 10, 20],
        [Cow(name="muh3"), 60, 5],
        [Cow(name="muh4"), 20, 15],
        [Cow(name="muh5"), 35, 8],
        [Cow(name="muh6"), 70, 18],
        [Grass(name="g2"), 15, 20],
        [Grass(name="g3"), 16, 20],
        [Grass(name="g4"), 25, 5],
        [Grass(name="g5"), 50, 12],
        [Grass(name="g6"), 55, 12],
        [Grass(name="g7"), 2, 2],
        [Grass(name="g8"), 3, 3],

        # garantierte Kollisionen für sofortiges Testen im ersten Tick
        [Wolf(name="direkt_wolf"), 30, 10],
        [Cow(name="direkt_kuh"), 30, 10],  # Wolf frisst Kuh sofort (gleiche Position)

        [Cow(name="gras_kuh"), 45, 15],
        [Grass(name="gras_ziel"), 45, 15],  # Kuh frisst Gras sofort (gleiche Position)

        [Wolf(name="hungrig1"), 55, 3],
        [Cow(name="opfer1"), 55, 3],
        [Cow(name="opfer2"), 55, 3],  # zwei Kühe gleichzeitig -> testet "nur 1 pro Tick"

        # weitere verteilte Kreaturen
        [Wolf(name="lonewolf"), 65, 20],
        [Cow(name="muh7"), 10, 5],
        [Cow(name="muh8"), 25, 20],
        [Grass(name="g9"), 60, 8],
        [Grass(name="g10"), 60, 9],
        [Wolf(name="patrol"), 70, 2],
        [Cow(name="muh9"), 38, 18],
        [Grass(name="g11"), 5, 10],
    ]

    for animal, x, y in animals:
        board.place_creature(animal, x, y)

    for step in range(90):
        os.system('clear')
        board.draw()
        time.sleep(speed)
        board.tick()


if __name__ == "__main__":
    main()
