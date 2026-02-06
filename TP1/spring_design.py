# 1.2. Problème d’optimisation


class SpringDesign:

    def __init__(self):
        self.bounds = [ (0.05, 2.00), # Bornes x[0] = diamètre du fil
                        (0.25, 1.30), # Bornes x[1] = diamètre de la spirale
                        (2.00, 15.0)] # Bornes x[2] = nombre de spirales

        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
        self.constraints = [
            {'type': 'ineq', 'fun': self.__constraint_g1},
            {'type': 'ineq', 'fun': self.__constraint_g2},
            {'type': 'ineq', 'fun': self.__constraint_g3},
            {'type': 'ineq', 'fun': self.__constraint_g4},
        ]

    def calcul_spring(self, x):
        safe_x = self.__validate_and_adjust_bounds(x)
        result = safe_x[0]**2 * safe_x[1] + (2 + safe_x[2])
        return safe_x, result

    def __constraint_g1(self, x):
        return (1 - (x[1]**3 * x[2]) / (71785 * x[0]**4)) <= 0

    def __constraint_g2(self, x):
        return ((4 * x[1]**2 - x[0] * x[1]) / (12566 * (x[1] * x[0]**3 - x[0]**4))) + (1 / (5108 * x[0]**2)) - 1 <= 0

    def __constraint_g3(self, x):
        return 1 - (140.45 * x[0]) / (x[1]**2 * x[2]) <= 0

    def __constraint_g4(self, x):
        return ((x[0] + x[1]) / 1.5) - 1 <= 0
    
    def __validate_and_adjust_bounds(self, x):
        safe_bounds = x.copy()
        for i in range(len(safe_bounds)):
            if safe_bounds[i] < self.bounds[i][0]:
                safe_bounds[i] = self.bounds[i][0]
            elif safe_bounds[i] > self.bounds[i][1]:
                safe_bounds[i] = self.bounds[i][1]
                
        return safe_bounds
