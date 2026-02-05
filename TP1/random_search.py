# 1.3. Recherche aléatoire
import numpy as np
from spring_design import SpringDesign
from hill_climbing import HillClimbing
from generalized_hill_climbing import GeneralizedHillClimbing
from contraintes_stagnation import ContraintesStagnation
# from scipy.optimize import minimize

class RandomSearch:

    def __init__(self):
        self.spring_design = SpringDesign()
        self.best_solution = None
        self.best_cost = float('inf')

    def generate_random_solution(self):
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html
        return [
            np.random.uniform(self.spring_design.bounds[0][0], self.spring_design.bounds[0][1]),  # x[0]
            np.random.uniform(self.spring_design.bounds[1][0], self.spring_design.bounds[1][1]),  # x[1]
            np.random.uniform(self.spring_design.bounds[2][0], self.spring_design.bounds[2][1]),  # x[2]
        ]

    def evaluate(self, montecarlo_value, heuristique_value):
        initial_solution = self.generate_random_solution()

        if heuristique_value == 1:
            heuristique = HillClimbing(self.spring_design, delta = 0.01, max_iterations = montecarlo_value)
        elif heuristique_value == 2:
            heuristique = GeneralizedHillClimbing()
        elif heuristique_value == 3:
            heuristique = ContraintesStagnation()
        else:
            raise ValueError("Error: Heuristique non reconnue")

        best_solution, best_cost = heuristique.optimize(initial_solution)
        return best_solution, best_cost

