# src/grid.py

from typing import List

class CellState:
    EMPTY = 0      # untouched
    FILLED = 1     # player filled
    MARKED = 2     # player marked as X

class Grid:
    def __init__(self, solution: List[List[int]]):
        self.solution = solution
        self.size = len(solution)
        self.cells = [
            [CellState.EMPTY for _ in range(self.size)]
            for _ in range(self.size)
        ]

    def toggle_fill(self, row: int, col: int):
        if self.cells[row][col] == CellState.FILLED:
            self.cells[row][col] = CellState.EMPTY
        else:
            self.cells[row][col] = CellState.FILLED

    def toggle_mark(self, row: int, col: int):
        if self.cells[row][col] == CellState.MARKED:
            self.cells[row][col] = CellState.EMPTY
        else:
            self.cells[row][col] = CellState.MARKED

    def is_solved(self) -> bool:
        for r in range(self.size):
            for c in range(self.size):
                if (self.solution[r][c] == 1 and self.cells[r][c] != CellState.FILLED) or \
                   (self.solution[r][c] == 0 and self.cells[r][c] == CellState.FILLED):
                    return False
        return True
