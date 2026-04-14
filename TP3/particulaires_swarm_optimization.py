import numpy as np
from helper import Helper
from spring_design import SpringDesign


class Particle:
    def __init__(self, dim, bounds):
        self.position = np.array([
            np.random.uniform(low, high) 
            for (low, high) in bounds
        ])

        self.velocity = np.zeros(dim)
        self.best_position = self.position.copy()
        self.best_cost = np.inf


class ParticulairesSwarmOptimization:

    def __init__(
        self,
        iterations,
        num_particles,
        inertia_weight,
        cognitive_weight,
        social_weight,
        neighborhood_size,
        delta_limit,
        stall_limit
    ):

        self.spring_design = SpringDesign()
        self.iterations = iterations
        self.bounds = self.spring_design.bounds
        self.num_particles = num_particles
        self.dimension = len(self.bounds)
        self.w = inertia_weight
        self.c1 = cognitive_weight
        self.c2 = social_weight
        self.neighborhood_size = neighborhood_size
        self.delta_limit = delta_limit
        self.stall_limit = stall_limit


    def get_neighborhood_best(self, swarm, index):
        ring_neighbors = []
        for i in range(-self.neighborhood_size, self.neighborhood_size + 1):
            idx = (index + i) % self.num_particles
            ring_neighbors.append(swarm[idx])

        best = min(ring_neighbors, key=lambda p: p.best_cost)
        return best.best_position


    def optimize(self):

        swarm = [
            Particle(self.dimension, self.bounds)
            for _ in range(self.num_particles)
        ]
        global_best_pos = None
        global_best_cost = float("inf")
        stall_counter = 0

        for p in swarm:
            cost = self.spring_design.calcul_spring(p.position)
            p.best_cost = cost
            p.best_position = p.position.copy()
            if cost < global_best_cost:
                global_best_cost = cost
                global_best_pos = p.position.copy()

        for iteration in range(self.iterations):
            previous_best = global_best_cost
            for i, p in enumerate(swarm):
                neighborhood_best = self.get_neighborhood_best(swarm, i)
                r1 = np.random.rand(self.dimension)
                r2 = np.random.rand(self.dimension)
                cognitive = self.c1 * r1 * (p.best_position - p.position)
                social = self.c2 * r2 * (neighborhood_best - p.position)
                p.velocity = self.w * p.velocity + cognitive + social
                p.position = p.position + p.velocity

                for d in range(self.dimension):
                    low, high = self.bounds[d]
                    if p.position[d] < low:
                        p.position[d] = low
                        p.velocity[d] *= -0.5
                    elif p.position[d] > high:
                        p.position[d] = high
                        p.velocity[d] *= -0.5

                cost = self.spring_design.calcul_spring(p.position)
                if self.spring_design.is_valid(p.position):
                    Helper.save_to_csv("pso_iteration", iteration, p.position, cost)
                    if cost < p.best_cost:
                        p.best_cost = cost
                        p.best_position = p.position.copy()
                    if cost < global_best_cost:
                        global_best_cost = cost
                        global_best_pos = p.position.copy()

            if previous_best - global_best_cost < self.delta_limit and self.spring_design.is_valid(global_best_pos):
                stall_counter += 1
            else:
                stall_counter = 0
            if stall_counter >= self.stall_limit:
                # print(f"Critère d'arrêt : Particulaire Swarm Optimization {iteration}")
                break

        return global_best_pos, global_best_cost
