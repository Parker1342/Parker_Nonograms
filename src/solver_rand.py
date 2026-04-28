import random
from typing import List, Optional, Tuple


Line = List[int]  # 1 = filled, 0 = empty
Clues = List[int]


def generate_line_candidates(length: int, clues: Clues) -> List[Line]:
    """
    Generate all valid line patterns for given length and clues.
    This is deterministic, but you can shuffle results to introduce randomness.
    """
    if clues == [0]:
        return [[0] * length]

    results = []

    def backtrack(idx: int, clue_idx: int, line: List[int]):
        if clue_idx == len(clues):
            # Fill remaining with zeros
            if idx <= length:
                results.append(line + [0] * (length - idx))
            return

        block_len = clues[clue_idx]
        # Try placing block starting at positions >= idx
        for start in range(idx, length - block_len + 1):
            new_line = line + [0] * (start - len(line)) + [1] * block_len
            if start + block_len < length:
                new_line.append(0)  # mandatory space after block if more clues
            backtrack(start + block_len + 1, clue_idx + 1, new_line)

    backtrack(0, 0, [])
    # Trim any overshoot from spacing logic
    trimmed = [l[:length] for l in results if len(l) >= length]
    random.shuffle(trimmed)
    return trimmed


def check_column_consistency(
    partial_grid: List[Line],
    col_clues: List[Clues],
    max_rows: int,
) -> bool:
    """
    Early contradiction check: ensure that current partial columns
    do not violate clues (basic check).
    """
    rows_filled = len(partial_grid)
    width = len(partial_grid[0]) if rows_filled > 0 else 0

    for c in range(width):
        col = [partial_grid[r][c] for r in range(rows_filled)]
        clues = col_clues[c]

        # Simple check: if we already exceed total filled cells allowed
        if sum(col) > sum(clues):
            return False

        # If we have a completed column, check exact clues
        if rows_filled == max_rows:
            # Build full column
            full_col = col
            # Convert to clues
            blocks = []
            count = 0
            for v in full_col:
                if v == 1:
                    count += 1
                elif count > 0:
                    blocks.append(count)
                    count = 0
            if count > 0:
                blocks.append(count)
            if blocks or clues:
                if blocks or clues:
                    if blocks != clues and not (blocks == [] and clues == [0]):
                        return False
    return True


def solve_nonogram_random(
    row_clues: List[Clues],
    col_clues: List[Clues],
    max_attempts: int = 10000,
) -> Optional[List[Line]]:
    """
    A backtracking solver that uses line candidates and randomization.
    """
    height = len(row_clues)
    width = len(col_clues)
    row_candidates = [
        generate_line_candidates(width, rc) for rc in row_clues
    ]

    # Randomize row order slightly (still solving top-down)
    order = list(range(height))

    def backtrack(row_idx: int, grid: List[Line]) -> Optional[List[Line]]:
        if row_idx == height:
            return grid

        r = order[row_idx]
        candidates = row_candidates[r]
        random.shuffle(candidates)

        for cand in candidates:
            new_grid = grid + [cand]
            if not check_column_consistency(
                new_grid, col_clues, max_rows=height
            ):
                continue
            result = backtrack(row_idx + 1, new_grid)
            if result is not None:
                return result
        return None

    for _ in range(max_attempts):
        result = backtrack(0, [])
        if result is not None:
            return result
    return None
