import pygame

from config import DIMENSIONS, FPS
from generator import generate_unique_puzzle
from grid import Grid
from renderer import Renderer
from input_handler import InputHandler


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        solution, row_clues, col_clues = generate_unique_puzzle(
            DIMENSIONS["grid_width"], DIMENSIONS["grid_height"]
        )
        self.grid = Grid(solution)
        self.renderer = Renderer(
            screen,
            row_clues,
            col_clues,
            self.grid.width,
            self.grid.height,
        )
        self.input_handler = InputHandler()
        self.status_text = "Nonogram - Left click: fill, Right click: mark"

    def handle_click(self, pos, left: bool):
        row, col = self.renderer.screen_to_grid(pos)
        if row == -1 or col == -1:
            return
        if left:
            self.grid.toggle_fill(row, col)
        else:
            self.grid.toggle_mark(row, col)

        if self.grid.is_solved():
            self.status_text = "Solved! Press close to exit."

    def update(self):
        # Currently no time-based logic; placeholder for future.
        pass

    def draw(self):
        self.renderer.draw(self.grid)
        self.renderer.draw_status(self.status_text)
        pygame.display.flip()

    def run(self):
        while self.running:
            if not self.input_handler.process_events(self):
                self.running = False
                break

            self.update()
            self.draw()
            self.clock.tick(FPS)
