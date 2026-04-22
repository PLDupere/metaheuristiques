import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class Helper:

    @staticmethod
    def save_to_csv(heuristique, iteration, solution, cost, results_dir='results'):
        os.makedirs(results_dir, exist_ok=True)

        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = os.path.join(results_dir, f'{heuristique}_{date_str}.csv')
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            fieldnames = ['iteration', 'solution', 'cost']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'iteration': iteration,
                'solution': str(solution),
                'cost': f"{cost:.5f}"
            })


    @staticmethod
    def save_stats_from_csv(results_dir='results'):
        folder = results_dir
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
    def plot_cost_boxplot_per_file(results_dir='results'):
        if not os.path.exists(results_dir):
            print(f"Erreur : Le dossier '{results_dir}' n'existe pas.")
            return
        for filename in os.listdir(results_dir):
            if filename.endswith("_stats.txt"):
                file_path = os.path.join(results_dir, filename)
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
                save_path = os.path.join(results_dir, f"{filename.replace('_stats.txt', '')}_boxplot.png")
                plt.savefig(save_path)
                plt.close(fig)


    @staticmethod
    def plot_cost_boxplot_overall(results_dir='results'):
        if not os.path.exists(results_dir):
            print(f"Erreur : Le dossier '{results_dir}' n'existe pas.")
            return

        data = {}
        found_file = False
        for filename in os.listdir(results_dir):
            if filename.endswith(".csv") and "iteration" in filename.lower():
                found_file = True
                file_path = os.path.join(results_dir, filename)
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
        save_path = os.path.join(results_dir, "all_iterations_boxplot.png")
        plt.savefig(save_path)
        plt.show()

