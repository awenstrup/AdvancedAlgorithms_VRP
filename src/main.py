from path import Path, save_multiple_paths_as_gif
from utils import Warehouse

if __name__ == "__main__":
    w1 = Warehouse("warehouse.txt")
    # w1.write_warehouse_to_png("warehouse.png")
    p1 = Path(w1, w1.bases[0], battery_life=30)
    p2 = Path(w1, w1.bases[1], battery_life=30)
    p3 = Path(w1, w1.bases[2], battery_life=30)
    p4 = Path(w1, w1.bases[3], battery_life=30)

    for i in range(5000):
        p1.mutate()
        p2.mutate()
        p3.mutate()
        p4.mutate()
        # print(p.coord_list)

    save_multiple_paths_as_gif(10, [p1, p2, p3, p4])