import pygame

from src.Board import Board
from src.BoardRenderer import BoardRenderer
from src.Creature import Cow, Wolf, Grass

TILE_SIZE = 24
MARGIN = 2
TICK_RATE = 3

def create_initial_board():
    board = Board(65, 37)

    animals = [
        [Cow(name="muh"), 0, 0],
        [Wolf(name="boeser"), 1, 2],
        [Cow(name="muh2"), 5, 0],
        [Wolf(name="rudel"), 40, 10],
        [Grass(name="g"), 10, 20],
        [Cow(name="muh3"), 58, 5],
        [Cow(name="muh4"), 20, 15],
        [Cow(name="muh5"), 35, 8],
        [Cow(name="muh6"), 59, 18],
        [Grass(name="g2"), 15, 20],
        [Grass(name="g3"), 16, 20],
        [Grass(name="g4"), 25, 5],
        [Grass(name="g5"), 50, 12],
        [Grass(name="g6"), 55, 12],
        [Grass(name="g7"), 2, 2],
        [Grass(name="g8"), 3, 3],
        [Wolf(name="direkt_wolf"), 30, 10],
        [Cow(name="direkt_kuh"), 30, 10],
        [Cow(name="gras_kuh"), 45, 15],
        [Grass(name="gras_ziel"), 45, 15],
        [Wolf(name="hungrig1"), 55, 3],
        [Cow(name="opfer1"), 55, 3],
        [Cow(name="opfer2"), 55, 3],
        [Wolf(name="lonewolf"), 35, 20],
        [Cow(name="muh7"), 10, 5],
        [Cow(name="muh8"), 25, 20],
        [Grass(name="g9"), 50, 8],
        [Grass(name="g10"), 57, 9],
        [Wolf(name="patrol"), 56, 2],
        [Cow(name="muh9"), 38, 18],
        [Grass(name="g11"), 5, 10],
        [Grass(name="g12"), 50, 36],
        [Grass(name="g13"), 7, 29],
        [Wolf(name="patrol2"), 56, 22],
        [Cow(name="muh10"), 38, 28],
        [Grass(name="g14"), 5, 20],
        [Cow(name="muh11"), 33, 28],
        [Cow(name="muh12"), 38, 33],
        [Cow(name="muh13"), 4, 31],
        [Wolf(name="patrol3"), 6, 27],
        [Wolf(name="patrol4"), 36, 26],
        [Wolf(name="patrol5"), 26, 25],
        [Wolf(name="patrol6"), 1, 2],
        [Wolf(name="patrol7"), 2, 2],
        [Wolf(name="patrol9"), 1, 3],
        [Wolf(name="patrol8"), 10, 5],
        [Wolf(name="patrol20"), 11, 3],
    ]

    for creature, x, y in animals:
        board.place_creature(creature, x, y)

    return board


def main():
    pygame.init()

    board = create_initial_board()
    tile_size = TILE_SIZE
    width = board.size_x * tile_size + (board.size_x + 1) * MARGIN
    height = board.size_y * tile_size + (board.size_y + 1) * MARGIN
    screen = pygame.display.set_mode((width, height))
    renderer = BoardRenderer(board)
    pygame.display.set_caption("lfh ki pygame")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", max(10, tile_size // 2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        board.tick()
        renderer.render(screen, tile_size, MARGIN, font)
        pygame.display.flip()
        clock.tick(TICK_RATE)

    pygame.quit()


if __name__ == "__main__":
    main()
