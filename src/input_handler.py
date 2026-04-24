# src/input_handler.py

import pygame
from .grid import Grid

class InputHandler:
    def handle_event(self, event: pygame.event.Event, grid: Grid, renderer) -> bool:
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cell = renderer.screen_to_cell(pos, grid.size)
            if cell is not None:
                r, c = cell
                if event.button == 1:   # left click
                    grid.toggle_fill(r, c)
                elif event.button == 3: # right click
                    grid.toggle_mark(r, c)
        return True
