import math
import numpy as np
from spring_design import SpringDesign


class SimulatedAnnealing:

    def __init__(self, max_iterations, stagnation_value,
                    stagnation_iteration, temperature, cooling_rate):

        self.spring_design = SpringDesign()
        self.max_iterations = max_iterations
        self.stagnation_value = stagnation_value
        self.stagnation_iteration = stagnation_iteration
        self.temperature = temperature
        self.cooling_rate = cooling_rate

    def optimize(self):

        current_solution = self.spring_design.generate_valid_random_solution()
        current_cost = self.spring_design.calcul_spring(current_solution)

        best_solution = current_solution.copy()
        best_cost = current_cost

        temperature = self.temperature
        stagnation_counter = 0

        for iteration in range(self.max_iterations):

            new_solution = current_solution + np.random.normal(0, size=len(current_solution))

            for i, (low, high) in enumerate(self.spring_design.bounds):
                new_solution[i] = np.clip(new_solution[i], low, high)

            if not self.spring_design.is_valid(new_solution):
                continue

            new_cost = self.spring_design.calcul_spring(new_solution)

            delta_cost = new_cost - current_cost

            if delta_cost < 0:
                accept = True
            else:
                prob = math.exp(-delta_cost / temperature)
                accept = np.random.rand() < prob

            if accept:
                current_solution = new_solution
                current_cost = new_cost

                if current_cost < best_cost:
                    best_solution = current_solution.copy()
                    best_cost = current_cost
                    print(f"Nouvelle meilleur solution: {current_solution} avec le coût: {current_cost}")
                    stagnation_counter = 0
                else:
                    stagnation_counter += 1
            else:
                stagnation_counter += 1

            temperature *= self.cooling_rate

            if stagnation_counter >= self.stagnation_iteration:
                print("Stagnation détectée")
                break

        return best_solution, best_cost
