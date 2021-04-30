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
        def row(i): [int(not b) for b in grid[i]]
    
        # use arrays for 2D array addition
        time_step_map = np.array([row(i) for i in grid]) 
        time_map = np.copy(time_step_map)
        
        # Iterate over the path, step by step
        for ts in range(len(self.paths[0].coord_list)):

            # For each point that any robot is looking at during the current timestep
            for y, x in self.surveyed_nodes(ts):
                self.fitness_val += time_map[y][x]
                time_map[y][x] = 0
            time_map += time_step_map
            
        return out

    def surveyed_nodes(self, time: int) -> List[Tuple[int, int]]:
        """Get all coordinated under surveillance at a given timestep"""
        # Initialize output list
        out = []

        # Append all visible points
        for path in self.paths:
            out.append(path.surveyedNodes(path.coord_list[time]))
    
        # Remove duplicates
        return list(set(out))


