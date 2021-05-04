# Base python imports
from typing import List
import random

# Project imports
from solution import Solution

class Generation:
    def __init__(self, solutions: List[Solution]):
        self.solutions = solutions

    def copy(self):
        return Generation([s.copy() for s in self.solutions])

    def mutate(self):
        """Insert a random mutation into a random path 
        in a random solution

        :rtype: Path
        :returns: The path that was mutated
        """
        sol = random.choice(self.solutions)
        path = random.choice(sol.paths)
        path.mutate()
        return path
    
    def crossover(
        self, 
        solution_one_index: int = -1, 
        solution_two_index: int = -1,
        allow_same: bool = False
        ) -> None:
        """Swap two paths from two provided solutions. If none provided,
        choose them randomly.

        :param int solution_one_index: The index in self.solutions of
            the first solution. Default to random.

        :param int solution_two_index: The index in self.solutions of
            the second solution. Default to random.

        :param bool allow_same: Allow the two solutions whose paths are being
            swapped to be the same solution. Default to False.

        :returns: None
        """
        # Select random paths from solutions
        s1 = random.choice(self.solutions) if solution_one_index == -1 else self.solutions[solution_one_index]
        s2 = random.choice(self.solutions) if solution_two_index == -1 else self.solutions[solution_two_index]

        # Force the solutions to be different
        while ((s1 is s2) and (not allow_same)):
            s2 = random.choice(self.solutions)

        p: int = random.choice(range(len(s1.paths)))
        
        # Swap p1 and p2
        tmp = s1.paths[p]
        s1.paths[p] = s2.paths[p]
        s2.paths[p] = tmp

    def __str__(self):
        return f"Evolution fitnesses: {self.solutions[0].fitness_func()}"

    