# Base python imports
import os
import random
import copy
from typing import Tuple, Optional, List, Union
import numpy as np
import math

# Extended python imports
from progress.bar import Bar
from PIL import Image, ImageOps
import png

# Project imports
from utils import Warehouse


class Path:
    def __init__(
        self, 
        warehouse: Warehouse, 
        base: Tuple[int, int],
        battery_life: int = 100, 
        vision_radius: int = 1,
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
        # Naive coord list initialization: [self.base for i in range(self.battery_life)]
        self.coord_list = coord_list if coord_list else self.gen_init_path()
        self.vision_radius = vision_radius
        self.distance_multiplier = 1

    def copy(self):
        return Path(
            self.warehouse, 
            self.base, 
            self.battery_life, 
            self.vision_radius, 
            list(self.coord_list))
        
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

    def gen_init_path(self) -> None:
        """Generate a better initial path"""
        # Initialize path
        coord_list = []
        coord_list.append(self.base)

        # Greedy algorithm generates path away from base
        while(len(coord_list) < (self.battery_life/2)):
            choices = self.get_valid_neighbors(coord_list[-1])
            # introduce a tiny bit of noise to the greedy choices,
            # to choose different paths when they are just as good
            choice = max(
                choices, 
                key = lambda x : self.euclidean_dist(self.base, x) + 
                (random.random()/20)
            )
            coord_list.append(choice)

        # Return to base
        for i, c in enumerate(reversed(coord_list)):
            if i == 0 and (self.battery_life % 2) == 1:
                # don't reppeat furthest point if batt_life is odd
                pass
            else:
                coord_list.append(c)

        self.coord_list = coord_list
        return coord_list
        

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
        overlap = n1 & n2
    
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
        self.fitness_val = 0
        timeStepMap = copy.deepcopy((np.invert(self.warehouse.png_write_helper())+256)/255)
        timeMap = copy.deepcopy(10*self.battery_life*(np.invert(self.warehouse.png_write_helper())+256)/255)
        
        for timeStep in range(len(self.coord_list)):
            #for robot in range(len(self.coord_list[0])):
            for point in self.surveyedNodes(self.coord_list[timeStep]):
                self.fitness_val += timeMap[point[0],point[1]]
                self.fitness_val += self.distance_multiplier*self.euclidean_dist(self.coord_list[0],point)
                timeMap[point[0],point[1]] = 0
            timeMap += timeStepMap

        # print(f"Fitness: ",{self.fitness_val})
            
        return self.fitness_val

    def add_point(self, point: Tuple[int, int]) -> None:
        """Add a new point to the path"""
        self.coord_list.append(point)

    def surveyedNodes(self, point:Tuple[int,int]):
        xLoc = point[0]
        yLoc = point[1]
        surveyedNodes = []
        
        for x in range(xLoc-self.vision_radius,xLoc+self.vision_radius+1):
            for y in range(yLoc-self.vision_radius, yLoc+self.vision_radius+1):

                try:
                    if (self.warehouse.occupancy_grid[x][y] == False):
                        node = (x,y)
                        surveyedNodes.append(node)
                except IndexError:
                    pass
        return surveyedNodes
        
    def save_as_gif(self, time: int):
        """Save the current path as a gif
        
        :param int time: The total time for the gif. Change this depending
            on how long the battery life is and how quickly you want 
            the robot to move
        """
        # Create all PNGs
        for i, frame in enumerate(self.coord_list):
            with open(f"temp_{i}.png", 'wb') as f:
                w = png.Writer(
                    len(self.warehouse.occupancy_grid[0]),
                    len(self.warehouse.occupancy_grid),
                    greyscale=True
                )
                data = self.warehouse.png_write_helper()
                for b in self.warehouse.bases:
                    data[b[0]][b[1]] = 127
                data[frame[0]][frame[1]] = 63
                w.write(f, data)

        # Load the PNGs
        frames = []
        for i in range(self.battery_life):
            new_frame = Image.open(f"temp_{i}.png")
            frames.append(new_frame)
        
        # Save into a GIF file that loops forever
        frames[0].save("path.gif", format='GIF',
                    append_images=frames[1:],
                    save_all=True,
                    duration=(time/self.battery_life), loop=0)

        # Purge temporary PNGs
        for i in range(self.battery_life):
            new_frame = os.remove(f"temp_{i}.png") 


def simulated_annealing(path:Path,cycles:int):
    pathEvolutions = []
    pathEvolutions.append(path.coord_list)
    bar = Bar('Mutating', max=cycles)
    k = 1.5
    for i in range(cycles):
        pMutated = copy.deepcopy(path)
        pMutated.mutate()

        pMutated.distance_multiplier = math.exp((-1*abs(pMutated.fitness_val-path.fitness_val))/(k*i)) #.01*(i/cycles)
        pMutated.fitness_func()
        

        if pMutated.fitness_val>path.fitness_val or (random.random() > math.exp((-1*abs(pMutated.fitness_val-path.fitness_val))/(k*i))):
            print(pMutated.fitness_val)
            path = copy.deepcopy(pMutated)
            pathEvolutions.append(path.coord_list)
            path.fitness_func()

        bar.next()
       
    bar.finish()
    path.fitness_func()
    return path, pathEvolutions
    
def save_multiple_paths_as_gif(time: int, paths: List[Path]) -> None:
    """Save a list of paths to a single gif"""
    # Define the color palette for the gif
    palette = [
        (0xFF, 0xFF, 0xFF), # white for empty space
        (0x00, 0x00, 0x00), # black for obstacles
        (0x77, 0x77, 0x77), # gray for base stations
        (0xFF, 0x00, 0x00), # red for a robot
        (0x00, 0x00, 0xFF), # blue for a robot
        (0x00, 0xFF, 0x00), # green for a robot
        (0xFF, 0x69, 0x00), # orange for a robot
        (0x6a, 0x00, 0xFF), # purple for a robot
        ]

    # Create all PNGs
    for i, frame in enumerate(paths[0].coord_list):
        with open(f"temp_{i}.png", 'wb') as f:
            w = png.Writer(
                len(paths[0].warehouse.occupancy_grid[0]),
                len(paths[0].warehouse.occupancy_grid),
                palette=palette,
                bitdepth=4
            )

            # Get data, mapped from 0-1 not 0-255
            data = paths[0].warehouse.png_write_helper()
            for y, r in enumerate(data):
                for x, c in enumerate(r):
                    data[y][x] = 1 if c == 255 else 0

            color: int = 3 # red is at index 3 in the color palette
            for path in paths:
                data[path.base[0]][path.base[1]] = 2 
                data[path.coord_list[i][0]][path.coord_list[i][1]] = color
                color += 1
                if color > 7: color = 3
            w.write(f, data)
        scale_up_png(f"temp_{i}.png", 10)

    # Load the PNGs
    frames = []
    for i in range(paths[0].battery_life):
        new_frame = Image.open(f"temp_{i}.png")
        frames.append(new_frame)
    
    # Save into a GIF file that loops forever
    frames[0].save("path.gif", format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=(time/paths[0].battery_life), loop=0)

    # Purge temporary PNGs
    for i in range(paths[0].battery_life):
        new_frame = os.remove(f"temp_{i}.png") 


def path_evolution_gif(evolvedPath, pathList,time):

    """Save a list of paths to a single gif"""
    # Define the color palette for the gif
    palette = [
        (0xFF, 0xFF, 0xFF), # white for empty space
        (0x00, 0x00, 0x00), # black for obstacles
        (0x77, 0x77, 0x77), # gray for base stations
        (0xFF, 0x00, 0x00), # red for a robot
        (0x00, 0x00, 0xFF), # blue for a robot
        (0x00, 0xFF, 0x00), # green for a robot
        (0xFF, 0x69, 0x00), # orange for a robot
        (0x6a, 0x00, 0xFF), # purple for a robot
        ]
   
    # Create all PNGs
    for i, path in enumerate(pathList):
        with open(f"temp_{i}.png", 'wb') as f:
            w = png.Writer(
                len(evolvedPath.warehouse.occupancy_grid[0]),
                len(evolvedPath.warehouse.occupancy_grid),
                palette=palette,
                bitdepth=4
            )

            # Get data, mapped from 0-1 not 0-255
            data =  evolvedPath.warehouse.png_write_helper()
            for y, r in enumerate(data):
                for x, c in enumerate(r):
                    data[y][x] = 1 if c == 255 else 0

            color: int = 3 # red is at index 3 in the color palette

            for coord in path:
                data[coord[0]][coord[1]] = 3
                data[coord[0]][coord[1]] = color
            w.write(f, data)
            
    print("SUCCESFULLY")
     # Load the PNGs
    frames = []
    '''
    for i in range(len(pathList)):
        print(i)
        new_frame = Image.open(f"temp_{i}.png")
        frames.append(new_frame)
        #new_frame.close()
        os.remove(f"temp_{i}.png") 
    '''
    for i in range(len(pathList)):
        img = Image.open(f"temp_{i}.png")
        frames.append(img.copy())
        img.close()
    # Save into a GIF file that loops forever
    frames[0].save("path2.gif", format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=(time/evolvedPath.battery_life), loop=0)

    #Purge temporary PNGs
    for i in range(len(pathList)):
       os.remove(f"temp_{i}.png") 

def scale_up_png(filepath: str, scale: int) -> None:
    """Scale up a .png file by a factor of scale"""
    mat = []

    # Define the color palette for the gif

    with open(filepath, 'rb') as f:
        reader = png.Reader(file=f)
        w, h, data, info = reader.read()
        for i, line in enumerate(data):
            # write each line scale times
            for x in range(scale):
                mat.append([])
                for j, pixel in enumerate(line):
                    # write each pixel scale times
                    for y in range(scale):
                        mat[-1].append(pixel)

    with open(filepath, 'wb') as f:
        writer = png.Writer(
            len(mat[0]),
            len(mat),
            greyscale=info["greyscale"],
            bitdepth=info["bitdepth"],
            palette=info["palette"]
        )
        writer.write(f, mat)


    
      




        
