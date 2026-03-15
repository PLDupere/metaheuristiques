# 8INF852_TP02_Version_Gen_Starter

## Description

Ce projet est une implémentation d'algorithmes métaheuristiques pour la génération de mots en français. Il utilise des modèles de langage trigram pour évaluer la "francité" des mots générés et applique des algorithmes génétiques (avec mutation et croisement) ainsi qu'un algorithme d'estimation de distribution (UMDA) pour optimiser la génération de mots.

Le projet fait partie du TP2 du cours 8INF852 sur les métaheuristiques.

## Fonctionnalités

- Génération de mots aléatoires à partir d'un dictionnaire français
- Construction d'un modèle trigram à partir d'un corpus d'entraînement
- Algorithmes implémentés :
  - Algorithme génétique avec mutation (sélection par tournoi)
  - Algorithme génétique avec croisement à un point (sélection par roulette)
  - Algorithme génétique avec croisement à plusieurs points (sélection par tournoi)
  - Algorithme UMDA (Univariate Marginal Distribution Algorithm)

## Prérequis

- Python 3.14
- Librairies : nltk, numpy, requests, pyyaml

## Installation

1. Cloner le dépôt :
   ```
   git clone <url_du_dépôt>
   cd TP2
   ```

2. Créer un environnement virtuel (recommandé) :
   ```
   python -m venv .venv
   source .venv/bin/activate  # Sur Linux/Mac
   # ou .venv\Scripts\activate sur Windows
   ```

3. Installer les dépendances :
   ```
   pip install nltk
   pip install numpy
   pip install requests
   pip install pyyaml
   ```

## Utilisation

1. Configurer les paramètres dans `parameters.yaml`
2. Exécuter le programme principal :
   ```
   python main.py
   ```

Les résultats sont sauvegardés dans le dossier `results/` sous forme de fichiers CSV.

## Structure du projet

- `main.py` : Programme principal orchestrant les algorithmes
- `ga_mutation.py` : Implémentation de l'algorithme génétique avec mutation
- `ga_crossover1.py` : Algorithme génétique avec croisement à un point
- `ga_crossover2.py` : Algorithme génétique avec croisement à plusieurs points
- `eda_umda.py` : Algorithme UMDA
- `gen_lm.py` : Génération du modèle de langage trigram
- `generate_corpus.py` : Génération du corpus d'entraînement
- `helper.py` : Fonctions utilitaires
- `parameters.yaml` : Fichier de configuration des paramètres
- `lexique/Lexique383.tsv` : Lexique français utilisé
- `results/` : Dossier contenant les résultats des exécutions

## Résultats

Les résultats incluent :
- `mutat.csv` : Résultats de l'algorithme avec mutation
- `cross1.csv` : Résultats du croisement à un point
- `cross2.csv` : Résultats du croisement à plusieurs points
- `umda.csv` : Résultats de l'algorithme UMDA
- `words*.csv` : Mots générés à différentes étapes
