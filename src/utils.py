# Base python
from typing import Tuple, List

# Extended Python
import png

class Warehouse:
    """A small utility class to hold information about the warehouse we are opperating in"""

    def __init__(self, file_path: str):
        if ".txt" in file_path:
            self.occupancy_grid, self.bases = self.load_warehouse_from_txt(file_path)
        elif ".png" in file_path:
            self.occupancy_grid, self.bases = self.load_warehouse_from_png(file_path)
        else:
            raise Exception("Warehouse must be defined in a txt or png file")

        print(self.bases)

    def load_warehouse_from_txt(self, path: str) -> Tuple[List[List[bool]], List[Tuple[int, int]]]:
        """Given a path to a warehouse file, load it and return the useful information.

        :param str path: The path (hopefully absolute) to the .txt file representing the warehouse.
            See warehouse.txt for an example. A robot starts at A and ends at B.

        :returns:
            * A 2D list of booleans; True spaces are occupied, False spaces can be traveled through.
            * A base point for a single robot
        """
        occupancy_grid: List[List[bool]] = []
        bases: List[tuple] = []

        with open(path) as f:
            for i, line in enumerate(f.readlines()):
                occupancy_grid.append([])
                for j, char in enumerate(line):
                    if char == "X":
                        occupancy_grid[i].append(True)
                    elif char == " ":
                        occupancy_grid[i].append(False)
                    elif char == "B":
                        occupancy_grid[i].append(False)
                        bases.append((i, j))

        return occupancy_grid, bases

    def load_warehouse_from_png(self, path: str) -> Tuple[List[List[bool]], Tuple[int, int], Tuple[int, int]]:
        """Given a path to a PNG, load a warehouse.

        Expect obstacles in black, empty space in white, and robot charging
        stations in red
        """
        occupancy_grid: List[List[bool]] = []
        bases: List[Tuple[int, int]] = []

        with open(path, 'rb') as f:
            reader = png.Reader(file=f)
            w, h, data, info = reader.read()

            for i, line in enumerate(data):
                occupancy_grid.append([])
                for j, val in enumerate(line):
                    if val == 255:
                        occupancy_grid[i].append(True)
                    elif val == 0:
                        occupancy_grid[i].append(False)
                    else:
                        occupancy_grid[i].append(False)
                        bases.append((i, j))

            return occupancy_grid, bases

    def png_write_helper(self) -> List[List[int]]:
        out = []
        for line in self.occupancy_grid:
            row = []
            out.append(row)
            for j in line:
                row.append(j * 255)
        return out

    def write_warehouse_to_png(self, path: str) -> None:
        """Given a warehouse, create a .png file to represent it
        
        Black pixels are occupied space, white pixels are free
        """
        with open(path, 'wb') as f:
            w = png.Writer(
                len(self.occupancy_grid[0]),
                len(self.occupancy_grid),
                greyscale=True
            )
            data = self.png_write_helper()
            for b in self.bases:
                data[b[0]][b[1]] = 127
            w.write(f, data)

