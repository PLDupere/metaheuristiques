import math
import numpy as np
from spring_design import SpringDesign
from helper import Helper


class SimulatedAnnealing:

    def __init__(self, max_iterations, stagnation_value, stagnation_iteration, temperature,
                        cooling_rate, delta, cooling_type, adaptive_factor, neighborhood_size):
        self.spring_design = SpringDesign()
        self.max_iterations = max_iterations
        self.stagnation_value = stagnation_value
        self.stagnation_iteration = stagnation_iteration
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.delta = delta
        self.cooling_type = cooling_type
        self.adaptive_factor = adaptive_factor
        self.neighborhood_size = neighborhood_size

    def optimize(self):
        self.temperature = 100
        initial_temperature = self.temperature
        current_solution = np.array(self.spring_design.generate_valid_random_solution())
        current_cost = self.spring_design.calcul_spring(current_solution)
        best_solution = current_solution.copy()
        best_cost = current_cost
        stagnation_counter = 0

        for iteration in range(self.max_iterations):
            neighbors = self.__generate_neighbors(current_solution)
            new_solution = neighbors[np.random.randint(len(neighbors))]
            new_cost = self.spring_design.calcul_spring(new_solution)
            delta_cost = new_cost - current_cost


            if delta_cost < 0 or np.random.rand() < math.exp(-delta_cost / self.temperature):
                current_solution = new_solution
                current_cost = new_cost

            if current_cost < best_cost - self.stagnation_value:
                best_solution = current_solution.copy()
                best_cost = current_cost
                stagnation_counter = 0
                print(f"Nouvelle meilleure: {best_solution} coût={best_cost:.10f}")
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.stagnation_iteration:
                self.temperature *= (1 + self.adaptive_factor)
                print(f"Réchauffé = {self.temperature:.12f}")
                stagnation_counter = 0

            self.__cooling_strategy(iteration, initial_temperature)
        return best_solution, best_cost


    def __generate_neighbors(self, solution):

        neighbors = []

        for _ in range(self.neighborhood_size):
            neighbor = solution.copy()

            for i in range(len(solution)):
                step = np.random.normal(0, self.delta)
                neighbor[i] += step

            neighbor = np.array(neighbor)

            if self.spring_design.is_valid(neighbor):
                neighbors.append(neighbor)

        if len(neighbors) == 0:
            neighbors.append(solution.copy())

        return neighbors

    def __cooling_strategy(self, iteration, initial_temperature):

        if self.cooling_type == "exponential":
            self.temperature *= self.cooling_rate

        elif self.cooling_type == "linear":
            self.temperature -= self.cooling_rate

        elif self.cooling_type == "logarithmic":
            self.temperature = initial_temperature / math.log(iteration + 2)

        if self.temperature < 1e-12:
            self.temperature = 1e-12
