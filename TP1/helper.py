import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

class Helper:

    @staticmethod
    def save_to_csv(heuristique, iteration, solution, cost):
        folder = 'results'
        os.makedirs(folder, exist_ok=True)

        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = os.path.join(folder, f'{heuristique}_{date_str}.csv')
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            fieldnames = ['iteration', 'solution', 'cost']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'iteration': iteration,
                'solution': solution,
                'cost': f"{cost:.5f}"
            })


    @staticmethod
    def get_cooling_type():
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


    @staticmethod
    def get_boolean_input(text):
        while True:
            user_input = input(text).strip().lower()
            if user_input in ['yes', 'y']:
                return True
            elif user_input in ['no', 'n']:
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


    @staticmethod
    def get_integer_input(text):
        while True:
            enter = input(text).strip()
            value = int(enter)
            if value > 0:
                return value
            else:
                print("Erreur : Le nombre positif.")


    @staticmethod
    def get_float_input(text):
        while True:
            enter = input(text).strip().replace(',', '.')
            value = float(enter)
            if value > 0:
                return value
            else:
                print("Erreur : Le facteur d'adaptation doit être un nombre positif.")


    @staticmethod
    def get_pourcentage_variation():
        while True:
            enter = input("Entrez le pourcentage de variation (0.25 par exemple) : ").strip().replace(',', '.')
            pourcentage_variation = float(enter)
            if 0 <= pourcentage_variation <= 1:
                return pourcentage_variation
            else:
                print("Erreur : Le pourcentage de variation doit être compris entre 0 et 1.")


    def plot_solution(self, best_random_solution, best_climbing_hill_solution, best_simulated_annealing_solution):
        # https://matplotlib.org/stable/api/pyplot_summary.html
        fig = plt.figure(figsize=(9,7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(best_random_solution[0], best_random_solution[1], best_random_solution[2], alpha=0.15, s=50, color='blue', label='random search')
        ax.scatter(best_climbing_hill_solution[0], best_climbing_hill_solution[1], best_climbing_hill_solution[2], alpha=0.15, s=50, color='green', label='Hill Climbing')
        ax.scatter(best_simulated_annealing_solution[0], best_simulated_annealing_solution[1], best_simulated_annealing_solution[2], alpha=0.15, s=50, color='red', label='Simulated Annealing')
        ax.set_xlabel('Diamètre du fil (x0)')
        ax.set_ylabel('Diamètre spirale (x1)')
        ax.set_zlabel('Nb spirales (x2)')
        ax.set_title('Meilleures solutions trouvées')
        ax.legend()
        plt.savefig("results/valid_space.png")
        print("Plot saved: results/valid_space.png")
