# Base python imports
from path import save_multiple_paths_as_gif
from typing import List
import random

# Project imports
from generation import Generation

def evolve(gen1: Generation, cycles: int = 40):
    """Given an initial generation and number of cycles, evolve!"""
    # Establish working generation
    curr = gen1.copy()
    num_solutions = len(gen1.solutions)

    for c in range(cycles):
        # Sort solutions from best to worst
        curr.solutions.sort(key=lambda x : x.fitness_func(), reverse=True)
        if (c % 10 == 0): print(curr)

        # Select top half of solutions, insert them each twice, make a new generation
        best = []
        n = int(num_solutions / 2)

        for i in range(n):
            best.append(curr.solutions[i].copy())
        for i in range(n):
            best.append(curr.solutions[i].copy())
        if (n % 2): best.append(curr.solutions[0])

        curr = Generation(best)

        # Crossover - only crossover the last half, 
        # keep the best solutions untouched
        for i in range(3): # arbitrary
            u, v = random.choices(range(n, num_solutions), k=2)
            curr.crossover(u, v)

        # Mutate - all
        for i in range(5): # arbitrary
            curr.mutate()
    
    save_multiple_paths_as_gif(10, curr.solutions[0].paths)
    return curr


