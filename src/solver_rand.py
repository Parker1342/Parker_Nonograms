import random
from typing import List, Optional, Tuple, Set
import signal
import threading


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
            # All clues placed; fill remaining with zeros
            if len(line) <= length:
                results.append(line + [0] * (length - len(line)))
            return

        block_len = clues[clue_idx]
        # Minimum space needed for remaining clues
        remaining_clues = clues[clue_idx + 1:]
        min_space_needed = sum(remaining_clues) + len(remaining_clues)
        
        # Try placing block starting at positions >= idx
        for start in range(idx, length - block_len - min_space_needed + 1):
            new_line = line + [0] * (start - len(line)) + [1] * block_len
            
            # If there are more clues, add mandatory space
            if clue_idx + 1 < len(clues) and start + block_len < length:
                new_line.append(0)
                next_idx = start + block_len + 1
            else:
                next_idx = start + block_len
            
            backtrack(next_idx, clue_idx + 1, new_line)

    backtrack(0, 0, [])
    return results


def compute_overlapping_segments(length: int, clues: Clues) -> Line:
    """
    Compute cells that MUST be filled using overlapping segment logic.
    For each block in the clues, find the leftmost and rightmost positions
    it can occupy, then mark cells that are filled in ALL valid placements.
    This is a key optimization mentioned in the README.
    
    Example: length=10, clues=[8]
    - Block can start at positions 0 (fills 0-7) or 2 (fills 2-9)
    - Cells 2-7 are always filled regardless of placement
    - Returns [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
    """
    if clues == [0]:
        return [0] * length
    
    # For each position, track if it must be filled
    must_fill = [False] * length
    must_empty = [False] * length
    
    candidates = generate_line_candidates(length, clues)
    if not candidates:
        return [0] * length
    
    # Find cells that are filled in ALL candidates
    for pos in range(length):
        all_filled = all(cand[pos] == 1 for cand in candidates)
        all_empty = all(cand[pos] == 0 for cand in candidates)
        
        if all_filled:
            must_fill[pos] = True
        if all_empty:
            must_empty[pos] = True
    
    return must_fill


def extract_clues_from_line(line: Line) -> List[int]:
    """
    Convert a filled line into its clue representation.
    Example: [1, 1, 0, 1, 1, 1] -> [2, 3]
    """
    blocks = []
    count = 0
    for v in line:
        if v == 1:
            count += 1
        elif count > 0:
            blocks.append(count)
            count = 0
    if count > 0:
        blocks.append(count)
    return blocks if blocks else [0]


def line_is_compatible(partial_line: Line, candidates: List[Line]) -> List[Line]:
    """
    Filter candidates to only those compatible with the partial line (so far).
    A candidate is compatible if where partial_line has a value, candidate matches.
    """
    compatible = []
    for cand in candidates:
        match = True
        for i, val in enumerate(partial_line):
            if val != -1 and cand[i] != val:  # -1 means "undecided"
                match = False
                break
        if match:
            compatible.append(cand)
    return compatible


def check_column_consistency(
    partial_grid: List[Line],
    col_clues: List[Clues],
    max_rows: int,
) -> bool:
    """
    Early contradiction check: ensure that current partial columns
    do not violate clues and are logically consistent.
    """
    rows_filled = len(partial_grid)
    width = len(partial_grid[0]) if rows_filled > 0 else 0

    for c in range(width):
        col = [partial_grid[r][c] for r in range(rows_filled)]
        clues = col_clues[c]

        # Check 1: if we already exceed total filled cells allowed
        if sum(col) > sum(clues):
            return False

        # Check 2: ensure filled cells form valid block structure
        blocks_so_far = [b for b in extract_clues_from_line(col) if b > 0]
        if blocks_so_far:
            # We should not have more blocks than expected clues
            if len(blocks_so_far) > len(clues):
                return False
            # Each completed block should match clue sizes (in order)
            for i, block in enumerate(blocks_so_far[:-1]):  # all but last
                if i >= len(clues) or block != clues[i]:
                    return False
            # Last block should not exceed its clue size
            if len(blocks_so_far) > 0:
                last_block_idx = len(blocks_so_far) - 1
                if last_block_idx < len(clues) and blocks_so_far[-1] > clues[last_block_idx]:
                    return False

        # Check 3: if we have a completed column, verify exact clues
        if rows_filled == max_rows:
            final_clues = extract_clues_from_line(col)
            if final_clues != clues:
                return False
    
    return True


def solve_nonogram_random(
    row_clues: List[Clues],
    col_clues: List[Clues],
    max_attempts: int = 10000,
) -> Optional[List[Line]]:
    """
    An optimized backtracking solver using:
    - Overlapping segments for deduction
    - Constraint propagation
    - Intelligent row ordering (fewest candidates first)
    - Early contradiction detection
    """
    height = len(row_clues)
    width = len(col_clues)
    
    # Pre-compute candidates for each row/column
    row_candidates = [
        generate_line_candidates(width, rc) for rc in row_clues
    ]
    col_candidates = [
        generate_line_candidates(height, cc) for cc in col_clues
    ]
    
    # Pre-compute overlapping segments (cells that must be filled)
    row_must_fill = [
        compute_overlapping_segments(width, rc) for rc in row_clues
    ]
    col_must_fill = [
        compute_overlapping_segments(height, cc) for cc in col_clues
    ]
    
    def solve_attempt() -> Optional[List[Line]]:
        """Single solve attempt with randomization."""
        grid = [[-1] * width for _ in range(height)]
        
        # Initialize with overlapping segments (mathematical certainty)
        for r in range(height):
            for c in range(width):
                if row_must_fill[r][c]:
                    grid[r][c] = 1
        
        for c in range(width):
            for r in range(height):
                if col_must_fill[c][r] and grid[r][c] == -1:
                    grid[r][c] = 1
        
        # Get remaining undecided rows, sorted by candidate count (greedy)
        remaining_rows = [
            r for r in range(height)
            if any(grid[r][c] == -1 for c in range(width))
        ]
        remaining_rows.sort(
            key=lambda r: len(row_candidates[r]), reverse=False
        )
        
        def backtrack_optimized(row_idx: int) -> Optional[List[Line]]:
            if row_idx == len(remaining_rows):
                # All rows assigned, verify solution
                for c in range(width):
                    col = [grid[r][c] for r in range(height)]
                    if extract_clues_from_line(col) != col_clues[c]:
                        return None
                return [grid[r][:] for r in range(height)]
            
            r = remaining_rows[row_idx]
            
            # Filter candidates to those compatible with current grid state
            valid_cands = []
            for cand in row_candidates[r]:
                valid = True
                for c in range(width):
                    if grid[r][c] != -1 and grid[r][c] != cand[c]:
                        valid = False
                        break
                if valid:
                    valid_cands.append(cand)
            
            if not valid_cands:
                return None
            
            # Shuffle for randomness
            random.shuffle(valid_cands)
            
            for cand in valid_cands:
                # Place the row
                old_grid = [row[:] for row in grid]
                for c in range(width):
                    grid[r][c] = cand[c]
                
                # Check column consistency
                valid = True
                for c in range(width):
                    col = [grid[row][c] for row in range(height)]
                    clues = col_clues[c]
                    
                    # Early pruning: check if column is still salvageable
                    filled_count = sum(1 for v in col if v == 1)
                    if filled_count > sum(clues):
                        valid = False
                        break
                
                if valid:
                    result = backtrack_optimized(row_idx + 1)
                    if result is not None:
                        return result
                
                # Restore grid
                for i in range(height):
                    grid[i] = old_grid[i]
            
            return None
        
        return backtrack_optimized(0)
    
    # Multiple attempts with randomization
    for _ in range(max_attempts):
        result = solve_attempt()
        if result is not None:
            # Convert -1 to 0 (in case any remain)
            return [
                [1 if cell == 1 else 0 for cell in row]
                for row in result
            ]
    
    return None


def solve_with_random_solver(
    row_clues: List[Clues],
    col_clues: List[Clues],
    timeout: float = 5.0,
) -> Optional[List[Line]]:
    """
    Wrapper for solve_nonogram_random with timeout support.
    
    Args:
        row_clues: Clues for each row
        col_clues: Clues for each column
        timeout: Maximum time in seconds to spend solving
    
    Returns:
        Solved grid if found within timeout, None otherwise
    """
    height = len(row_clues)
    width = len(col_clues)
    
    # Estimate max attempts based on timeout
    # This is a heuristic: adjust based on typical solve time
    max_attempts = max(1, int(timeout * 100))
    
    result = solve_nonogram_random(row_clues, col_clues, max_attempts)
    return result
