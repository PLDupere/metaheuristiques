

class HillClimbing:

    def __init__(self, spring_design, delta=0.1, max_iterations=50):
        self.spring_design = spring_design
        self.delta = delta
        self.max_iterations = max_iterations

    def optimize(self, initial_solution):
        current_solution = initial_solution
        current_cost = float('inf')

        for _ in range(self.max_iterations):
            neighbors = self.__generate_neighbors(current_solution)
            best_neighbor = None
            best_cost = float('inf')

            # TODO: Validate 
            # for neighbor in neighbors:
            #     cost = self.spring_design.penalized_function(neighbor)
            #     if cost < best_cost:
            #         best_cost = cost
            #         best_neighbor = neighbor

            if best_cost < current_cost:
                current_solution = best_neighbor
                current_cost = best_cost

        # for _ in range(self.max_iterations):
        #     initial_solution = self.generate_random_solution()
        #     cost = self.spring_design.spring_function(initial_solution)

        #     print(f"Solution: {solution}, Cost: {cost}")

        #     if cost < self.best_cost:
        #         self.best_cost = cost
        #         self.best_solution = solution

        # return self.best_solution, self.best_cost

        return current_solution, current_cost

    def __generate_neighbors(self, solution):
        neighbors = []
        for i in range(len(solution)):
            up = solution.copy()
            down = solution.copy()
            up[i] += self.delta
            down[i] -= self.delta
            neighbors.append(up)
            neighbors.append(down)

        return neighbors
