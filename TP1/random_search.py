from helper import Helper
from spring_design import SpringDesign

class RandomSearch:

    def __init__(self, max_iterations):
        self.spring_design = SpringDesign()
        self.max_iterations = max_iterations

    def optimize(self):
        best_solution = None
        best_cost = float('inf')

        for iteration in range(self.max_iterations):
                solution = self.spring_design.generate_random_solution()
                if not self.spring_design.is_valid(solution):
                    continue

                cost = self.spring_design.calcul_spring(solution)
                # Helper.save_to_csv('random_search', iteration, solution, cost)

                if self.spring_design.is_valid(solution):
                    if cost < best_cost:
                        best_solution = solution.copy()
                        best_cost = cost
                        print(f"Nouvelle meilleure solution: {best_solution} coût: {best_cost}")

        return best_solution, best_cost
