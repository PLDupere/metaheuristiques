from helper import Helper
from differential_evolution import DifferentialEvolution
from particulaires_swarm_optimization import ParticulairesSwarmOptimization
from ant_colony_optimization import AntColonyOptimization
from simulated_annealing import SimulatedAnnealing
import time
import numpy as np
import networkx as nx


if __name__ == "__main__":
    print("Métaheuristique pour l'optimisation de ressorts")
    print("Les paramètres suivants seront utilisés pour les trois algorithmes (Particule Swarm Optimization, Differential Evolution et Ant Colony Optimization) :")
    montecarlo_iteration = Helper.get_integer_input("Spécifier  le  nombre  de simulations de Monte-Carlo : (50 par exemple) ")
    iterations = Helper.get_integer_input("Spécifier  le  nombre  d'itérations : (100 par exemple) ")
    stall_limit = Helper.get_integer_input("Spécifier  le  nombre  d'itérations de stagnation avant arrêt : (50 par exemple) ")
    delta_limit = Helper.get_float_input("Spécifier  le  delta_limit pour le critère de stagnation : (0.00001 par exemple) ")

    best_pso_solution = None
    best_pso_cost = float('inf')
    best_differential_evolution_solution = None
    best_differential_evolution_cost = float('inf')
    best_simulated_annealing_solution = None
    best_simulated_annealing_cost = float('inf')

    POP_SIZE = 5
    MUTATION_FACTOR = 0.5
    CROSSOVER_RATE = 0.7
    de = DifferentialEvolution(iterations=iterations,
                                pop_size=POP_SIZE,
                                mutation_factor=MUTATION_FACTOR,
                                crossover_rate=CROSSOVER_RATE,
                                delta_limit=delta_limit,
                                stall_limit=stall_limit)

    NUM_PARTICLES = 20
    INERTIA_WEIGHT = 0.8
    NEIGHBORHOOD_SIZE = 2
    COGNITIVE_WEIGHT = 1.3
    SOCIAL_WEIGHT = 1.3
    pso = ParticulairesSwarmOptimization(iterations=iterations,
                                        num_particles=NUM_PARTICLES,
                                        inertia_weight=INERTIA_WEIGHT,
                                        cognitive_weight=COGNITIVE_WEIGHT,
                                        social_weight=SOCIAL_WEIGHT,
                                        neighborhood_size=NEIGHBORHOOD_SIZE,
                                        delta_limit=delta_limit,
                                        stall_limit=stall_limit)

    TEMPERATURE = 1.0
    COOLING_RATE = 0.99
    COOLING_TYPE = 'linear' # 'exponential' , 'linear' , 'logarithmic'
    ADAPTIVE_FACTOR = 0.15
    sa = SimulatedAnnealing(max_iterations=iterations,
                            stagnation_value=delta_limit,
                            stagnation_iteration=stall_limit,
                            temperature=TEMPERATURE,
                            cooling_rate=COOLING_RATE,
                            cooling_type=COOLING_TYPE,
                            adaptive_factor=ADAPTIVE_FACTOR)

    for i in range(montecarlo_iteration):
        start_pso = time.perf_counter()
        pso_solution, pso_cost = pso.optimize()
        Helper.save_to_csv(f'pso_meilleur', i, pso_solution, pso_cost)
        if pso_cost < best_pso_cost:
            best_pso_solution = pso_solution.copy()
            best_pso_cost = pso_cost
        end_pso = time.perf_counter()
        print(f"pso iteration time: {end_pso - start_pso:.4f} seconds")

        start_de = time.perf_counter()
        de_solution, de_cost = de.optimize()
        Helper.save_to_csv(f'de_meilleur', i, de_solution, de_cost)
        if de_cost < best_differential_evolution_cost:
            best_differential_evolution_solution = de_solution.copy()
            best_differential_evolution_cost = de_cost
        end_de = time.perf_counter()
        print(f"de iteration time: {end_de - start_de:.4f} seconds")

        start_sa = time.perf_counter()
        sa_solution, sa_cost = sa.optimize()
        Helper.save_to_csv(f'sa_meilleur', i, sa_solution, sa_cost)
        if sa_cost < best_simulated_annealing_cost:
            best_simulated_annealing_solution = sa_solution.copy()
            best_simulated_annealing_cost = sa_cost
        end_sa = time.perf_counter()
        print(f"sa iteration time: {end_sa - start_sa:.4f} seconds")

    Helper().save_stats_from_csv()
    Helper.plot_cost_boxplot_per_file()
    Helper.plot_cost_boxplot_overall()
    Helper.plot_costs_sorted_per_file()
    Helper.plot_costs_sorted_overall()

    print("Meilleure solution Particle Swarm Optimization: ", best_pso_solution, "Coût: ", best_pso_cost)
    print("Meilleure solution Differential Evolution: ", best_differential_evolution_solution, "Coût: ", best_differential_evolution_cost)
    print("Meilleure solution Simulated Annealing: ", best_simulated_annealing_solution, "Coût: ", best_simulated_annealing_cost)


    """
    BONUS : Ant Colony Optimization
    """
    best_ant_colony_solution = None
    best_ant_colony_cost = float('inf')

    G = nx.random_geometric_graph(20, radius=0.4, seed=3).to_directed()
    pos = nx.get_node_attributes(G, "pos")
    pos[0] = (0.5, 0.5)
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            dist = np.linalg.norm(
                np.array(pos[i]) - np.array(pos[j])
            )
            G.add_edge(i, j, cout=dist)
            G.add_edge(j, i, cout=dist)

    MONTE_CARLO_ITERATION = 50
    ITERATIONS = 25
    TAU_INIT = 0.95
    NUM_ANTS = 30
    EVAPORATION = 0.3
    ALPHA = 1.0
    BETA = 2.0
    PHEROMONE_INIT = 1.0
    ELITISM_WEIGHT = 3

    for i in range(MONTE_CARLO_ITERATION):

        ac = AntColonyOptimization(
            graph=G,
            iterations=ITERATIONS,
            number_ants=NUM_ANTS,
            evaporation=EVAPORATION,
            alpha=ALPHA,
            beta=BETA,
            pheromone_init=PHEROMONE_INIT,
            elitism_weight=ELITISM_WEIGHT
        )

        start_ac = time.perf_counter()
        ac_solution, ac_cost = ac.optimize()
        Helper.save_to_csv(f'ac_meilleur', i, ac_solution, ac_cost)
        if ac_cost < best_ant_colony_cost:
            best_ant_colony_solution = ac_solution.copy()
            best_ant_colony_cost = ac_cost
        end_ac = time.perf_counter()
        print(f"ac iteration time: {end_ac - start_ac:.4f} seconds")
    path = list(zip(best_ant_colony_solution, best_ant_colony_solution[1:]))
    Helper.save_graph_plot(G=G, pos=pos, path_edges=path, name="ac_result" )
    print("Meilleure solution Ant Colony Optimization: ", best_ant_colony_solution, "Coût: ", best_ant_colony_cost)