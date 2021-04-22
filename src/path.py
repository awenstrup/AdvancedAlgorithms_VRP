# Base python imports
from typing import Tuple, Optional, List

# Project imports
from utils import Warehouse


class Path:
    def __init__(self, warehouse: Warehouse, path: Optional[List[Tuple[int, int]]] = None):
        """Initialize a new (2 dimensional) Path object

        A path consists of a list of tuples, representing points in 2D space.
        The path is defined within an occupancy grid, so points in space are
        discrete and coordinates are given with integers.

        :param Warehouse warehouse: The warehouse we are opperating in.
        :param list path: An optional parameter. A list of tuples (2D points)
            that have been traveled through so far
        """
        self.path = path if path else []
        self.warehouse = warehouse

    def get_current_location(self) -> Tuple[int, int]:
        """Get the most recent point on the path"""
        return self.path[-1]

    def get_neighbors(self) -> List[Tuple[int, int]]:
        """Get the neighbors of the most recent point on the path"""
        x, y = self.path[-1]
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def get_valid_neighbors(self) -> List[Tuple[int, int]]:
        """Get the valid neighbors of the most recent point on the path.

        A neighbor is valid if it does not intersect any occupied space in the
        warehouse.
        """
        return [p for p in self.get_neighbors() if (self.warehouse[p[0]][p[1]] == False)]

    def add_point(self, point: Tuple[int, int]) -> None:
        """Add a new point to the path"""
        self.path.append(point)
