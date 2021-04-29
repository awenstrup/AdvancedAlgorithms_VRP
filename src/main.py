from path import Path, save_multiple_paths_as_gif, simulated_annealing, path_evolution_gif
from utils import Warehouse
import copy
from progress.bar import Bar
import random

if __name__ == "__main__":
    w1 = Warehouse("bigWarehouse.txt")
    # w1.write_warehouse_to_png("warehouse.png")
    p1 = Path(w1, w1.bases[0], battery_life=500,vision_radius=2)
    #p2 = Path(w1, w1.bases[1], battery_life=30)
    #p3 = Path(w1, w1.bases[2], battery_life=30)
    #p4 = Path(w1, w1.bases[3], battery_life=30)
    p1.fitness_func()
    print(p1.fitness_val)

    cycles = 30000
    p1, evolutions = simulated_annealing(p1,cycles)

    path_evolution_gif(p1,evolutions,1)
    save_multiple_paths_as_gif(10, [p1])