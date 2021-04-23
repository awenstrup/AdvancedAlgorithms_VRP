# Base python
from typing import Tuple, List

# Extended Python
import png

class Warehouse:
    """A small utility class to hold information about the warehouse we are opperating in"""

    def __init__(self, path: str):
        if ".txt" in path:
            self.occupancy_grid, self.base = self.load_warehouse(path)
        elif ".png" in path:
            self.occupancy_grid, self.base = self.load_warehouse_from_png(path)
        else:
            raise Exception("Warehouse must be defined in a txt or png file")

    def load_warehouse(self, path: str) -> Tuple[List[List[bool]], Tuple[int, int]]:
        """Given a path to a warehouse file, load it and return the useful information.

        :param str path: The path (hopefully absolute) to the .txt file representing the warehouse.
            See warehouse.txt for an example. A robot starts at A and ends at B.

        :returns:
            * A 2D list of booleans; True spaces are occupied, False spaces can be traveled through.
            * A base point for a single robot
        """
        occupancy_grid: list = []
        base: tuple

        with open(path) as f:
            for i, line in enumerate(f.readlines()):
                for j, char in enumerate(line):
                    if char == "X":
                        occupancy_grid[i].append(True)
                    elif char == " ":
                        occupancy_grid[i].append(False)
                    elif char == "B":
                        occupancy_grid[i].append(False)
                        base = (i, j)

        return occupancy_grid, base

    def load_warehouse_from_png(path: str) -> Tuple[List[List[bool]], Tuple[int, int], Tuple[int, int]]:
        """Given a path to a PNG, load a warehouse.

        Expect obstacles in black, empty space in white, and robot charging
        stations in red
        """
        pass
