from typing import Tuple, List


class Warehouse:
    """A small utility class to hold information about the warehouse we are opperating in"""

    def __init__(self, path):
        self.occupancy_grid, self.start, self.end = self.load_warehouse(path)

    def load_warehouse(self, path: str) -> Tuple[List[List[bool]], Tuple[int, int], Tuple[int, int]]:
        """Given a path to a warehouse file, load it and return the useful information.

        :param str path: The path (hopefully absolute) to the .txt file representing the warehouse.
            See warehouse.txt for an example. A robot starts at A and ends at B.

        :returns:
            * A 2D list of booleans; True spaces are occupied, False spaces can be traveled through.
            * A start point for a single robot
            * An end point for a single robot
        """
        occupancy_grid: list = []
        start: tuple
        end: tuple

        with open(path) as f:
            for i, line in enumerate(f.readlines()):
                for j, char in enumerate(line):
                    if char == "X":
                        occupancy_grid[i][j] = True
                    elif char == " ":
                        occupancy_grid[i][j] = False
                    elif char == "A":
                        occupancy_grid[i][j] = False
                        start = (i, j)
                    elif char == "B":
                        occupancy_grid[i][j] = False
                        end = (i, j)

        return occupancy_grid, start, end
