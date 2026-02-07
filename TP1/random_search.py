from spring_design import SpringDesign
from hill_climbing import HillClimbing
from simulated_annealing import SimulatedAnnealing


class RandomSearch:

    def __init__(self):
        self.spring_design = SpringDesign()
        self.best_solution = None
        self.best_cost = float('inf')

    def evaluate(self, montecarlo_iteration, heuristique_value, stagnation_value, stagnation_iteration):

        if heuristique_value == 1:
            delta = float(input("Entrez le delta du voisinage: (0.25 par exemple) ").strip().replace(',', '.'))
            neighborhood_number = 1
            heuristique = HillClimbing( delta = delta, 
                                        max_iterations = montecarlo_iteration, 
                                        neighborhood_size = neighborhood_number,
                                        stagnation_value = stagnation_value,
                                        stagnation_iteration = stagnation_iteration)
        elif heuristique_value == 2:
            delta = float(input("Entrez le delta du voisinage: (0.25 par exemple) ").strip().replace(',', '.'))
            neighborhood_number = int(input("Entrez le nombre voisin (5 par exemple) "))
            heuristique = HillClimbing( delta = delta, 
                                        max_iterations = montecarlo_iteration, 
                                        neighborhood_size = neighborhood_number, 
                                        stagnation_value = stagnation_value,
                                        stagnation_iteration = stagnation_iteration)
        elif heuristique_value == 3:
            temperature = 100.0
            cooling_rate = float(input("Entrez le taux de refroidissement (0.99 par exemple) "))
            heuristique = SimulatedAnnealing( delta = delta,
                                            max_iterations = montecarlo_iteration,
                                            stagnation_value = stagnation_value,
                                            stagnation_iteration = stagnation_iteration,
                                            temperature = temperature,
                                            cooling_rate = cooling_rate,)
        else:
            raise ValueError("Error: Heuristique non reconnue")

        best_solution, best_cost = heuristique.optimize()
        return best_solution, best_cost

