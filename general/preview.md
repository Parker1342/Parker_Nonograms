# Parker Nonograms

A complete Nonogram puzzle game with intelligent solving capabilities.

## Key Features

- **Interactive Gameplay**: Left-click to fill cells, right-click to mark as empty
- **Smart Puzzle Generation**: Creates solvable puzzles with proper clue systems
- **Programmatic Solver**: Random solver with constraint optimizations
- **Modular Architecture**: Clean separation of game logic, rendering, and input

## The Game Loop

The heart of the game - how everything comes together:

```python
class Game:
    def __init__(self, screen: pygame.Surface):
        # Generate a random solution grid for this game session
        solution = generate_solution(GRID_SIZE)
        
        # Convert the solution into clues that players will see
        row_clues, col_clues = compute_clues(solution)

        # Create the grid that tracks player progress
        self.grid = Grid(solution)
        
        # Set up the renderer to draw everything on screen
        self.renderer = Renderer(screen, row_clues, col_clues)
        
        # Initialize input handling
        self.input_handler = InputHandler()
        
        # Game loop control flag
        self.running = True

    def update(self):
        # Process all pending events (mouse clicks, key presses, etc.)
        for event in pygame.event.get():
            # Handle the event - returns False if player wants to quit
            if not self.input_handler.handle_event(event, self.grid, self.renderer):
                self.running = False

    def draw(self):
        # Tell the renderer to draw the current game state
        self.renderer.draw(self.grid)
```

## Puzzle Generation - The Magic Behind the Scenes

How we create random puzzles that are actually solvable:

```python
def generate_solution(size: int) -> List[List[int]]:
    # Create a random grid where each cell is either filled (1) or empty (0)
    # This represents the "picture" the player needs to recreate
    return [
        [random.choice([0, 1]) for _ in range(size)]
        for _ in range(size)
    ]

def _line_to_clues(line: list[int]) -> list[int]:
    # Convert a row/column of 1s and 0s into clue numbers
    clues = []
    count = 0
    
    # Count consecutive 1s (filled cells)
    for cell in line:
        if cell == 1:
            count += 1
        elif count > 0:
            # End of a filled block - add it to clues
            clues.append(count)
            count = 0
    
    # Handle case where line ends with filled cells
    if count > 0:
        clues.append(count)
    
    # Return clues, or [0] if no filled cells (empty line)
    return clues or [0]
```

## Smart Grid Management

Three-state cell system allows for nuanced player input:

```python
class CellState:
    EMPTY = 0      # untouched - player hasn't decided yet
    FILLED = 1     # player filled - thinks this should be painted
    MARKED = 2     # player marked as X - thinks this should be empty

class Grid:
    def __init__(self, solution: List[List[int]]):
        # Store the correct answer (1 = filled, 0 = empty)
        self.solution = solution
        
        # Get grid dimensions
        self.size = len(solution)
        
        # Initialize player's grid - all cells start empty
        self.cells = [
            [CellState.EMPTY for _ in range(self.size)]
            for _ in range(self.size)
        ]

    def is_solved(self) -> bool:
        # Check if player's grid matches the solution
        for r in range(self.size):
            for c in range(self.size):
                # For each cell, check if player's choice matches solution
                if (self.solution[r][c] == 1 and self.cells[r][c] != CellState.FILLED) or \
                   (self.solution[r][c] == 0 and self.cells[r][c] == CellState.FILLED):
                    return False
        return True
```

## The Intelligent Solver

Our random solver uses clever optimizations to solve puzzles programmatically:

```python
class RandomSolver:
    """
    Solver that uses random generation with constraint-based optimizations.
    Based on nonogram solving techniques using overlapping segments and line deductions.
    """

    def __init__(self, row_clues: List[List[int]], col_clues: List[List[int]], timeout: float = 30.0):
        # Store the clues that define the puzzle
        self.row_clues = row_clues
        self.col_clues = col_clues
        
        # Get grid size from number of row clues
        self.size = len(row_clues)
        
        # Set timeout to prevent infinite solving attempts
        self.timeout = timeout
        
        # Will be set when solving starts
        self.start_time = None

    def solve(self) -> Optional[List[List[int]]]:
        # Record when solving started for timeout checking
        self.start_time = time.time()

        # Initialize blank grid
        grid = self._initialize_blank_grid()

        # Apply initial constraints and deductions
        grid = self._apply_initial_constraints(grid)

        # Main solving loop with random attempts
        return self._solve_with_random_attempts(grid)
```

## Configuration System

Clean organization of all game parameters:

```python
# Window dimensions - determines the size of the game window in pixels
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Frames per second - controls how smooth the game runs (60 FPS is standard for games)
FPS = 60

# Grid size - number of cells in each row/column (10x10 = 100 cells total)
GRID_SIZE = 10

# Color definitions using RGB tuples (0-255 values)
BACKGROUND_COLOR = (30, 30, 30)      # Dark background provides contrast
GRID_LINE_COLOR = (200, 200, 200)     # Light gray for grid lines
FILLED_COLOR = (60, 180, 75)          # Green for filled cells
MARKED_COLOR = (200, 60, 60)          # Red for marked cells
TEXT_COLOR = (230, 230, 230)          # Light gray for text
```

## Project Architecture

```
Parker_Nonograms/
├── src/
│   ├── config.py          # Game settings and constants
│   ├── game.py            # Main game orchestrator
│   ├── generator.py       # Puzzle creation logic
│   ├── grid.py            # Grid state management
│   ├── input_handler.py   # User input processing
│   ├── main.py            # Entry point and game loop
│   ├── renderer.py        # Visual rendering (planned)
│   ├── solver_rand.py     # Intelligent puzzle solver
│   └── solver_prolog.py   # Future Prolog-based solver
```

## Future Vision

**Prolog Solver Implementation**: Using logic programming for exact puzzle solving and in-game hints. Will leverage pyswip for persistent Prolog engine integration, enabling advanced features like:
- Real-time hint generation
- Solution verification
- Complex puzzle analysis

This project demonstrates advanced Python concepts including modular design, algorithmic puzzle solving, and game development principles.