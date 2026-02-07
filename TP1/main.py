from random_search import RandomSearch


if __name__ == "__main__":

    print("Choisir la métaheuristique à exécuter:")
    print("1. Hill Climbing")
    print("2. Generalized Hill Climbing")
    print("3. Recuit simulé (Simulated Annealing)")
    heuristique_value = input("Entrez le numéro de votre choix (1, 2 ou 3): ").strip()

    montecarlo_iteration = input("Spécifier  le  nombre  de simulations de Monte-Carlo : (5000 par exemple) ").strip()
    stagnation_value = input("Définit la valeur de stagnation : (0.001 par exemple) ").strip().replace(',', '.')
    stagnation_iteration = input("Définit le nombre d'itérations de stagnation : (20 par exemple) ").strip()

    random_search = RandomSearch()
    best_solution, best_cost = random_search.evaluate(  int(montecarlo_iteration),
                                                        int(heuristique_value),
                                                        float(stagnation_value),
                                                        int(stagnation_iteration))
    print(f"Meilleur solution: {best_solution}, Meilleur coût: {best_cost}")


    print("Fin du programme")
