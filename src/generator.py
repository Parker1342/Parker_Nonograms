import random
from typing import List, Tuple

from config import DIMENSIONS
import solver_prolog


Grid = List[List[int]]  # 1 = filled, 0 = empty


def generate_random_solution(
    width: int, height: int, fill_prob: float = 0.5
) -> Grid:
    return [
        [1 if random.random() < fill_prob else 0 for _ in range(width)]
        for _ in range(height)
    ]


def line_to_clues(line: List[int]) -> List[int]:
    clues = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        elif count > 0:
            clues.append(count)
            count = 0
    if count > 0:
        clues.append(count)
    return clues or [0]


def compute_clues(grid: Grid) -> Tuple[List[List[int]], List[List[int]]]:
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    row_clues = [line_to_clues(row) for row in grid]
    col_clues = [
        line_to_clues([grid[r][c] for r in range(height)]) for c in range(width)
    ]
    return row_clues, col_clues


def generate_unique_puzzle(
    width: int = None, height: int = None, max_attempts: int = 50
) -> Tuple[Grid, List[List[int]], List[List[int]]]:
    """
    Generate a random solution grid and its clues, and (conceptually)
    check uniqueness via solver_prolog. Currently uses a stubbed uniqueness
    check that always accepts the first grid.
    """
    if width is None:
        width = DIMENSIONS["grid_width"]
    if height is None:
        height = DIMENSIONS["grid_height"]

    for _ in range(max_attempts):
        solution = generate_random_solution(width, height, fill_prob=0.5)
        row_clues, col_clues = compute_clues(solution)

        # Ask Prolog solver how many solutions exist (stubbed for now).
        num_solutions = solver_prolog.count_solutions(
            row_clues, col_clues, width, height, max_solutions=2
        )
        if num_solutions == 1:
            return solution, row_clues, col_clues

    # Fallback: just return the last generated puzzle even if uniqueness
    # is not guaranteed (you can tighten this later).
    return solution, row_clues, col_clues