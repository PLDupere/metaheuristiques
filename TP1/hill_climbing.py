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
        current_solution = self.spring_design.generate_valid_random_solution()
        current_cost = float('inf')
        stagnation_counter = 0

        for _ in range(self.max_iterations):
            neighbors = self.__generate_neighbors(current_solution, self.neighborhood_size)
            best_neighbor = None
            best_cost = float('inf')

            for neighbor in neighbors:
                cost = self.spring_design.calcul_spring(neighbor)

                if cost < best_cost:
                    best_cost = cost
                    best_neighbor = neighbor

            if best_cost < current_cost:
                current_solution = best_neighbor
                current_cost = best_cost
                stagnation_counter = 0
                print(f"Nouvelle meilleur solution: {current_solution} avec le coût: {current_cost}")
            else:
                stagnation_counter += 1
                if stagnation_counter >= self.stagnation_iteration:
                    print("Stagnation détectée")
                    break
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

    #TODO: Ajouter pénalité
    def __apply_penalty(self, solution, neighborhood_size):
            pass