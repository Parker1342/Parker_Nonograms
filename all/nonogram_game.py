"""
Parker Nonograms - Complete Game Code (Standalone)
All code consolidated into one file for easy copy-paste integration.
Can be run directly or imported into another pygame project.
"""

import pygame
import random
from typing import List, Tuple, Optional, Set

# ============================================================================
# CONFIGURATION
# ============================================================================

pygame.init()

# Colors grouped in a dictionary
COLORS = {
    "background": (30, 30, 30),
    "grid": (200, 200, 200),
    "grid_bold": (255, 255, 255),
    "filled": (60, 160, 220),
    "marked": (200, 80, 80),
    "text": (240, 240, 240),
    "status": (255, 255, 0),
}

# Dimensions grouped in a dictionary
DIMENSIONS = {
    "grid_width": 10,
    "grid_height": 10,
    "window_width": 800,
    "window_height": 800,
}

# Sizings grouped in a dictionary
SIZINGS = {
    "cell_size": 32,
    "line_thickness": 1,
    "bold_line_thickness": 3,
    "clue_margin": 10,
    "clue_panel_size": 150,
    "status_height": 40,
}

FONT_NAME = "arial"
FPS = 60

# Preload fonts
FONTS = {
    "clue": pygame.font.SysFont(FONT_NAME, 18),
    "status": pygame.font.SysFont(FONT_NAME, 22),
}

# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

Line = List[int]  # 1 = filled, 0 = empty
Clues = List[int]
Grid = List[List[int]]  # 1 = filled, 0 = empty
GridData = List[List[int]]  # 1 = filled, 0 = empty

# ============================================================================
# SOLVER (Optimized Random-Based)
# ============================================================================


def generate_line_candidates(length: int, clues: Clues) -> List[Line]:
    """
    Generate all valid line patterns for given length and clues.
    Uses optimized backtracking with early pruning.
    """
    if clues == [0]:
        return [[0] * length]

    results = []

    def backtrack(idx: int, clue_idx: int, line: List[int]):
        if clue_idx == len(clues):
            if len(line) <= length:
                results.append(line + [0] * (length - len(line)))
            return

        block_len = clues[clue_idx]
        remaining_clues = clues[clue_idx + 1:]
        min_space_needed = sum(remaining_clues) + len(remaining_clues)

        for start in range(idx, length - block_len - min_space_needed + 1):
            new_line = line + [0] * (start - len(line)) + [1] * block_len

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
    (Karen's optimization from README)
    """
    if clues == [0]:
        return [0] * length

    must_fill = [False] * length
    candidates = generate_line_candidates(length, clues)
    if not candidates:
        return [0] * length

    for pos in range(length):
        if all(cand[pos] == 1 for cand in candidates):
            must_fill[pos] = True

    return must_fill


def extract_clues_from_line(line: Line) -> List[int]:
    """Convert a filled line into its clue representation."""
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


def solve_nonogram_random(
    row_clues: List[Clues],
    col_clues: List[Clues],
    max_attempts: int = 10000,
) -> Optional[List[Line]]:
    """
    Optimized backtracking solver with overlapping segments deduction.
    """
    height = len(row_clues)
    width = len(col_clues)

    row_candidates = [generate_line_candidates(width, rc) for rc in row_clues]
    col_candidates = [
        generate_line_candidates(height, cc) for cc in col_clues
    ]

    row_must_fill = [
        compute_overlapping_segments(width, rc) for rc in row_clues
    ]
    col_must_fill = [
        compute_overlapping_segments(height, cc) for cc in col_clues
    ]

    def solve_attempt() -> Optional[List[Line]]:
        grid = [[-1] * width for _ in range(height)]

        for r in range(height):
            for c in range(width):
                if row_must_fill[r][c]:
                    grid[r][c] = 1

        for c in range(width):
            for r in range(height):
                if col_must_fill[c][r] and grid[r][c] == -1:
                    grid[r][c] = 1

        remaining_rows = [
            r
            for r in range(height)
            if any(grid[r][c] == -1 for c in range(width))
        ]
        remaining_rows.sort(key=lambda r: len(row_candidates[r]), reverse=False)

        def backtrack_optimized(row_idx: int) -> Optional[List[Line]]:
            if row_idx == len(remaining_rows):
                for c in range(width):
                    col = [grid[r][c] for r in range(height)]
                    if extract_clues_from_line(col) != col_clues[c]:
                        return None
                return [grid[r][:] for r in range(height)]

            r = remaining_rows[row_idx]

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

            random.shuffle(valid_cands)

            for cand in valid_cands:
                old_grid = [row[:] for row in grid]
                for c in range(width):
                    grid[r][c] = cand[c]

                valid = True
                for c in range(width):
                    col = [grid[row][c] for row in range(height)]
                    clues = col_clues[c]

                    filled_count = sum(1 for v in col if v == 1)
                    if filled_count > sum(clues):
                        valid = False
                        break

                if valid:
                    result = backtrack_optimized(row_idx + 1)
                    if result is not None:
                        return result

                for i in range(height):
                    grid[i] = old_grid[i]

            return None

        return backtrack_optimized(0)

    for _ in range(max_attempts):
        result = solve_attempt()
        if result is not None:
            return [[1 if cell == 1 else 0 for cell in row] for row in result]

    return None


def solve_with_random_solver(
    row_clues: List[Clues],
    col_clues: List[Clues],
    timeout: float = 5.0,
) -> Optional[List[Line]]:
    """Wrapper for solve_nonogram_random with timeout support."""
    max_attempts = max(1, int(timeout * 100))
    result = solve_nonogram_random(row_clues, col_clues, max_attempts)
    return result


# ============================================================================
# GENERATOR
# ============================================================================


def generate_random_solution(
    width: int, height: int, fill_prob: float = 0.5
) -> Grid:
    """Generate a random nonogram solution."""
    return [
        [1 if random.random() < fill_prob else 0 for _ in range(width)]
        for _ in range(height)
    ]


def line_to_clues(line: List[int]) -> List[int]:
    """Convert a line to its clue representation."""
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
    """Compute row and column clues from a solution grid."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    row_clues = [line_to_clues(row) for row in grid]
    col_clues = [
        line_to_clues([grid[r][c] for r in range(height)])
        for c in range(width)
    ]
    return row_clues, col_clues


def generate_unique_puzzle(
    width: int = None, height: int = None, max_attempts: int = 50
) -> Tuple[Grid, List[List[int]], List[List[int]]]:
    """Generate a unique nonogram puzzle (stub - doesn't verify uniqueness)."""
    if width is None:
        width = DIMENSIONS["grid_width"]
    if height is None:
        height = DIMENSIONS["grid_height"]

    for _ in range(max_attempts):
        solution = generate_random_solution(width, height, fill_prob=0.5)
        row_clues, col_clues = compute_clues(solution)
        return solution, row_clues, col_clues

    return solution, row_clues, col_clues


# ============================================================================
# GRID
# ============================================================================


class Grid:
    """Represents the game grid state."""

    def __init__(self, solution: GridData):
        self.solution = solution
        self.height = len(solution)
        self.width = len(solution[0]) if self.height > 0 else 0

        # Player grid: 0 = unknown, 1 = filled, -1 = marked (X)
        self.player = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def toggle_fill(self, row: int, col: int):
        if not self.in_bounds(row, col):
            return
        if self.player[row][col] == 1:
            self.player[row][col] = 0
        else:
            self.player[row][col] = 1

    def toggle_mark(self, row: int, col: int):
        if not self.in_bounds(row, col):
            return
        if self.player[row][col] == -1:
            self.player[row][col] = 0
        else:
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
        """Returns: 1=filled, -1=marked (X), 0=empty/unknown"""
        if not self.in_bounds(row, col):
            return 0
        return self.player[row][col]


# ============================================================================
# RENDERER
# ============================================================================


class Renderer:
    """Handles all rendering for the nonogram game."""

    def __init__(
        self,
        screen: pygame.Surface,
        row_clues: List[List[int]],
        col_clues: List[List[int]],
        grid_width: int,
        grid_height: int,
    ):
        self.screen = screen
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.cell_size = SIZINGS["cell_size"]
        self.clue_panel_size = SIZINGS["clue_panel_size"]
        self.status_height = SIZINGS["status_height"]

        self.grid_origin = self._compute_grid_origin()
        self.static_surface = self._build_static_surface()

    def _compute_grid_origin(self) -> Tuple[int, int]:
        total_width = self.clue_panel_size + self.grid_width * self.cell_size
        total_height = (
            self.clue_panel_size
            + self.grid_height * self.cell_size
            + self.status_height
        )

        win_w = DIMENSIONS["window_width"]
        win_h = DIMENSIONS["window_height"]

        offset_x = (win_w - total_width) // 2
        offset_y = (win_h - total_height) // 2 + self.status_height
        return offset_x + self.clue_panel_size, offset_y

    def _build_static_surface(self) -> pygame.Surface:
        win_w = DIMENSIONS["window_width"]
        win_h = DIMENSIONS["window_height"]
        surface = pygame.Surface((win_w, win_h))
        surface.fill(COLORS["background"])

        self._draw_clue_panels(surface)
        self._draw_grid_lines(surface)
        return surface

    def _draw_clue_panels(self, surface: pygame.Surface):
        # Draw row clues (left)
        for r, clues in enumerate(self.row_clues):
            text = " ".join(map(str, clues))
            img = FONTS["clue"].render(text, True, COLORS["text"])
            x = self.grid_origin[0] - 10
            y = (
                self.grid_origin[1]
                + r * self.cell_size
                + self.cell_size // 2
            )
            rect = img.get_rect(right=x, centery=y)
            surface.blit(img, rect)

        # Draw column clues (top)
        for c, clues in enumerate(self.col_clues):
            text = "\n".join(map(str, clues))
            lines = text.split("\n")
            x = (
                self.grid_origin[0]
                + c * self.cell_size
                + self.cell_size // 2
            )
            base_y = self.grid_origin[1] - 10
            for i, line in enumerate(reversed(lines)):
                img = FONTS["clue"].render(line, True, COLORS["text"])
                rect = img.get_rect(centerx=x, bottom=base_y - i * 18)
                surface.blit(img, rect)

    def _draw_grid_lines(self, surface: pygame.Surface):
        x0, y0 = self.grid_origin
        w = self.grid_width * self.cell_size
        h = self.grid_height * self.cell_size

        for r in range(self.grid_height + 1):
            y = y0 + r * self.cell_size
            thickness = (
                SIZINGS["bold_line_thickness"]
                if r % 5 == 0
                else SIZINGS["line_thickness"]
            )
            color = (
                COLORS["grid_bold"]
                if r % 5 == 0
                else COLORS["grid"]
            )
            pygame.draw.line(surface, color, (x0, y), (x0 + w, y), thickness)

        for c in range(self.grid_width + 1):
            x = x0 + c * self.cell_size
            thickness = (
                SIZINGS["bold_line_thickness"]
                if c % 5 == 0
                else SIZINGS["line_thickness"]
            )
            color = (
                COLORS["grid_bold"]
                if c % 5 == 0
                else COLORS["grid"]
            )
            pygame.draw.line(
                surface, color, (x, y0), (x, y0 + h), thickness
            )

    def draw_status(self, text: str):
        img = FONTS["status"].render(text, True, COLORS["status"])
        rect = img.get_rect(
            centerx=DIMENSIONS["window_width"] // 2,
            top=5,
        )
        self.screen.blit(img, rect)

    def draw(self, grid_state):
        # Blit static background (grid + clues)
        self.screen.blit(self.static_surface, (0, 0))

        # Draw dynamic cells (filled and X marks)
        x0, y0 = self.grid_origin
        for r in range(grid_state.height):
            for c in range(grid_state.width):
                state = grid_state.get_cell_state(r, c)
                cell_rect = pygame.Rect(
                    x0 + c * self.cell_size + 1,
                    y0 + r * self.cell_size + 1,
                    self.cell_size - 2,
                    self.cell_size - 2,
                )
                if state == 1:
                    pygame.draw.rect(
                        self.screen, COLORS["filled"], cell_rect
                    )
                elif state == -1:
                    # Draw X mark
                    pygame.draw.line(
                        self.screen,
                        COLORS["marked"],
                        cell_rect.topleft,
                        cell_rect.bottomright,
                        2,
                    )
                    pygame.draw.line(
                        self.screen,
                        COLORS["marked"],
                        cell_rect.topright,
                        cell_rect.bottomleft,
                        2,
                    )

    def screen_to_grid(self, pos) -> Tuple[int, int]:
        x, y = pos
        x0, y0 = self.grid_origin
        if x < x0 or y < y0:
            return -1, -1
        col = (x - x0) // self.cell_size
        row = (y - y0) // self.cell_size
        if (
            col < 0
            or col >= self.grid_width
            or row < 0
            or row >= self.grid_height
        ):
            return -1, -1
        return row, col


# ============================================================================
# INPUT HANDLER
# ============================================================================


class InputHandler:
    """Handles user input (mouse clicks)."""

    def __init__(self):
        self.left_down = False
        self.right_down = False

    def process_events(self, game) -> bool:
        """Returns False if user wants to quit, True otherwise."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_down = True
                    game.handle_click(event.pos, left=True)
                elif event.button == 3:
                    self.right_down = True
                    game.handle_click(event.pos, left=False)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_down = False
                elif event.button == 3:
                    self.right_down = False

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Press 'H' for hint
                    game.give_hint()
                elif event.key == pygame.K_s:  # Press 'S' to solve
                    game.solve_puzzle()

        return True


# ============================================================================
# GAME
# ============================================================================


class Game:
    """Main game class that orchestrates all components."""

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
        self.status_text = (
            "Click: fill/mark | H: hint | S: solve"
        )

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

    def give_hint(self):
        """Provide one hint by solving and revealing one correct cell."""
        # Get clues from solution
        row_clues = [line_to_clues(row) for row in self.grid.solution]
        col_clues = [
            line_to_clues([self.grid.solution[r][c] for r in range(self.grid.height)])
            for c in range(self.grid.width)
        ]

        # Solve the puzzle
        solution = solve_with_random_solver(row_clues, col_clues, timeout=2.0)

        if solution:
            # Find first unfilled cell that should be filled
            for r in range(self.grid.height):
                for c in range(self.grid.width):
                    if self.grid.player[r][c] == 0 and solution[r][c] == 1:
                        self.grid.toggle_fill(r, c)
                        self.status_text = "Hint: A cell filled! Press 'H' for more hints."
                        return
            # If all cells are filled, show success
            if self.grid.is_solved():
                self.status_text = "Solved! Press close to exit."
        else:
            self.status_text = "Could not solve puzzle. Try manually!"

    def solve_puzzle(self):
        """Automatically solve the entire puzzle."""
        # Get clues from solution
        row_clues = [line_to_clues(row) for row in self.grid.solution]
        col_clues = [
            line_to_clues([self.grid.solution[r][c] for r in range(self.grid.height)])
            for c in range(self.grid.width)
        ]

        # Solve the puzzle
        solution = solve_with_random_solver(row_clues, col_clues, timeout=5.0)

        if solution:
            # Fill all correct cells
            for r in range(self.grid.height):
                for c in range(self.grid.width):
                    if solution[r][c] == 1:
                        self.grid.player[r][c] = 1
                    else:
                        self.grid.player[r][c] = 0
            self.status_text = "Puzzle solved automatically! Press close to exit."
        else:
            self.status_text = "Could not solve puzzle automatically."

    def update(self):
        """Update game state (placeholder for time-based logic)."""
        pass

    def draw(self):
        """Draw the current game state."""
        self.renderer.draw(self.grid)
        self.renderer.draw_status(self.status_text)
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            if not self.input_handler.process_events(self):
                self.running = False
                break

            self.update()
            self.draw()
            self.clock.tick(FPS)


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Entry point for the game."""
    pygame.init()
    screen = pygame.display.set_mode(
        (DIMENSIONS["window_width"], DIMENSIONS["window_height"])
    )
    pygame.display.set_caption("Nonogram")

    game = Game(screen)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
