import random
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
            neighbors = self.__generate_neighbors(best_solution, self.neighborhood_size)

            temp_neighbor = None
            temp_cost = float('inf')

            for neighbor in neighbors:
                if not self.spring_design.is_valid(neighbor):
                    continue

                cost = self.spring_design.calcul_spring(neighbor)
                # Keep for report
                # if self.neighborhood_size == 1:
                #     Helper.save_to_csv('hill_climbing', iteration, neighbor, cost)
                # else:
                #     Helper.save_to_csv('generalized_hill_climbing', iteration, neighbor, cost)

                if cost < temp_cost:
                    temp_cost = cost
                    temp_neighbor = neighbor

            if temp_neighbor is not None and temp_cost < best_cost:
                best_solution = temp_neighbor.copy()
                best_cost = temp_cost
                stagnation_counter = 0
                print(f"Nouvelle meilleure solution: {best_solution} coût: {best_cost}")
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.stagnation_iteration:
                print("Stagnation détectée")
                break

        return best_solution, best_cost

    # Keep for report
    # def __generate_neighbors(self, solution, neighborhood_size):
    #     neighbors = []
    #     for _ in range(neighborhood_size):
    #         for i in range(len(solution)):
    #             up_solution = solution.copy()
    #             up_solution[i] += self.step
    #             neighbors.append(up_solution)
    #             down_solution = solution.copy()
    #             down_solution[i] -= self.step
    #             neighbors.append(down_solution)

    #     return neighbors

    def __generate_neighbors(self, solution, neighborhood_size):
            neighbors = []
            for _ in range(neighborhood_size):
                tmp_solution = solution.copy()
                for i in range(len(solution)):
                    lower_bound, upper_bound = self.spring_design.bounds[i]
                    variation = random.uniform(-self.pourcentage_variation * (upper_bound - lower_bound), 
                                                self.pourcentage_variation * (upper_bound - lower_bound))
                    new_value = tmp_solution[i] + variation
                    new_value = max(lower_bound, min(new_value, upper_bound))
                    tmp_solution[i] = new_value

                neighbors.append(tmp_solution)
            return neighbors