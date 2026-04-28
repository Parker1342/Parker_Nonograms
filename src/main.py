import pygame

from config import DIMENSIONS
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (DIMENSIONS["window_width"], DIMENSIONS["window_height"])
    )
    pygame.display.set_caption("Nonogram")

    game = Game(screen)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
