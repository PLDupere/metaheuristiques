from helper import Helper
from random_search import RandomSearch
from hill_climbing import HillClimbing
from simulated_annealing import SimulatedAnnealing


if __name__ == "__main__":
    print("Métaheuristique pour l'optimisation de ressorts")
    print("Les paramètres suivants seront utilisés pour les trois algorithmes (Random Search, Hill Climbing et Simulated Annealing)")
    montecarlo_iteration = Helper.get_integer_input("Spécifier  le  nombre  de simulations de Monte-Carlo : (10000 par exemple) ")
    print("Random Search")
    iterations = Helper.get_integer_input("Définit le nombre d'itérations : (100 par exemple) ")
    print("Hill Climbing")
    pourcentage_variation = Helper.get_value_between_0_and_1("Entrez le pourcentage de variation (0.25 par exemple) : ")
    neighborhood_size = Helper.get_integer_input("Entrez le nombre voisin (5 par exemple) ")
    stagnation_value = Helper.get_float_input("Définit la valeur de stagnation : (0.001 par exemple) ")
    stagnation_iteration = Helper.get_integer_input("Définit le nombre d'itérations de stagnation : (50 par exemple) ")
    print("Recuit simulé (Simulated Annealing)")
    temperature = 1.0
    cooling_rate = Helper.get_value_between_0_and_1("Entrez le taux de refroidissement (0.99 par exemple) ")
    cooling_type = Helper().get_cooling_type()
    adaptive_factor = Helper.get_value_between_0_and_1("Entrez le facteur d'adaptation pour la remontée de température : (0.15 par exemple) ")


    best_random_solution = None
    best_random_cost = float('inf')
    best_climbing_hill_solution = None
    best_climbing_hill_cost = float('inf')
    best_generalized_hill_climbing_solution = None
    best_generalized_hill_climbing_cost = float('inf')
    best_simulated_annealing_solution = None
    best_simulated_annealing_cost = float('inf')

    random_Search = RandomSearch(iterations)
    hill_climbing = HillClimbing(pourcentage_variation, iterations, neighborhood_size, stagnation_value, stagnation_iteration)
    simulated_annealing = SimulatedAnnealing(iterations, stagnation_value, stagnation_iteration, temperature, 
                                                cooling_rate, cooling_type, adaptive_factor)

    for iteration in range(montecarlo_iteration):
        random_Search_solution, random_Search_cost = random_Search.optimize()
        Helper.save_to_csv(f'random_search_{montecarlo_iteration}', iteration, random_Search_solution, random_Search_cost)
        if random_Search_cost < best_random_cost:
            best_random_solution = random_Search_solution.copy()
            best_random_cost = random_Search_cost

        hill_climbing_solution, hill_climbing_cost = hill_climbing.optimize()
        Helper.save_to_csv(f'hill_climbing_{montecarlo_iteration}', iteration, hill_climbing_solution, hill_climbing_cost)
        if hill_climbing_cost < best_climbing_hill_cost:
            best_climbing_hill_solution = hill_climbing_solution.copy()
            best_climbing_hill_cost = hill_climbing_cost

        simulated_annealing_solution, simulated_annealing_cost = simulated_annealing.optimize()
        Helper.save_to_csv(f'simulated_annealing_{montecarlo_iteration}', iteration, simulated_annealing_solution, simulated_annealing_cost)
        if simulated_annealing_cost < best_simulated_annealing_cost:
            best_simulated_annealing_solution = simulated_annealing_solution.copy()
            best_simulated_annealing_cost = simulated_annealing_cost

    Helper().plot_solution(best_random_solution, best_climbing_hill_solution, best_simulated_annealing_solution)

    print("Meilleure solution Random Search: ", best_random_solution, "Coût: ", best_random_cost)
    print("Meilleure solution Hill Climbing: ", best_climbing_hill_solution, "Coût: ", best_climbing_hill_cost)
    print("Meilleure solution Simulated Annealing: ", best_simulated_annealing_solution, "Coût: ", best_simulated_annealing_cost)
