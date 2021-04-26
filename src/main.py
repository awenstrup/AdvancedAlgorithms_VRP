from path import Path
from utils import Warehouse

if __name__ == "__main__":
    w1 = Warehouse("warehouse.txt")
    w1.write_warehouse_to_png("warehouse.png")
    p = Path(w1, w1.bases[0], battery_life=20)

    for i in range(1000):
        p.mutate()
        # print(p.coord_list)

    p.save_as_gif(5)