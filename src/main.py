from path import Path, save_multiple_paths_as_gif
from utils import Warehouse
import copy
from progress.bar import Bar
import random

if __name__ == "__main__":
    w1 = Warehouse("bigWarehouse.txt")
    # w1.write_warehouse_to_png("warehouse.png")
    p1 = Path(w1, w1.bases[0], battery_life=30)
    #p2 = Path(w1, w1.bases[1], battery_life=30)
    #p3 = Path(w1, w1.bases[2], battery_life=30)
    #p4 = Path(w1, w1.bases[3], battery_life=30)
    p1.fitness_func(1)
    print(p1.fitness_val)

    cycles = 5000
    bar = Bar('Mutating', max=cycles)
    for i in range(cycles):
        pMutated = copy.deepcopy(p1)
        pMutated.mutate()
        pMutated.distance_multiplier = .01*(i/cycles)
        pMutated.fitness_func(1)
        # print(p1.fitness_val)
        

        if pMutated.fitness_val>p1.fitness_val or (random.random() > i/cycles):
            print(pMutated.fitness_val)
            p1 = copy.deepcopy(pMutated)
            p1.fitness_func(1)

        bar.next()
       
    print(p1.coord_list)
        
    bar.finish()
    p1.fitness_func(1)
    print(p1.coord_list)
    print(p1.fitness_val)
      

    save_multiple_paths_as_gif(10, [p1])