from path import Path, save_multiple_paths_as_gif, simulated_annealing, path_evolution_gif
from utils import Warehouse
from solution import Solution
from generation import Generation
from evolution import evolve
import copy
from progress.bar import Bar
import random

def solution_factory(w: Warehouse, batt: int):
    paths = []
    for base in w.bases:
        paths.append(Path(w, base, battery_life=batt))
    return Solution(paths)

def generation_factory(w: Warehouse, batt: int, size: int):
    solutions = []
    for i in range(size):
        solutions.append(solution_factory(w, batt))
    return Generation(solutions)

if __name__ == "__main__":
    w1 = Warehouse("warehouse.png")
    w1.write_warehouse_to_png("warehouse.png")

    generation = generation_factory(w1, batt=30, size=12)

    generation = evolve(generation, cycles=500)

    save_multiple_paths_as_gif(
        10, 
        [
            generation.solutions[0].paths[0],
            generation.solutions[0].paths[1],
            generation.solutions[0].paths[2],
            generation.solutions[0].paths[3],
        ]
    )

    # p1.fitness_func()
    # print(p1.fitness_val)
    # cycles = 30000
    # p1, evolutions = simulated_annealing(p1,cycles)
    # path_evolution_gif(p1,evolutions,1)
    # save_multiple_paths_as_gif(10, [p1])