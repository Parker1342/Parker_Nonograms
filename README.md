# Parker_Nonograms
Doc MO 25-26 HAI Final Project


# History
V1.0 (Initial Design and Draft)
V1.1 (Copilot Redraft of Outline)
V1.2 (Google AI Redraft)
# config.py
File containing the various configurations, such as grid dimensions (X and Y), window dimensions (X and Y), window FPS, colors (background,text,filled tiles,grid,numbers), the font, line thickness, and any spacers or margin distances. Group the various constants into dictionaries such as Colors, Dimensions, Sizings.

# generator.py
File that will have the code generating each board. It will create a random board and the solution. Taking this board, it has a function that converts into the clues for each row and column. Helper functions that count consecutive numbers. Then recheck the clues to make sure there is not more than one solution for these clues. Check this by asking solver_prolog.py for how many solutions exist, and it fails if greater than 1. 

# grid.py
File that has the cell states (filled or empty), the solution grid given by generator.py, the current player’s grid, the function that updates the game state for filling in a tile, a solve state checker.

# renderer.py
File containing the pygame visualization code, by compute clue panel sizes, compute offsets to center puzzle, draw background panel, draw clues (top + left), draw grid cells, draw X marks, draw thin grid lines, draw thick lines every 5 cells, draw status text, convert screen coords → grid coords. Precompute everything that will remain constant, like clues and the grid, and cache this information.Also, use Surface Blitting. Instead of drawing 400 individual rectangles every frame, draw the static grid and clues to a single Surface once, then just "stamp" that surface onto the screen each frame. Only redraw the "X" marks or filled tiles when the game state actually changes.

# input_handler.py
File containing the quit function, mouse handler to update the various states in both grid.py and renderer.py. 
game.py
File that imports all of the other files, and uses them to make a full game. Includes generating the solutions, computing clues, creating grid, update loop of processing the various events, and the draw loop. Break all the code for this into classes to separate the responsibility and keep it from getting too complicated. 

# main.py
File that runs everything. Initializing, creates the window, creates the game, loops through checking for updates and drawing anything needed.

# solver_rand.py (To Be Implemented)
File that will be used to make the solver that uses random generation. Here is the structure for my solver:
Start with blank ones, and use the size of the grid and the numbers in the clues, since between each number has to be 1 blank tile. This means if the (Sum of Clues) + (Number of Clues) - 1 = Row/Column length.
This can give a baseline for any given graph.
Use line based deduction, check early contradictions, add timeout cap so it doesn’t take too long.
Instead of purely random, look into "Overlapping Segments." If a row is 10 wide and the clue is 8, the middle 6 tiles must be filled regardless of where the block starts. This "mathematical certainty" is much faster than random guessing.

# solver_prolog.py (To Be Implemented)
Use clues and prolog to solve the grid. Write a small Prolog DSL generator (Python → Prolog text). Write a parser for Prolog output. Add a fallback if Prolog solver fails or times out. If you plan on using the solver for "hints" during gameplay, use a library like pyswip to keep the Prolog engine in memory, rather than generating a text file and calling a shell command every time.
