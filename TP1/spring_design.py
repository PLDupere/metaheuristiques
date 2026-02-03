# 1.2. Problème d’optimisation
import numpy as np
from scipy.optimize import minimize

class SpringDesign:

    def __init__(self):
        # Bornes x[0], x[1], x[2]
        self.bounds = [(0.05, 2.00), (0.25, 1.30), (2.00, 15.0)]

        # Définir les contraintes
        # https://docs.scipy.org/doc/scipy/tutorial/optimize.html
        self.constraints = [
            {'type': 'ineq', 'fun': self.constraint_g1},
            {'type': 'ineq', 'fun': self.constraint_g2},
            {'type': 'ineq', 'fun': self.constraint_g3},
            {'type': 'ineq', 'fun': self.constraint_g4},
        ]

    # Minimiser la fonction
    def spring_function(self, x):
        return x[0]**2 * x[1] + (2 + x[3])

    # Sujette aux contraintes
    def constraint_g1(self, x):
        return (1 - (x[1]**3 * x[2]) / (71785 * x[0]**4)) <= 0

    def constraint_g2(self, x):
        return ((4 * x[1]**2 - x[0] * x[1]) / (12566 * (x[1] * x[0]**3 - x[0]**4))) + (1 / (5108 * x[0]**2)) - 1 <= 0

    def constraint_g3(self, x):
        return 1 - (140.45 * x[0]) / (x[1]**2 * x[2]) <= 0

    def constraint_g4(self, x):
        return ((x[0] + x[1]) / 1.5) - 1 <= 0
