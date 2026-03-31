import math
import numpy as np
from helper import Helper
from spring_design import SpringDesign


class SimulatedAnnealing:

    def __init__(self, max_iterations, stagnation_value, stagnation_iteration, temperature,
                    cooling_rate, cooling_type, adaptive_factor):

        self.spring_design = SpringDesign()
        self.max_iterations = max_iterations
        self.stagnation_value = stagnation_value
        self.stagnation_iteration = stagnation_iteration
        self.initial_temperature = temperature
        self.cooling_rate = cooling_rate
        self.cooling_type = cooling_type
        self.adaptive_factor = adaptive_factor


    def optimize(self):
        temperature = self.initial_temperature
        current_solution = np.array(self.spring_design.generate_random_solution())
        current_cost = self.__cost(current_solution)
        best_solution = None
        best_cost = float('inf')
        stagnation_counter = 0

        for iteration in range(self.max_iterations):
            tmp_solution = current_solution.copy()
            for idx in range(len(tmp_solution)):
                lower, upper = self.spring_design.bounds[idx]

                variation = np.random.uniform(
                   -temperature * (upper - lower),
                   temperature * (upper - lower)
                )

                value = tmp_solution[idx] + variation
                value = max(lower, min(value, upper))
                tmp_solution[idx] = value

            tmp_cost = self.__cost(tmp_solution)
            delta = tmp_cost - current_cost

            if delta < 0 or np.random.rand() < math.exp(-delta / temperature):
                current_solution = tmp_solution
                current_cost = tmp_cost

            if  self.spring_design.is_valid(current_solution):
                if current_cost < best_cost:
                    best_solution = current_solution.copy()
                    best_cost = current_cost
                    stagnation_counter = 0
                    Helper.save_to_csv("simulated_annealing_results", iteration, best_solution, best_cost)
                    print(f"Nouvelle meilleure: {best_solution} coût={best_cost:.12f}")

            if abs(delta) > self.stagnation_value:
                stagnation_counter += 1
            if stagnation_counter >= self.stagnation_iteration:
                temperature = self.adaptive_factor
                stagnation_counter = 0
                print(f"Réchauffement → T = {temperature:.12f}")

            temperature = self.__cooling_strategy(iteration, temperature)
        return best_solution, best_cost


    def __cooling_strategy(self, iteration, temperature):
        if self.cooling_type == "exponential":
            temperature *= self.cooling_rate
        elif self.cooling_type == "linear":
            temperature = self.initial_temperature * (1 - iteration / self.max_iterations)
        elif self.cooling_type == "logarithmic":
            temperature = self.initial_temperature / (1 + math.log(iteration + 1))
        #Safety
        if temperature < 1e-12:
            temperature = 1e-12

        return temperature


    def __cost(self, x):
        c = self.spring_design.calcul_spring(x)
        if isinstance(c, (list, tuple, np.ndarray)):
            return float(c[0])
        return float(c)
