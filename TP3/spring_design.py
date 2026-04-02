import numpy as np
import os


class SpringDesign:

    def __init__(self):
        os.makedirs("results", exist_ok=True)
        self.bounds = [ (0.05, 2.00), # Bornes x[0] = diamètre du fil
                        (0.25, 1.30), # Bornes x[1] = diamètre de la spirale
                        (2.00, 15.0)] # Bornes x[2] = nombre de spirales


    def calcul_spring(self, x):
        # if not self.is_valid(x):
        #     return self.__penalty(x)
        return x[0]**2 * x[1] + (2 + x[2])


    def __calcul_g1(self, x):
        return 1 - (x[1]**3 * x[2]) / (71785 * x[0]**4)

    def __calcul_g2(self, x):
        return ((4 * x[1]**2 - x[0] * x[1]) / (12566 * (x[1] * x[0]**3 - x[0]**4))) + (1 / (5108 * x[0]**2)) - 1

    def __calcul_g3(self, x):
        return 1 - (140.45 * x[0]) / (x[1]**2 * x[2])

    def __calcul_g4(self, x):
        return ((x[0] + x[1]) / 1.5) -1

    def __constraint_g1(self, x):
        return self.__calcul_g1(x) <= 0

    def __constraint_g2(self, x):
        return self.__calcul_g2(x) <= 0

    def __constraint_g3(self, x):
        return self.__calcul_g3(x) <= 0

    def __constraint_g4(self, x):
        return self.__calcul_g4(x) <= 0


    def generate_random_solution(self):
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

    def __penalty(self, x):
        penalty = 0.0

        for i in range(len(x)):
            lower, upper = self.bounds[i]
            if x[i] < lower:
                penalty += (lower - x[i]) * 20
            elif x[i] > upper:
                penalty += (x[i] - upper) * 20

        g1_penalty = self.__calcul_g1(x)
        if g1_penalty > 0:
            penalty += g1_penalty * 20
        g2_penalty = self.__calcul_g2(x)
        if g2_penalty > 0:
            penalty += g2_penalty * 20
        g3_penalty = self.__calcul_g3(x)
        if g3_penalty > 0:
            penalty += g3_penalty * 20
        g4_penalty = self.__calcul_g4(x)
        if g4_penalty > 0:
            penalty += g4_penalty * 20

        cost = x[0]**2 * x[1] + (2 + x[2])
        return cost + penalty
