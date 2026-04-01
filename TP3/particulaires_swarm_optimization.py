import numpy as np
from helper import Helper
from spring_design import SpringDesign

class ParticulairesSwarmOptimization:

    def __init__(self, max_iterations):
        self.spring_design = SpringDesign()
        self.max_iterations = max_iterations


    def optimize(self):
        best_solution = None
        best_cost = float('inf')

        for iteration in range(self.max_iterations):
            pass

        return best_solution, best_cost