#!/usr/bin/env python3

import sys
import time

# Add src to path
sys.path.append('../src')

from generator import generate_solution, compute_clues
from solver_rand import solve_with_random_solver


def measure_solve_percentage(dimensions, runs=50, timeout=30.0):
    results = {}
    for dim in dimensions:
        solved_count = 0
        for _ in range(runs):
            solution = generate_solution(dim)
            row_clues, col_clues = compute_clues(solution)
            solved = solve_with_random_solver(row_clues, col_clues, timeout=timeout)
            if solved is not None:
                solved_count += 1
        results[dim] = (solved_count, runs)
    return results


def print_solve_percentages(results):
    for dim, (solved_count, runs) in results.items():
        percentage = solved_count / runs * 100
        print(f"{dim}x{dim}: {percentage:.1f}% ({solved_count}/{runs})")


def main():
    dimensions = [3,4,5]
    results = measure_solve_percentage(dimensions, runs=200, timeout=30.0)
    print_solve_percentages(results)


if __name__ == "__main__":
    main()
