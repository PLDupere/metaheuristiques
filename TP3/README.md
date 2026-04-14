# Optimisation de design de ressorts

Ce projet compare plusieurs métaheuristiques appliquées au problème de conception de ressorts.

## Structure du projet

- `spring_design.py` : définition du problème d'optimisation et contraintes
- `particulaires_swarm_optimization.py` : implémentation de Particle Swarm Optimization (PSO)
- `differential_evolution.py` : implémentation de Differential Evolution (DE)
- `ant_colony_optimization.py` : implémentation de Ant Colony Optimization (ACO)
- `simulated_annealing.py` : implémentation de Simulated Annealing (SA)
- `helper.py` : utilitaires de saisie, sauvegarde CSV et visualisation
- `main.py` : point d'entrée principal qui exécute les algorithmes et génère les résultats
- `results/` : répertoire de sortie contenant les fichiers CSV et les graphiques générés

## Installation des dépendances

1. Créez un environnement virtuel dans le dossier du projet :
   ```bash
   python3 -m venv .venv
   ```

2. Activez l'environnement virtuel :
   - Linux/macOS :
     ```bash
     source .venv/bin/activate
     ```
   - Sur Windows :
     ```
     .venv\Scripts\activate
     ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Vérifiez que l'environnement est bien activé avant d'exécuter le script.

## Lancer les expériences

### Configuration des constantes dans `main.py`

Le fichier `main.py` contient les valeurs de configuration par défaut. Il est possible d'ajustées directement dans le fichier avant d'exécuter le programme :

- DE : `POP_SIZE`, `MUTATION_FACTOR`, `CROSSOVER_RATE`
- PSO : `NUM_PARTICLES`, `INERTIA_WEIGHT`, `NEIGHBORHOOD_SIZE`, `COGNITIVE_WEIGHT`, `SOCIAL_WEIGHT`
- ACO : `NUM_ANTS`, `EVAPORATION`, `FACTOR`, `PHEROMONE_INIT`, `PHEROMONE_INCREASE_FACTOR`, `TOP_PHEROMONES`
- SA : `TEMPERATURE`, `COOLING_RATE`, `COOLING_TYPE`, `ADAPTIVE_FACTOR`

1. Avec l'environnement `.venv` activé, lancez :
   ```bash
   python3 main.py
   ```

2. Répondez aux questions affichées dans le terminal :
   - nombre de simulations Monte-Carlo
   - nombre d'itérations
   - limite de stagnation
   - delta limite pour la stagnation

3. Le script exécute les algorithmes suivants :
   - Particle Swarm Optimization (PSO)
   - Differential Evolution (DE)
   - Simulated Annealing (SA)
      - Ant Colony Optimization (ACO) en bonus

4. Les résultats sont enregistrés automatiquement dans le dossier `results/`.


## Prérequis

- Python 3.13.12
- numpy
- matplotlib
- scipy
- pandas
- networkx

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

