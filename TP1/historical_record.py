import csv
import os
from datetime import datetime

class HistoricalRecord:

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
                'cost': cost
            })
