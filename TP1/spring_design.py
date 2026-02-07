import numpy as np


class SpringDesign:

    def __init__(self):
        self.bounds = [ (0.05, 2.00), # Bornes x[0] = diamètre du fil
                        (0.25, 1.30), # Bornes x[1] = diamètre de la spirale
                        (2.00, 15.0)] # Bornes x[2] = nombre de spirales

    def calcul_spring(self, x):
        if not self.is_valid(x):
            return float('inf')
        # TODO: Ajouter pénalité pour contraintes violées
        return x[0]**2 * x[1] + (2 + x[2])

    def __constraint_g1(self, x):
        result_g1 = 1 - (x[1]**3 * x[2]) / (71785 * x[0]**4)
        return result_g1 <= 0

    def __constraint_g2(self, x):
        result_g2 = ((4 * x[1]**2 - x[0] * x[1]) / (12566 * (x[1] * x[0]**3 - x[0]**4))) + (1 / (5108 * x[0]**2)) - 1
        return result_g2 <= 0

    def __constraint_g3(self, x):
        result_g3 = 1 - (140.45 * x[0]) / (x[1]**2 * x[2])
        return result_g3 <= 0

    def __constraint_g4(self, x):
        result_g4 = ((x[0] + x[1]) / 1.5) -1
        return result_g4 <= 0

    def __generate_random_solution(self):
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html
        return [
            np.random.uniform(self.bounds[0][0], self.bounds[0][1]),  # x[0]
            np.random.uniform(self.bounds[1][0], self.bounds[1][1]),  # x[1]
            np.random.uniform(self.bounds[2][0], self.bounds[2][1])   # x[2]
        ]

    def is_valid(self, x):
        safe_bounds = x.copy()
        for i in range(len(safe_bounds)):
            if safe_bounds[i] < self.bounds[i][0]:
                return False
            elif safe_bounds[i] > self.bounds[i][1]:
                return False
                

        if self.__constraint_g1(safe_bounds) == False:
            return False
        if self.__constraint_g2(safe_bounds) == False:
            return False
        if self.__constraint_g3(safe_bounds) == False:
            return False
        if self.__constraint_g4(safe_bounds) == False:
            return False

        return True

    def generate_valid_random_solution(self):
        while True:
            solution = self.__generate_random_solution()
            if self.is_valid(solution):
                return solution
