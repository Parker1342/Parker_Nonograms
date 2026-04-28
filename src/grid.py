from typing import List, Tuple

GridData = List[List[int]]  # 1 = filled, 0 = empty


class Grid:
    def __init__(self, solution: GridData):
        self.solution = solution
        self.height = len(solution)
        self.width = len(solution[0]) if self.height > 0 else 0

        # Player grid: 0 = unknown, 1 = filled, -1 = marked (X)
        self.player = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def toggle_fill(self, row: int, col: int):
        if not self.in_bounds(row, col):
            return
        if self.player[row][col] == 1:
            self.player[row][col] = 0
        else:
            self.player[row][col] = 1
            # Clear mark if present
            if self.player[row][col] == -1:
                self.player[row][col] = 1

    def toggle_mark(self, row: int, col: int):
        if not self.in_bounds(row, col):
            return
        if self.player[row][col] == -1:
            self.player[row][col] = 0
        else:
            self.player[row][col] = -1
            # Clear fill if present
            if self.player[row][col] == 1:
                self.player[row][col] = -1

    def is_solved(self) -> bool:
        for r in range(self.height):
            for c in range(self.width):
                if self.player[r][c] == 1 and self.solution[r][c] != 1:
                    return False
                if self.solution[r][c] == 1 and self.player[r][c] != 1:
                    return False
        return True

    def get_cell_state(self, row: int, col: int) -> int:
        """
        Returns:
            1  = filled
            -1 = marked (X)
            0  = empty/unknown
        """
        if not self.in_bounds(row, col):
            return 0
        return self.player[row][col]