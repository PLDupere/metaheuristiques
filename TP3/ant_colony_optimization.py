import numpy as np
from spring_design import SpringDesign


class AntColonyOptimization:

    def __init__(self, iterations=100, number_ants=30, evaporation=0.8, factor=0.5):

        self.spring_design = SpringDesign()
        self.iterations = iterations
        self.number_ants = number_ants
        self.evaporation = evaporation
        self.factor = factor
        self.bounds = self.spring_design.bounds
        self.dimension = len(self.bounds)


    def generate_solution(self):
        return [
            np.random.uniform(self.bounds[i][0], self.bounds[i][1])
            for i in range(self.dimension)
        ]


    def optimize(self):

        archive = [self.generate_solution() for _ in range(self.number_ants)]
        archive_cost = [
            self.spring_design.calcul_spring(x)
            for x in archive
        ]

        best_solution = archive[np.argmin(archive_cost)]
        best_cost = min(archive_cost)

        for iteration in range(self.iterations):
            new_archive = []

            for _ in range(self.number_ants):
                idx = np.random.randint(0, len(archive))
                base = archive[idx]
                new_solution = []

                for i in range(self.dimension):
                    sigma = self.factor * (self.bounds[i][1] - self.bounds[i][0])
                    value = np.random.normal(base[i], sigma)
                    value = np.clip(value, self.bounds[i][0], self.bounds[i][1])
                    new_solution.append(value)
                new_archive.append(new_solution)

            new_cost = [
                self.spring_design.calcul_spring(x)
                for x in new_archive
            ]

            archive.extend(new_archive)
            archive_cost.extend(new_cost)
            sorted_index = np.argsort(archive_cost)
            archive = [archive[i] for i in sorted_index[:self.number_ants]]
            archive_cost = [archive_cost[i] for i in sorted_index[:self.number_ants]]

            if archive_cost[0] < best_cost:
                best_cost = archive_cost[0]
                best_solution = archive[0]

        best_solution = [float(x) for x in best_solution]
        best_cost = float(best_cost)
        return best_solution, best_cost