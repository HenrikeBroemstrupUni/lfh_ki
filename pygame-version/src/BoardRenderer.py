from src.Creature import Cow, Wolf, Grass
import pygame

class BoardRenderer:
    def __init__(self, board):
        self.images = {}
        self.board = board
        self._load_images()


    def _load_images(self):
        try:
            self.images['cow'] = pygame.image.load('./pictures/cow.png')
        except:
            self.images['cow'] = None
        try:
            self.images['wolf'] = pygame.image.load('./pictures/wolf.png')
        except:
            self.images['wolf'] = None
        try:
            self.images['grass'] = pygame.image.load('./pictures/plant.png')
        except:
            self.images['grass'] = None

    def _get_image(self, creature, tile_size):
        if isinstance(creature, Cow):
            img = self.images.get('cow')
        elif isinstance(creature, Wolf):
            img = self.images.get('wolf')
        elif isinstance(creature, Grass):
            img = self.images.get('grass')
        else:
            return None

        if img is None:
            return None
        return pygame.transform.scale(img, (tile_size, tile_size))

    def render(self, screen, tile_size=16, margin=1, font=None):
        background = (20, 20, 20)
        grid_color = (55, 55, 55)

        screen.fill(background)

        for y in range(self.board.size_y):
            for x in range(self.board.size_x):
                cell_rect = pygame.Rect(
                    margin + x * (tile_size + margin),
                    margin + y * (tile_size + margin),
                    tile_size,
                    tile_size,
                )
                pygame.draw.rect(screen, grid_color, cell_rect)

                ids = self.board.locations.get((x, y))
                if not ids:
                    continue

                creatures = [self.board.creature_registry[id] for id in ids]
                creature = creatures[0]

                img = self._get_image(creature, tile_size)
                if img is not None:
                    screen.blit(img, cell_rect)

                if font is None or len(creatures) <= 1:
                    continue

                label = str(len(creatures))
                text = font.render(label, True, (255, 255, 0))
                text_rect = text.get_rect(center=cell_rect.center)
                screen.blit(text, text_rect)