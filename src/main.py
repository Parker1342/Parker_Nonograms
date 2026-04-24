# src/main.py

import pygame
from .config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from .game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Nonogram Generator")
    clock = pygame.time.Clock()

    game = Game(screen)

    while game.running:
        game.update()
        game.draw()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()