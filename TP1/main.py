from spring_design import SpringDesign
from random_search import RandomSearch

if __name__ == "__main__":

    # 1.1. Interface simple (CLI)
    algorithme_value = input("Choisir la métaheuristique à exécuter: ").strip().lower()
    montecarlo_value = input("Spécifier  le  nombre  de simulations de Monte-Carlo : ").strip().lower()
    stagnation_value = input("Définit la conditions d'arrêt : ").strip().lower()

    spring_design = SpringDesign()

    print(f"Algorithme choisi : {algorithme_value}")
