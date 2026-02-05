from spring_design import SpringDesign
from random_search import RandomSearch
from scipy.optimize import minimize

if __name__ == "__main__":

    # 1.1. Interface simple (CLI)
    print("Choisir la métaheuristique à exécuter:")
    print("1. Hill Climbing")
    print("2. Generalized Hill Climbing")
    print("3. Contraintes de Stagnation")
    heuristique_value = input("Entrez le numéro de votre choix (1, 2 ou 3): ").strip()
    montecarlo_value = 50

    # montecarlo_value = input("Spécifier  le  nombre  de simulations de Monte-Carlo : ").strip().lower()
    # stagnation_value = input("Définit la conditions d'arrêt : ").strip().lower()

    random_search = RandomSearch()
    best_solution, best_cost = random_search.evaluate(int(montecarlo_value), int(heuristique_value))
    print(f"Best solution: {best_solution}, Best cost: {best_cost}")

    # random_search = RandomSearch(max_iterations=int(montecarlo_value))
    

    # spring_design = SpringDesign()

    print("END OF PROGRAM")
    print(":)")
