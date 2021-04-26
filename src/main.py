from path import Path
from utils import Warehouse

if __name__ == "__main__":
    w1 = Warehouse("warehouse.png")
    p = Path(w1, battery_life=20)

    for i in range(1000):
        p.mutate()
        print(p.coord_list)