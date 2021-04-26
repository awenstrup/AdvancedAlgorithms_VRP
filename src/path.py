# Base python imports
import random
from typing import Tuple, Optional, List, Union

# Project imports
from utils import Warehouse


class Path:
    def __init__(
        self, 
        warehouse: Warehouse, 
        base: Tuple[int, int],
        battery_life: int = 100, 
        coord_list: Optional[List[Tuple[int, int]]] = None
    ):
        """Initialize a new (2 dimensional) Path object

        A path consists of a list of tuples, representing points in 2D space.
        The path is defined within an occupancy grid, so points in space are
        discrete and coordinates are given with integers.

        :param Warehouse warehouse: The warehouse we are opperating in.
        :param list path: An optional parameter. A list of tuples (2D points)
            that have been traveled through so far
        """
        self.warehouse = warehouse
        self.base = base
        self.battery_life = battery_life
        self.coord_list = coord_list if coord_list else [base for i in range(battery_life)]

    def get_current_location(self) -> Tuple[int, int]:
        """Get the most recent point on the path
        
        NOT USED
        """
        pass

    def get_neighbors(self, index: Union[int, Tuple[int, int]] = 0) -> List[Tuple[int, int]]:
        """Get the neighbors of a point in the path. Accepts either an
        index in the coordinate list or a coordinate itself.
        
        :param Union[int, Tuple[int, int]] index: 
            Either an int, representing the index to look up in
            the coordinate list, or a coordinate itself

        :rtype: List[Tuple[int, int]]
        :returns: All valid neighbors, including the point itself 
            (not moving during a timestep is valid)
        """
        if type(index) is int:
            x, y = self.coord_list[index]
        elif type(index) is tuple:
            x, y = index
        else:
            raise TypeError(
                f"Invalid type passed to Path.get_neighbors: {type(index)}. Expected int or tuple."
            )
        return [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def get_valid_neighbors(self, index: Union[int, Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Get the valid neighbors of the most recent point on the path.

        A neighbor is valid if it does not intersect any occupied space in the
        warehouse.
        """
        out = []
        neighbors = self.get_neighbors(index)
        for n in neighbors:
            if (self.warehouse.occupancy_grid[n[0]][n[1]] == False):
                out.append(n)
        
        return out

    def euclidean_dist(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """Get the euclidean distance between two points"""
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
    
    def valid_mutation_indices(self) -> List[int]:
        """Get a list of places in the path where a mutation is possible

        :rtype: List[int]
        :returns: All indices in self.coord_path where a mutation is possible.
        """
        mutation_indices = []
        
        for i in range(1,len(self.coord_list)-1):
            start = self.coord_list[i-1]
            end = self.coord_list[i+1]

            # really 2 but 1.9 to avoid floating point errors
            if self.euclidean_dist(start, end) < 1.9:  
                 mutation_indices.append(i)

        return mutation_indices
            
    def mutate(self) -> None:
        """Mutate around a random point where a mutation is valid"""

        # Find all valid places to mutate
        potential_targets: List[int] = self.valid_mutation_indices()

        # Select a single index to mutate around
        target_index: int = random.choice(potential_targets)

        # Find all potential muations about the index
        n1: List[Tuple[int, int]] = set(self.get_valid_neighbors(target_index - 1))
        n2: List[Tuple[int, int]] = set(self.get_valid_neighbors(target_index + 1))
        overlap = n1.intersection(n2)
    
        # Choose a random valid neighbor to mutate to
        mutated_coord: Tuple[int, int] = random.choice(list(overlap))

        # Add mutated coordinate into path
        self.coord_list[target_index] = mutated_coord

        # Check if valid
        # Only run in debugging, all mutations should be valid
        # self.check_is_valid()

    def check_is_valid(self) -> None:
        """Check that the current coord_list is valid

        Robots are allowed to move up, down, left, or right 1 unit per timestep

        Raise an exception if the coordinate list is no longer valid
        """
        for i in range(len(self.coord_list) - 1):
            here = self.coord_list[i]
            there = self.coord_list[i+1]
            if (here[0] != there[0] and here[1] != there[1]):
                print(f"Moving from: {here} to: {there} is not allowed!")
                raise Exception(f"Invalid coord_list: {self.coord_list}")
        
    def fitness_func(self):
        pass
        self.fitness_val = 0
        for coordinate in self.coord_list:
            surveyedNodes = []
            print(0)
        # return self.fitness_val

    def add_point(self, point: Tuple[int, int]) -> None:
        """Add a new point to the path"""
        self.coord_list.append(point)
        
