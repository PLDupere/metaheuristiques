import numpy as np
import random

from helper import Helper


class AntColonyOptimization:

    def __init__(
        self,
        graph,
        iterations=100,
        number_ants=20,
        alpha=1.0,
        beta=2.0,
        evaporation=0.5,
        pheromone_init=1.0,
        elitism_weight=2
    ):

        self.G = graph
        self.iterations = iterations
        self.number_ants = number_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.elitism_weight = elitism_weight
        self.start = 0
        self.n_nodes = len(self.G.nodes())

        for (u, v) in self.G.edges():
            self.G.edges[u, v]["tau"] = pheromone_init

    def __heuristic(self, u, v):
        return 1.0 / self.G.edges[u, v]["cout"]


    def __choose_next_node(self, current, visited):
        neighbors = list(self.G.neighbors(current))
        neighbors = [n for n in neighbors if n not in visited]
        if not neighbors:
            return None

        probs = []
        for node in neighbors:
            tau = self.G.edges[current, node]["tau"]
            eta = self.__heuristic(current, node)
            probs.append((tau ** self.alpha) * (eta ** self.beta))

        probs = np.array(probs)
        if probs.sum() == 0:
            return random.choice(neighbors)

        probs = probs / probs.sum()
        return np.random.choice(neighbors, p=probs)


    def __generate_path(self):
        current = self.start
        visited = {current}
        path = [current]
        while len(visited) < self.n_nodes:
            nxt = self.__choose_next_node(current, visited)
            if nxt is None:
                return None
            path.append(nxt)
            visited.add(nxt)
            current = nxt
        return path


    def __path_cost(self, path):
        return sum(
            self.G.edges[path[i], path[i + 1]]["cout"]
            for i in range(len(path) - 1)
        )


    def __update_pheromones(self, paths, costs, best_path):
        for (u, v) in self.G.edges():
            self.G.edges[u, v]["tau"] *= (1 - self.evaporation)

        for path, cost in zip(paths, costs):
            if path is None:
                continue
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.G.edges[u, v]["tau"] += 1.0 / cost
        if self.elitism_weight > 0 and best_path is not None:
            best_cost = self.__path_cost(best_path)
            for i in range(len(best_path) - 1):
                u, v = best_path[i], best_path[i + 1]
                self.G.edges[u, v]["tau"] += self.elitism_weight * (1.0 / best_cost)

    def optimize(self):
        best_path = None
        best_cost = float("inf")
        for i in range(self.iterations):
            paths = []
            costs = []
            for _ in range(self.number_ants):
                path = self.__generate_path()
                if path is not None:
                    cost = self.__path_cost(path)
                    paths.append(path)
                    costs.append(cost)
                    if cost < best_cost:
                        best_cost = cost
                        best_path = path

            self.__update_pheromones(paths, costs, best_path)
            Helper.save_to_csv("ac_iteration", i, best_path, best_cost)

        return best_path, best_cost