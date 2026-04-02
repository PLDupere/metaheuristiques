## Structure du Projet

Projet d'optimisation de design de ressorts utilisant trois métaheuristiques : Particulaires Swarm Optimization, Differential Evolution, et Ant Colony Optimization.

- **spring_design.py** : Classe principale définissant le problème d'optimisation avec la fonction objectif et les contraintes.

- **particulaires_swarm_optimization.py** : .

- **differential_evolution.py** : .

- **ant_colony_optimization.py** : .

- **helper.py** : Classe utilitaire contenant des fonctions pour l'entrée utilisateur, la sauvegarde des résultats en CSV et la visualisation 3D des solutions.

- **main.py** : Point d'entrée principal qui coordonne l'exécution des trois algorithmes sur plusieurs itérations Monte-Carlo.

- **results/** : Répertoire contenant les fichiers CSV avec les résultats et le graphique de visualisation.

## Utilisation

1. Activez l'environnement virtuel :
   - Sur Linux/Mac :
     ```
     source .venv/bin/activate
     ```
   - Sur Windows :
     ```
     .venv\Scripts\activate
     ```

2. Exécutez le script principal :
   ```
   python main.py
   ```

3. Suivez les instructions pour configurer :
   - Nombre de simulations Monte-Carlo
   - Paramètres du Random Search
   - Paramètres du Hill Climbing (variation, voisinage, stagnation)
   - Paramètres du Simulated Annealing (température, refroidissement)

4. Les résultats seront sauvegardés dans le répertoire `results/`.

## Prérequis

- Python 3.13.12
- numpy
- matplotlib
- scipy

## Configuration de l'environnement virtuel

1. Créez un environnement virtuel :
   ```
   python3 -m venv .venv
   ```

2. Activez-le et installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

3. Pour désactiver :
   ```
   deactivate
   ```

