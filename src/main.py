from path import Path, save_multiple_paths_as_gif
from utils import Warehouse

if __name__ == "__main__":
    w1 = Warehouse("warehouse.png")
    # w1.write_warehouse_to_png("warehouse.png")
    p1 = Path(w1, w1.bases[0], battery_life=20)
    p2 = Path(w1, w1.bases[1], battery_life=20)

    for i in range(5000):
        p1.mutate()
        p2.mutate()
        # print(p.coord_list)

    save_multiple_paths_as_gif(5, [p1, p2])