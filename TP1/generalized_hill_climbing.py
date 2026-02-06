from spring_design import SpringDesign


class GeneralizedHillClimbing:

    def __init__(self, delta, max_iterations, neighborhood_size):
            self.spring_design = SpringDesign()
            self.delta = delta
            self.max_iterations = max_iterations
            self.neighborhood_size = neighborhood_size

    def optimize(self, initial_solution):
        current_solution = initial_solution
        current_cost = float('inf')

        for _ in range(self.max_iterations):
            neighbors = self.__generate_neighbors(current_solution, self.neighborhood_size)
            best_neighbor = None
            best_cost = float('inf')

            for neighbor in neighbors:
                safe_neighbor, cost = self.spring_design.calcul_spring(neighbor)
                if cost < best_cost:
                    best_cost = cost
                    best_neighbor = safe_neighbor

            if best_cost < current_cost:
                current_solution = best_neighbor
                current_cost = best_cost
                print(f"Nouvelle meilleur solution: {current_solution} avec le coût: {current_cost}")

        return current_solution, current_cost

    def __generate_neighbors(self, solution, neighborhood_size):
        neighbors = []
        for _ in range(neighborhood_size):
            for i in range(len(solution)):
                up = solution.copy()
                down = solution.copy()
                up[i] += self.delta
                down[i] -= self.delta
                neighbors.append(up)
                neighbors.append(down)

        return neighbors