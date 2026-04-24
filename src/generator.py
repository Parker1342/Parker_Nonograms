# src/generator.py

import random
from typing import List, Tuple

def generate_solution(size: int) -> List[List[int]]:
    # 1 = filled, 0 = empty
    return [
        [random.choice([0, 1]) for _ in range(size)]
        for _ in range(size)
    ]

def _line_to_clues(line: list[int]) -> list[int]:
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

def compute_clues(solution: list[list[int]]) -> Tuple[list[list[int]], list[list[int]]]:
    size = len(solution)
    row_clues = [_line_to_clues(row) for row in solution]
    col_clues = [_line_to_clues([solution[r][c] for r in range(size)]) for c in range(size)]
    return row_clues, col_clues
