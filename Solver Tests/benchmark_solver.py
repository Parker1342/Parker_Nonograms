#!/usr/bin/env python3

import sys
import time
import csv
import os

# Add src to path
sys.path.append('../src')

from generator import generate_solution, compute_clues
from solver_rand import solve_with_random_solver

def benchmark_solver():
    times = []
    dimensions = []
    run_numbers = []

    for dim in range(3, 9):
        print(f"Testing dimension {dim}x{dim}")
        for run in range(1, 51):
            # Generate puzzle
            solution = generate_solution(dim)
            row_clues, col_clues = compute_clues(solution)

            # Time the solve
            start_time = time.time()
            solved = solve_with_random_solver(row_clues, col_clues, timeout=30.0)
            end_time = time.time()
            solve_time = end_time - start_time

            if solved is not None:
                times.append(solve_time)
                dimensions.append(dim)
                run_numbers.append(run)
                print(f"  Run {run}: {solve_time:.4f}s")
            else:
                print(f"  Run {run}: Failed to solve")

    # Write to CSVs
    with open('times.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time'])
        for t in times:
            writer.writerow([t])

    with open('dimensions.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['dimension'])
        for d in dimensions:
            writer.writerow([d])

    with open('run_numbers.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['run'])
        for r in run_numbers:
            writer.writerow([r])

    print("Benchmark complete. Results saved to times.csv, dimensions.csv, run_numbers.csv")

if __name__ == "__main__":
    benchmark_solver()