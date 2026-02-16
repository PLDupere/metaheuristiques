import numpy as np
from helper import Helper
from spring_design import SpringDesign

class HillClimbing:

    def __init__(self, pourcentage_variation, max_iterations, neighborhood_size, stagnation_value, stagnation_iteration):
        self.spring_design = SpringDesign()
        self.pourcentage_variation = pourcentage_variation
        self.max_iterations = max_iterations
        self.neighborhood_size = neighborhood_size
        self.stagnation_value = stagnation_value
        self.stagnation_iteration = stagnation_iteration


    def optimize(self):
        best_solution = self.spring_design.generate_valid_random_solution()
        best_cost = self.spring_design.calcul_spring(best_solution)
        stagnation_counter = 0

        for iteration in range(self.max_iterations):
            neighbors = self.__generate_neighbors(best_solution)
            tmp_neighbor = None
            tmp_cost = float('inf')

            for neighbor in neighbors:
                cost = self.spring_design.calcul_spring(neighbor)

            # Reduce by 5%
            if cost > 100:
                if self.pourcentage_variation >= 0.05:
                    self.pourcentage_variation *= 0.95

                if cost < tmp_cost:
                    tmp_cost = cost
                    tmp_neighbor = neighbor
            
            if  self.spring_design.is_valid(neighbor):
                if tmp_neighbor is not None and tmp_cost < best_cost:
                    best_solution = tmp_neighbor.copy()
                    best_cost = tmp_cost
                    stagnation_counter = 0
                    print(f"Nouvelle meilleure solution: {best_solution} coût: {best_cost}")
                else:
                    stagnation_counter += 1
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.stagnation_iteration:
                print("Stagnation détectée")
                break

        return best_solution, best_cost

    # Keep for report 
    # def __generate_neighbors(self, solution):
    #     neighbors = []
    #     for _ in range(self.neighborhood_size):
    #         for i in range(len(solution)):
    #             up_solution = solution.copy()
    #             up_solution[i] += self.step
    #             neighbors.append(up_solution)
    #             down_solution = solution.copy()
    #             down_solution[i] -= self.step
    #             neighbors.append(down_solution)

    #     return neighbors

    def __generate_neighbors(self, solution):
            neighbors = []
            for _ in range(self.neighborhood_size):
                tmp_solution = solution.copy()
                for i in range(len(solution)):
                    lower, upper = self.spring_design.bounds[i]
                    variation = np.random.uniform(-self.pourcentage_variation * (upper - lower), 
                                                self.pourcentage_variation * (upper - lower))
                    value = tmp_solution[i] + variation
                    value = max(lower, min(value, upper))
                    tmp_solution[i] = value

                neighbors.append(tmp_solution)
            return neighbors