import math
import numpy as np
from spring_design import SpringDesign
from historical_record import HistoricalRecord


class SimulatedAnnealing:

    def __init__(self, max_iterations, stagnation_value, stagnation_iteration, 
                    temperature, cooling_rate, step_size, cooling_type, adaptive_factor):

        self.spring_design = SpringDesign()
        self.max_iterations = max_iterations
        self.stagnation_value = stagnation_value
        self.stagnation_iteration = stagnation_iteration
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.step_size = step_size
        self.cooling_type = cooling_type
        self.adaptive_factor = adaptive_factor

    def optimize(self):
        initial_temperature = self.temperature
        current_solution = self.spring_design.generate_valid_random_solution()
        current_cost = self.spring_design.calcul_spring(current_solution)

        best_solution = current_solution.copy()
        best_cost = current_cost
        stagnation_counter = 0

        for iteration in range(self.max_iterations):

            step = np.random.normal(0, self.step_size, size=len(current_solution))
            new_solution = current_solution + step

            if not self.spring_design.is_valid(new_solution):
                self.__cooling_strategy(iteration, initial_temperature)
                continue

            new_cost = self.spring_design.calcul_spring(new_solution)
            HistoricalRecord.save_to_csv('simulated_annealing', iteration, new_solution, new_cost)
            delta_cost = new_cost - current_cost

            if delta_cost < 0 or np.random.rand() < np.exp(-delta_cost / self.temperature):
                current_solution = new_solution
                current_cost = new_cost

            if current_cost < best_cost:
                best_solution = current_solution.copy()
                best_cost = current_cost
                stagnation_counter = 0
                print(f"Nouveau meilleur: {best_solution} coût: {best_cost}")
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.stagnation_iteration:
                self.temperature += self.adaptive_factor * self.temperature
                print(f"Stagnation détectée, remontée de la température à {self.temperature:.12f}")
                stagnation_counter = 0

            self.__cooling_strategy(iteration, initial_temperature)

        return best_solution, best_cost

    def __cooling_strategy(self, iteration, initial_temperature):
            if self.cooling_type == "exponential":
                self.temperature *= self.cooling_rate

            elif self.cooling_type == "linear":
                self.temperature -= self.cooling_rate
                if self.temperature < 1e-8: # Avoid negative temperature
                    self.temperature = 1e-8

            elif self.cooling_type == "logarithmic":
                self.temperature = initial_temperature / math.log(iteration + 2)
