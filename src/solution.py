# Base python imports
from typing import List, Tuple

# Extended python imports
import numpy as np

# Project imports
from path import Path

class Solution:
    def __init__(self, paths: List[Path]):
        self.paths = paths
        self.fitness_val = 0

    def copy(self):
        return Solution([p.copy() for p in self.paths])

    def surveillance_score(self) -> int:
        """Return the portion of the fitness function corresponding
        to how well the robots are surveiling
        """
        # Initialize output variable
        out = 0

        # Pull out a few useful variables for later
        warehouse = self.paths[0].warehouse
        grid = warehouse.occupancy_grid

        # Initialize warehouse grid score matrices
        # 0's where a wall is located, 1's in empty space
        def row(i): return [int(not b) for b in grid[i]]
    
        # use arrays for 2D array addition
        time_step_map = np.array([row(i) for i in range(len(grid))]) 
        time_map = np.copy(time_step_map)
        
        # Iterate over the path, step by step
        for ts in range(len(self.paths[0].coord_list)):

            # For each point that any robot is looking at during the current timestep
            for y, x in self.surveyed_nodes(ts):
                out += time_map[y][x]
                time_map[y][x] = 0
            time_map += time_step_map
            
        self.fitness_val = out
        return out

    def surveyed_nodes(self, time: int) -> List[Tuple[int, int]]:
        """Get all coordinated under surveillance at a given timestep"""
        # Initialize output list
        out = []

        # Append all visible points
        for path in self.paths:
            out.extend(path.surveyedNodes(path.coord_list[time]))
    
        # Remove duplicates
        return list(set(out))

    def distance_score(self) -> float:
        """Get the component of the fitness function that
        encourages robots to venture away from their bases
        """
        coef = 10
        out = 0.0

        # Iterate over the paths, step by step
        for ts in range(len(self.paths[0].coord_list)):
            for path in self.paths:
                # Add the distance between the robot and its base
                out += coef * path.euclidean_dist(path.base, path.coord_list[ts])

        return out

    def fitness_func(self) -> float:
        """Evaluate a solution's fitness, store and return it"""
        self.fitness_val = self.surveillance_score() + self.distance_score()
        return self.fitness_val


