# src/game.py

import pygame
from .grid import Grid
from .generator import generate_solution, compute_clues
from .renderer import Renderer
from .input_handler import InputHandler
from .config import GRID_SIZE

class Game:
    def __init__(self, screen: pygame.Surface):
        solution = generate_solution(GRID_SIZE)
        row_clues, col_clues = compute_clues(solution)

        self.grid = Grid(solution)
        self.renderer = Renderer(screen, row_clues, col_clues)
        self.input_handler = InputHandler()
        self.running = True

    def update(self):
        for event in pygame.event.get():
            if not self.input_handler.handle_event(event, self.grid, self.renderer):
                self.running = False

    def draw(self):
        self.renderer.draw(self.grid)
