import numpy as np
from spring_design import SpringDesign

class Particle:
    def __init__(self, dim, bounds):
        self.dim = dim
        self.bounds = bounds
        self.position = np.array([np.random.uniform(low, high) for (low, high) in bounds])
        self.velocity = np.array([np.random.uniform(-(high - low), (high - low)) * 0.1 for (low, high) in bounds])
        self.particle_best_pos = self.position.copy()
        self.particle_best_cost = np.inf

class ParticulairesSwarmOptimization:

    def __init__(self, iterations=200, num_particles=40, inertia_weight=0.7, cognitive_weight=1.4, social_weight=1.4):
        self.spring_design = SpringDesign()
        self.iterations = iterations
        self.bounds = self.spring_design.bounds
        self.num_particles = num_particles
        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight
        self.dimension = len(self.bounds)  

    def optimize(self, inertia_weight=0.8, cognitive_weight=1.5, social_weight=1.5):
        swarm = [Particle(self.dimension, self.bounds) for _ in range(self.num_particles)]
        global_best_pos = None
        global_best_cost = float('inf')
        for p in swarm:
            cost = self.spring_design.calcul_spring(p.position)
            p.particle_best_cost = cost
            p.particle_best_pos = p.position.copy()
            if cost < global_best_cost:
                global_best_cost = cost
                global_best_pos = p.position.copy()

        for iteration in range(self.iterations):
            for p in swarm:
                rand1 = np.random.rand(self.dimension)
                rand2 = np.random.rand(self.dimension)

                cognitive = cognitive_weight * rand1 * (p.particle_best_pos - p.position)
                social = social_weight * rand2 * (global_best_pos - p.position)
                p.velocity = inertia_weight * p.velocity + cognitive + social
                p.position = p.position + p.velocity

                for i in range(self.dimension):
                    low, high = self.bounds[i]
                    if p.position[i] < low:
                        p.position[i] = low
                        p.velocity[i] = 0.0
                    elif p.position[i] > high:
                        p.position[i] = high
                        p.velocity[i] = 0.0

                cost = self.spring_design.calcul_spring(p.position)

                if cost < p.particle_best_cost:
                    p.particle_best_cost = cost
                    p.particle_best_pos = p.position.copy()

                if cost < global_best_cost:
                    global_best_cost = cost
                    global_best_pos = p.position.copy()

        return global_best_pos, global_best_cost