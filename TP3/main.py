from helper import Helper
from differential_evolution import DifferentialEvolution
from particulaires_swarm_optimization import ParticulairesSwarmOptimization
from ant_colony_optimization import AntColonyOptimization


if __name__ == "__main__":
    print("Métaheuristique pour l'optimisation de ressorts")
    print("Les paramètres suivants seront utilisés pour les trois algorithmes (Particule Swarm Optimization, Differential Evolution et Ant Colony Optimization) :")
    montecarlo_iteration = Helper.get_integer_input("Spécifier  le  nombre  de simulations de Monte-Carlo : (100 par exemple) ")
    iterations = Helper.get_integer_input("Spécifier  le  nombre  d'itérations : (100 par exemple) ")


    best_pso_solution = None
    best_pso_cost = float('inf')
    best_differential_evolution_solution = None
    best_differential_evolution_cost = float('inf')
    best_ant_colony_solution = None
    best_ant_colony_cost = float('inf')

    de = DifferentialEvolution(iterations)
    pso = ParticulairesSwarmOptimization(iterations)
    ac = AntColonyOptimization(iterations)

    for i in range(montecarlo_iteration):
        pso_solution, pso_cost = pso.optimize()
        Helper.save_to_csv(f'pso_{montecarlo_iteration}', i, pso_solution, pso_cost)
        if pso_cost < best_pso_cost:
            best_pso_solution = pso_solution.copy()
            best_pso_cost = pso_cost

        # de_solution, de_cost = de.optimize()
        # Helper.save_to_csv(f'de_{montecarlo_iteration}', i, de_solution, de_cost)
        # if de_cost < best_differential_evolution_cost:
        #     best_differential_evolution_solution = de_solution.copy()
        #     best_differential_evolution_cost = de_cost

        # ac_solution, ac_cost = ac.optimize()
        # Helper.save_to_csv(f'ac_{montecarlo_iteration}', i, ac_solution, ac_cost)
        # if ac_cost < best_ant_colony_cost:
        #     best_ant_colony_solution = ac_solution.copy()
        #     best_ant_colony_cost = ac_cost

    # Helper().plot_solution(best_pso_solution, best_differential_evolution_solution, best_ant_colony_solution)

    # print("Meilleure solution Random Search: ", best_pso_solution, "Coût: ", best_pso_cost)
    # print("Meilleure solution Hill Climbing: ", best_differential_evolution_solution, "Coût: ", best_differential_evolution_cost)
    # print("Meilleure solution Simulated Annealing: ", best_ant_colony_solution, "Coût: ", best_ant_colony_cost)
