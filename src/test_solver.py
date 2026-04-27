#!/usr/bin/env python3

from generator import generate_solution, compute_clues
from solver_rand import solve_with_random_solver

def test_solver():
    # Generate a random solution
    size = 10
    solution = generate_solution(size)
    row_clues, col_clues = compute_clues(solution)

    print("Generated solution:")
    for row in solution:
        print(''.join('█' if c else ' ' for c in row))

    print("\nRow clues:", row_clues)
    print("Col clues:", col_clues)

    # Try to solve
    solved = solve_with_random_solver(row_clues, col_clues, timeout=6000.0)

    if solved:
        print("\nSolver found a solution:")
        for row in solved:
            print(''.join('█' if c else ' ' for c in row))
        print("Matches original:", solved == solution)
    else:
        print("\nSolver failed to find solution within timeout.")

if __name__ == "__main__":
    test_solver()