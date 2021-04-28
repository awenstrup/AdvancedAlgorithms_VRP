from path import Path, save_multiple_paths_as_gif
from utils import Warehouse
import copy

if __name__ == "__main__":
    w1 = Warehouse("warehouse.txt")
    # w1.write_warehouse_to_png("warehouse.png")
    p1 = Path(w1, w1.bases[3], battery_life=10)
    #p2 = Path(w1, w1.bases[1], battery_life=30)
    #p3 = Path(w1, w1.bases[2], battery_life=30)
    #p4 = Path(w1, w1.bases[3], battery_life=30)
    p1.fitness_func(2)
    print(p1.fitness_val)
    for i in range(8000):
        pMutated = copy.deepcopy(p1)
        pMutated.mutate()
        pMutated.fitness_func(2)
        print(p1.fitness_val)
        

        if pMutated.fitness_val>p1.fitness_val:
            print(pMutated.fitness_val)
            p1 = copy.deepcopy(pMutated)
            p1.fitness_func(2)
        
            
       
        
       
        # print(p.coord_list)
    p1.fitness_func(2)
    print(p1.coord_list)
    print(p1.fitness_val)
   
   

    save_multiple_paths_as_gif(10, [p1])