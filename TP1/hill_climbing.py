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
        current = self.spring_design.generate_random_solution()
        current_cost = self.spring_design.calcul_spring(current)
        variation = self.pourcentage_variation

        best_solution = current.copy()
        best_cost = current_cost
        stagnation_counter = 0

        for iteration in range(self.max_iterations):

            neighbors = self.__generate_neighbors(current, variation)

            tmp_neighbor = None
            tmp_cost = float('inf')

            for neighbor in neighbors:
                cost = self.spring_design.calcul_spring(neighbor)
                if not self.spring_design.is_valid(neighbor):
                    if cost > 100:
                        if variation >= 0.05:
                            variation *= 0.95
                    continue

                if cost < tmp_cost:
                    tmp_cost = cost
                    tmp_neighbor = neighbor

            if tmp_neighbor is not None and tmp_cost < current_cost:
                current = tmp_neighbor.copy()
                current_cost = tmp_cost

                if current_cost < best_cost:
                    best_solution = current.copy()
                    best_cost = current_cost
                    print("New best:", best_cost)

                stagnation_counter = 0
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.stagnation_iteration:
                print("Stagnation détectée")
                break

        return best_solution, best_cost


    def __generate_neighbors(self, solution, variation):
            neighbors = []
            for _ in range(self.neighborhood_size):
                tmp_solution = solution.copy()
                for i in range(len(solution)):
                    lower, upper = self.spring_design.bounds[i]
                    variation = np.random.uniform(-variation * (upper - lower), 
                                                variation * (upper - lower))
                    value = tmp_solution[i] + variation
                    value = max(lower, min(value, upper))
                    tmp_solution[i] = value

                neighbors.append(tmp_solution)
            return neighbors