from spring_design import SpringDesign

class HillClimbing:

    def __init__(self, delta, max_iterations, neighborhood_size, stagnation_value, stagnation_iteration):
        self.spring_design = SpringDesign()
        self.delta = delta
        self.max_iterations = max_iterations
        self.neighborhood_size = neighborhood_size
        self.stagnation_value = stagnation_value
        self.stagnation_iteration = stagnation_iteration

    def optimize(self):
        best_solution = self.spring_design.generate_valid_random_solution()
        best_cost = self.spring_design.calcul_spring(best_solution)
        stagnation_counter = 0

        for _ in range(self.max_iterations):
            neighbors = self.__generate_neighbors(best_solution, self.neighborhood_size)

            temp_neighbor = None
            temp_cost = float('inf')

            for neighbor in neighbors:
                if not self.spring_design.is_valid(neighbor):
                    continue

                cost = self.spring_design.calcul_spring(neighbor)

                if cost < temp_cost:
                    temp_cost = cost
                    temp_neighbor = neighbor

            if temp_neighbor is not None and temp_cost < best_cost:
                best_solution = temp_neighbor.copy()
                best_cost = temp_cost
                stagnation_counter = 0
                print(f"Nouvelle meilleure solution: {best_solution} coût: {best_cost}")
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.stagnation_iteration:
                print("Stagnation détectée")
                break

        return best_solution, best_cost

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
