# src/solver_rand.py

import random
import time
import sys
from typing import Optional

class RandomSolver:
    """
    Solver that uses random generation with constraint-based optimizations.
    Based on nonogram solving techniques using overlapping segments and line deductions.
    """

    def __init__(self, row_clues, col_clues, timeout=30.0):
        """
        Initialize the solver with clues and timeout.

        Args:
            row_clues: List of clue lists for each row
            col_clues: List of clue lists for each column
            timeout: Maximum time to spend solving in seconds
        """
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.size = len(row_clues)
        self.timeout = timeout
        self.start_time = None

    def solve(self):
        """
        Attempt to solve the nonogram using random generation with optimizations.

        Returns:
            Solved grid as list of lists, or None if unsolved/timeout
        """
        self.start_time = time.time()
        sys.setrecursionlimit(2000)

        # Initialize blank grid
        grid = self._initialize_blank_grid()

        # Apply initial constraints and deductions
        grid = self._apply_initial_constraints(grid)

        # Main solving loop with random attempts
        return self._solve_with_random_attempts(grid)

    def _initialize_blank_grid(self):
        """Create a blank grid (all zeros)."""
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def _apply_initial_constraints(self, grid):
        """
        Apply initial mathematical certainties before random attempts.
        Uses overlapping segments and clue sum constraints.
        """
        # Apply row constraints
        for row_idx, clues in enumerate(self.row_clues):
            grid[row_idx] = self._apply_line_constraints(grid[row_idx], clues)

        # Apply column constraints
        for col_idx, clues in enumerate(self.col_clues):
            col = [grid[r][col_idx] for r in range(self.size)]
            col = self._apply_line_constraints(col, clues)
            for r in range(self.size):
                grid[r][col_idx] = col[r]

        return grid

    def _apply_line_constraints(self, line, clues):
        """
        Apply constraints to a single line (row or column).
        Uses clue sums and overlapping segments.
        """
        # Check if line can be fully determined
        if self._can_determine_line(clues, len(line)):
            return self._determine_line_from_clues(clues, len(line))

        # Apply overlapping segments
        return self._apply_overlapping_segments(line, clues)

    def _can_determine_line(self, clues, length):
        """
        Check if a line can be fully determined from clues.
        Formula: (Sum of Clues) + (Number of Clues) - 1 = Length
        """
        if not clues or clues == [0]:
            return True  # Empty line
        clue_sum = sum(clues)
        num_clues = len(clues)
        return clue_sum + num_clues - 1 == length

    def _determine_line_from_clues(self, clues, length):
        """Determine complete line from clues when possible."""
        if not clues or clues == [0]:
            return [0] * length

        line = []
        for i, clue in enumerate(clues):
            line.extend([1] * clue)
            if i < len(clues) - 1:
                line.append(0)
        return line

    def _apply_overlapping_segments(self, line, clues):
        """
        Apply overlapping segments logic.
        For a single clue of size N in a line of size L, the middle cells must be filled.
        """
        if len(clues) == 1:
            clue = clues[0]
            L = len(line)
            P = L - clue + 1
            if P > 1:
                start = L - clue
                end = clue - 1
                for i in range(start, end + 1):
                    line[i] = 1
        return line

    def _solve_with_random_attempts(self, grid):
        """
        Main solving loop using random attempts with constraint checking.
        """
        attempts = 0
        max_attempts = 10000  # Increased limit

        while attempts < max_attempts and not self._is_timeout():
            # Try to fill remaining cells randomly
            candidate = self._generate_candidate_solution(grid)

            # Check if candidate satisfies all constraints
            if self._validate_solution(candidate):
                return candidate

            attempts += 1

        return None  # Could not solve within limits

    def _generate_candidate_solution(self, partial_grid):
        """Generate a complete solution from partial grid by filling unknowns randomly."""
        candidate = [row[:] for row in partial_grid]  # Copy

        for r in range(self.size):
            for c in range(self.size):
                if candidate[r][c] == 0:  # Unknown cell
                    candidate[r][c] = 1 if random.random() > 0.5 else 0

        return candidate

    def _validate_solution(self, grid):
        """
        Check if a grid satisfies all row and column clues.
        Also check for early contradictions.
        """
        # Validate rows
        for r in range(self.size):
            if not self._line_matches_clues(grid[r], self.row_clues[r]):
                return False

        # Validate columns
        for c in range(self.size):
            col = [grid[r][c] for r in range(self.size)]
            if not self._line_matches_clues(col, self.col_clues[c]):
                return False

        return True

    def _line_matches_clues(self, line, clues):
        """Check if a line matches its clues."""
        actual_clues = []
        count = 0
        for cell in line:
            if cell == 1:
                count += 1
            elif count > 0:
                actual_clues.append(count)
                count = 0
        if count > 0:
            actual_clues.append(count)

        return actual_clues == clues

    def _is_timeout(self):
        """Check if we've exceeded the timeout."""
        if self.start_time is None:
            return False
        elapsed = time.time() - self.start_time
        if elapsed > self.timeout:
            return True
        return False

def solve_with_random_solver(row_clues, col_clues, timeout=30.0):
    """
    Convenience function to solve using RandomSolver.

    Args:
        row_clues: Row clues
        col_clues: Column clues
        timeout: Timeout in seconds

    Returns:
        Solved grid or None
    """
    solver = RandomSolver(row_clues, col_clues, timeout)
    return solver.solve()
