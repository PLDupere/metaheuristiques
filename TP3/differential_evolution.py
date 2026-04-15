import numpy as np
from spring_design import SpringDesign
from helper import Helper


class DifferentialEvolution:
    def __init__(self, iterations, pop_size, mutation_factor, crossover_rate, delta_limit, stall_limit):
        self.spring_design = SpringDesign()
        self.iterations = iterations
        self.bounds = np.array(self.spring_design.bounds)
        self.pop_size = pop_size
        self.mutation_factor = mutation_factor
        self.crossover_rate = crossover_rate
        self.dimension = len(self.spring_design.bounds)
        self.delta_limit = delta_limit
        self.stall_limit = stall_limit

    def initialize(self):
        low = self.bounds[:, 0]
        high = self.bounds[:, 1]
        self.population = low + (high - low) * np.random.rand(self.pop_size, self.dimension)

    def mutate(self, i):
        indexes = [index for index in range(self.pop_size) if index != i]
        a, b, c = self.population[np.random.choice(indexes, 3, replace=False)]
        mutant = a + self.mutation_factor * (b - c)
        return np.clip(mutant, self.bounds[:, 0], self.bounds[:, 1])

    def crossover(self, target, mutant):
        cross = np.random.rand(self.dimension) < self.crossover_rate
        if not np.any(cross):
            cross[np.random.randint(0, self.dimension)] = True
        trial = np.where(cross, mutant, target)
        return trial

    def select(self, target, trial):
        if self.spring_design.calcul_spring(trial) < self.spring_design.calcul_spring(target):
            return trial
        return target

    def optimize(self):
        self.initialize()
        stall_counter = 0
        cost = np.array([self.spring_design.calcul_spring(ind) for ind in self.population])
        best_index = np.argmin(cost)
        global_best_position = self.population[best_index].copy()
        global_best_cost = cost[best_index]

        for iteration in range(self.iterations):
            previous_best = global_best_cost
            new_pop = []

            for i in range(self.pop_size):
                target = self.population[i]
                mutant = self.mutate(i)
                trial = self.crossover(target, mutant)
                new_solution = self.select(target, trial)
                cost = self.spring_design.calcul_spring(new_solution)
                if self.spring_design.is_valid(new_solution):
                    Helper.save_to_csv("de_iteration", iteration, new_solution, cost)
                new_pop.append(new_solution)

            self.population = np.array(new_pop)
            cost = np.array([self.spring_design.calcul_spring(ind) for ind in self.population])
            best_index = np.argmin(cost)
            current_best_cost = cost[best_index]
            current_best_pos = self.population[best_index].copy()

            if current_best_cost < global_best_cost and self.spring_design.is_valid(current_best_pos):
                global_best_cost = current_best_cost
                global_best_position = current_best_pos
            if previous_best - global_best_cost < self.delta_limit:
                stall_counter += 1
            else:
                stall_counter = 0
            if stall_counter >= self.stall_limit:
                # print(f"Critère d'arrêt : differential evolution {iteration}")
                break
        Helper.save_to_csv("de_iteration", iteration, global_best_position, global_best_cost)
        return global_best_position, global_best_cost