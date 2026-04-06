import numpy as np
from spring_design import SpringDesign
from helper import Helper


class AntColonyOptimization:

    def __init__(
        self,
        iterations,
        number_ants,
        evaporation,
        factor,
        delta_limit,
        stall_limit,
        pheromone_init,
        pheromone_increase_factor,
        top_pheromones
    ):
        self.spring_design = SpringDesign()
        self.iterations = iterations
        self.number_ants = number_ants
        self.evaporation = evaporation
        self.factor = factor
        self.bounds = self.spring_design.bounds
        self.dimension = len(self.bounds)
        self.delta_limit = delta_limit
        self.stall_limit = stall_limit
        self.pheromone_init = pheromone_init
        self.pheromone_increase_factor = pheromone_increase_factor
        self.top_pheromones = top_pheromones
        self.pheromones = np.ones((self.dimension, 2)) * self.pheromone_init

    def generate_solution(self):
        solution = []
        for i in range(self.dimension):
            low, high = self.bounds[i]
            pheromone_min, pheromone_max = self.pheromones[i]
            mean = (pheromone_min + pheromone_max) / 2
            sigma = self.factor * (high - low)
            value = np.random.normal(mean, sigma)
            value = np.clip(value, low, high)
            solution.append(float(value))
        return solution

    def update_pheromones(self, archive):
        self.pheromones *= (1 - self.evaporation)
        top_pheromones_solutions = min(self.top_pheromones, len(archive))
        for i in range(self.dimension):
            best_values = [sol[i] for sol in archive[:top_pheromones_solutions]]
            mean_best = np.mean(best_values)
            self.pheromones[i, 0] += mean_best * self.pheromone_increase_factor
            self.pheromones[i, 1] += mean_best * self.pheromone_increase_factor
        self.pheromones = np.clip(self.pheromones, 1e-6, 1e6)

    def optimize(self):
        archive = [self.generate_solution() for _ in range(self.number_ants)]
        archive_cost = [self.spring_design.calcul_spring(x) for x in archive]

        best_solution = archive[np.argmin(archive_cost)]
        best_cost = min(archive_cost)
        stall_counter = 0

        for iteration in range(self.iterations):
            previous_best = best_cost
            new_archive = []

            for _ in range(self.number_ants):
                index = np.random.randint(0, len(archive))
                base = archive[index]
                temp_solution = []

                for i in range(self.dimension):
                    sigma = self.factor * (self.bounds[i][1] - self.bounds[i][0])
                    value = np.random.normal(base[i], sigma)
                    value = np.clip(value, self.bounds[i][0], self.bounds[i][1])
                    temp_solution.append(float(value))

                cost = self.spring_design.calcul_spring(temp_solution)
                if self.spring_design.is_valid(temp_solution):
                    Helper.save_to_csv("ac_iteration", iteration, temp_solution, cost)
                    new_archive.append(temp_solution)

            archive.extend(new_archive)
            archive_cost.extend([self.spring_design.calcul_spring(x) for x in new_archive])
            sorted_index = np.argsort(archive_cost)
            archive = [archive[i] for i in sorted_index[:self.number_ants]]
            archive_cost = [archive_cost[i] for i in sorted_index[:self.number_ants]]

            if archive_cost[0] < best_cost:
                best_cost = archive_cost[0]
                best_solution = archive[0]

            self.update_pheromones(archive)
            if previous_best - best_cost < self.delta_limit:
                stall_counter += 1
            else:
                stall_counter = 0
            if stall_counter >= self.stall_limit:
                # print(f"Critère d'arrêt : Ant Colony Optimization à l'itération {iteration}")
                break

        return best_solution, best_cost