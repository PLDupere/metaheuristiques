import numpy as np
from spring_design import SpringDesign


class DifferentialEvolution:
    def __init__(self, iterations=100, pop_size=20, mutation_factor=0.5, crossover_rate=0.7):
        self.spring_design = SpringDesign()
        self.max_iter = iterations
        self.bounds = np.array(self.spring_design.bounds)
        self.pop_size = pop_size
        self.mutation_factor = mutation_factor
        self.crossover_rate = crossover_rate
        self.dimension = len(self.spring_design.bounds)

    def initialize(self):
        low = self.bounds[:, 0]
        high = self.bounds[:, 1]
        self.population = low + (high - low) * np.random.rand(self.pop_size, self.dimension)

    def mutate(self, i):
        indexes = [index for index in range(self.pop_size) if index != i]
        a, b, c = self.population[np.random.choice(indexes, 3, replace=False)]
        mutant = a + self.mutation_factor * (b - c)
        return np.clip(mutant, self.bounds[:,0], self.bounds[:,1])

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
        global_best_pos = None
        global_best_cost = float('inf')

        for _ in range(self.max_iter):
            new_pop = []
            for i in range(self.pop_size):
                target = self.population[i]
                mutant = self.mutate(i)
                trial = self.crossover(target, mutant)
                new = self.select(target, trial)
                new_pop.append(new)

            self.population = np.array(new_pop)

        fitness = np.array([self.spring_design.calcul_spring(index) for index in self.population])
        best_idx = np.argmin(fitness)
        global_best_pos = self.population[best_idx]
        global_best_cost = fitness[best_idx]

        return global_best_pos, global_best_cost