import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import time
import networkx as nx
import math

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
    def get_value_between_0_and_1(text):
        while True:
            enter = input(text).strip().replace(',', '.')
            value = float(enter)
            if 0 <= value <= 1:
                return value
            else:
                print("Erreur : Le pourcentage de variation doit être compris entre 0 et 1.")


    @staticmethod
    def save_stats_from_csv():
        folder = 'results'
        os.makedirs(folder, exist_ok=True)

        for filename in os.listdir(folder):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path)

                if 'cost' in df.columns:
                    cost_series = pd.to_numeric(df['cost'], errors='coerce').dropna()

                    stats = {
                        "count": cost_series.count(),
                        "mean": cost_series.mean(),
                        "min": cost_series.min(),
                        "q1 (25%)": cost_series.quantile(0.25),
                        "median (q2, 50%)": cost_series.median(),
                        "q3 (75%)": cost_series.quantile(0.75),
                        "max": cost_series.max(),
                        "std": cost_series.std(),
                    }

                    txt_filename = os.path.join(folder, f"{os.path.splitext(filename)[0]}_stats.txt")
                    with open(txt_filename, "w") as f:
                        f.write(f"Statistiques pour {filename}\n")
                        for k, v in stats.items():
                            f.write(f"{k}: {v}\n")


    @staticmethod
    def plot_cost_boxplot_per_file(folder='results'):
        if not os.path.exists(folder):
            print(f"Erreur : Le dossier '{folder}' n'existe pas.")
            return
        for filename in os.listdir(folder):
            if filename.endswith("_stats.txt"):
                file_path = os.path.join(folder, filename)
                stats_dict = {}
                with open(file_path, "r") as f:
                    for line in f:
                        if ':' in line:
                            key, value = line.strip().split(":")
                            key = key.strip()
                            value = float(value.strip())
                            stats_dict[key] = value

                box_data = [
                    stats_dict['min'],
                    stats_dict['q1 (25%)'],
                    stats_dict['median (q2, 50%)'],
                    stats_dict['q3 (75%)'],
                    stats_dict['max']
                ]

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.boxplot([box_data], labels=[filename.replace("_stats.txt", "")], patch_artist=True)
                ax.set_title(f"Répartition des coûts: {filename}")
                ax.set_ylabel("Cost")
                plt.tight_layout()
                save_path = os.path.join(folder, f"{filename.replace('_stats.txt', '')}_boxplot.png")
                plt.savefig(save_path)
                plt.close(fig)


    @staticmethod
    def plot_cost_boxplot_overall(folder='results'):
        if not os.path.exists(folder):
            print(f"Erreur : Le dossier '{folder}' n'existe pas.")
            return

        data = {}
        found_file = False
        for filename in os.listdir(folder):
            if filename.endswith(".csv") and "iteration" in filename.lower():
                found_file = True
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path)

                if 'cost' in df.columns:
                    costs = pd.to_numeric(df['cost'], errors='coerce').dropna()
                    data[filename.replace(".csv","")] = costs.tolist()

        if not found_file or not data:
            print("Erreur : Aucun fichier CSV valide trouvé.")
            return

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.boxplot(data.values(), labels=list(data.keys()), patch_artist=True)
        ax.set_title("Répartition des coûts par fichier / itérations")
        ax.set_ylabel("Cost")
        plt.xticks(rotation=45)
        plt.tight_layout()
        save_path = os.path.join(folder, "all_iterations_boxplot.png")
        plt.savefig(save_path)
        plt.show()


    @staticmethod
    def get_costs_sorted_per_file(folder='results', keyword="iteration"):
        if not os.path.exists(folder):
            print(f"Erreur : Le dossier '{folder}' n'existe pas.")
            return {}
    
        costs_per_file = {}
        for filename in os.listdir(folder):
            if filename.endswith(".csv") and keyword.lower() in filename.lower():
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path)
                if 'cost' in df.columns:
                    costs = pd.to_numeric(df['cost'], errors='coerce').dropna().tolist()
                    costs.sort(reverse=True)
                    costs_per_file[filename] = costs

        if not costs_per_file:
            print("Erreur : Aucun fichier CSV avec des coûts trouvé.")
            return {}

        return costs_per_file


    @staticmethod
    def plot_costs_sorted_per_file(folder='results', keyword="iteration"):
        costs_per_file = Helper.get_costs_sorted_per_file(folder, keyword)
        if not costs_per_file:
            print("Erreur : Aucun fichier avec coûts trouvé pour le plot.")
            return

        for filename, costs in costs_per_file.items():
            plt.figure(figsize=(8,4))
            plt.plot(range(1, len(costs)+1), costs, marker='o', linestyle='-', alpha=0.7)
            plt.xlabel("Index (du plus grand au plus petit)")
            plt.ylabel("Cost")
            plt.title(f"Évolution des coûts triés : {filename.replace('.csv','')}")
            plt.grid(True)
            plt.tight_layout()
            save_path = os.path.join(folder, f"{filename.replace('.csv','')}_sorted_costs.png")
            plt.savefig(save_path)
            plt.close()


    @staticmethod
    def get_all_costs_overall(folder='results', keyword="iteration"):
        if not os.path.exists(folder):
            print(f"Erreur : Le dossier '{folder}' n'existe pas.")
            return []

        all_costs = []
        for filename in os.listdir(folder):
            if filename.endswith(".csv") and keyword.lower() in filename.lower():
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path)

                if 'cost' in df.columns:
                    costs = pd.to_numeric(df['cost'], errors='coerce').dropna()
                    all_costs.extend(costs.tolist())

        if not all_costs:
            print("Erreur : Aucune valeur de cost trouvée.") 
            return []

        all_costs.sort(reverse=True)
        return all_costs


    @staticmethod
    def plot_costs_sorted_overall(folder='results', keyword="iteration"):
        costs_per_file = Helper.get_costs_sorted_per_file(folder, keyword)
        all_costs = Helper.get_all_costs_overall(folder, keyword)

        if not costs_per_file:
            print("Erreur : Aucun fichier avec coûts trouvé pour le plot.")
            return

        plt.figure(figsize=(12,6))
        for filename, costs in costs_per_file.items():
            plt.plot(range(1, len(costs)+1), costs, marker='o', linestyle='-', alpha=0.7, label=filename.replace(".csv",""))

        if all_costs:
            plt.plot(range(1, len(all_costs)+1), all_costs, linestyle='--', color='black', alpha=0.8, label='Somme de tous les coûts valides')

        plt.xlabel("Index (du plus grand au plus petit)")
        plt.ylabel("Cost")
        plt.title("Évolution des coûts triés par fichier")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        save_path = os.path.join(folder, "all_sorted_costs_plot.png")
        plt.savefig(save_path)
        plt.show()


    @staticmethod
    def save_graph_plot(G, pos, path_edges=None, name="graph"):
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        plt.figure(figsize=(10, 8))
        nx.draw_networkx_edges(G, pos, edge_color="blue", width=0.5)

        if path_edges is not None:
            nx.draw_networkx(
                G,
                pos,
                with_labels=True,
                edgelist=path_edges,
                edge_color="red",
                node_size=200,
                width=3,
            )
        else:
            nx.draw_networkx(G, pos, with_labels=True, node_size=200)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{results_dir}/{name}_{timestamp}.png"
        plt.savefig(filename, bbox_inches="tight")
        plt.close()
        print(f"[Helper] Graph saved: {filename}")
        return filename
    