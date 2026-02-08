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
            neighborhood_size = 1
            #TODO: RANDOM RESTART ??
            # random_restart = bool(self._get_boolean_input("Do you want to restart the process? (yes or no / y or n): "))
            heuristique = HillClimbing( delta = delta, 
                                        max_iterations = montecarlo_iteration, 
                                        neighborhood_size = neighborhood_size,
                                        stagnation_value = stagnation_value,
                                        stagnation_iteration = stagnation_iteration)
        elif heuristique_value == 2:
            delta = float(input("Entrez le pas avec le voisinage: (0.25 par exemple) ").strip().replace(',', '.'))
            neighborhood_size = int(input("Entrez le nombre voisin (5 par exemple) "))
            heuristique = HillClimbing( delta = delta, 
                                        max_iterations = montecarlo_iteration, 
                                        neighborhood_size = neighborhood_size, 
                                        stagnation_value = stagnation_value,
                                        stagnation_iteration = stagnation_iteration)
        elif heuristique_value == 3:
            temperature = 100.0
            cooling_rate = float(input("Entrez le taux de refroidissement (0.99 par exemple) "))
            step_size = float(input("Entrez le pas de déplacement (0.25 par exemple) "))
            cooling_type = self.__get_cooling_type()
            adaptive_factor = float(input("Entrez le facteur d'adaptation pour la remontée de température (1.1 par exemple) "))
            heuristique = SimulatedAnnealing(max_iterations = montecarlo_iteration,
                                            stagnation_value = stagnation_value,
                                            stagnation_iteration = stagnation_iteration,
                                            temperature = temperature,
                                            cooling_rate = cooling_rate,
                                            step_size = step_size,
                                            cooling_type = cooling_type,
                                            adaptive_factor=adaptive_factor)
        else:
            raise ValueError("Error: Heuristique non reconnue")

        best_solution, best_cost = heuristique.optimize()
        return best_solution, best_cost
    
    def __get_cooling_type(self):
        while True:
            cooling_type = input("Entrez le type de refroidissement ( 1: exponential, 2: linear, 3: logarithmic): ").strip().lower()
            if cooling_type == '1':
                return 'exponential'
            elif cooling_type == '2':
                return 'linear'
            elif cooling_type == '3':
                return 'logarithmic'
            else:
                print("Invalid input. Please enter 1, 2 or 3.")

    def _get_boolean_input(text):
        while True:
            user_input = input(text).strip().lower()
            if user_input in ['yes', 'y']:
                return True
            elif user_input in ['no', 'n']:
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")