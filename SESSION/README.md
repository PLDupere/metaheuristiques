# MO_IFCMS - Multi-Objective Fuzzy C-Means Segmentation

Implémentation de l'algorithme MO_IFCMS (Multi-Objective Fuzzy C-Means Segmentation) utilisant l'optimisation par essaims particulaires (PSO) pour la segmentation d'images.


## Prérequis

- Python 3.14.2
- numpy
- opencv-python

## Configuration de l'environnement virtuel et exécution

1. Créez un environnement virtuel :
   ```
   python3 -m venv .venv
   ```

2. Activez-le et installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

3. Activez l'environnement virtuel :
   - Sur Linux/Mac :
     ```
     source .venv/bin/activate
     ```
   - Sur Windows :
     ```
     .venv\Scripts\activate
     ```

4. Exécutez le script principal :
   ```
   python3 main.py
   ```

5. Pour désactiver :
   ```
   deactivate
   ```

## Utilisation



## Pseudo code de l'algorithme  III.1 MO_IFCMS [1]
1: Initialiser aléatoirement les positions des particules (centres des classes) c(0)
i dans la plage
des niveaux de gris présents dans l’image et initialiser les vitesses des particules à 0.
2: Pour chaque particule Faire
3: Calculer les fonctions objectifs en utilisant les équations (Eqs. (III.5)) and ((III.9))
4: Fin Pour
5: Sauvegarder les solutions non dominées dans l’archive externe et générer les hypercubes
comme système de coordonnées (voir section III.2)
6: Initialiser les meilleures solutions personnelles pour chaque particule avec sa position initiale
7: Pour k = 1 Jusqu’au nombre maximal d’itérations Faire
8: Pour chaque particule Faire
9: Choisir un leader (Rep(h)) de l’archive externe en utilisant la roulette russe (voir
section III.2)
10: Mettre à jour les vitesses des particules en utilisant l’équation (Eq. (III.3))
11: Mettre à jour les positions des particules (centres des classes) en utilisant l’équation
(Eq. (III.4))
12: Maintenir les positions des particules dans l’espace de recherche. Si la position d’une
particule sort du domaine de recherche, elle prend la valeur limite et sa vitesse est multipliée
par (≠1)
13: Calculer les fonctions objectifs en utilisant les équations (Eqs. (III.5)) et ((III.9))
14: Mettre à jour la mémoire des particules : la meilleure solution (au sens de Pareto)
entre la nouvelle et l’ancienne est retenue dans la mémoire. Si aucune ne domine l’autre,
l’une des deux est choisie aléatoirement.
15: Fin Pour
16: Mettre à jour le contenu de l’archive externe
17: Fin Pour
18: Pour chaque solution (particule) dans l’archive externe Faire
19: Calculer les degrés d’appartenance en utilisant l’équation (Eq. (II.12))
20: Trier les centres de classes pour que chaque classe ait le même label dans l’ensemble des
solutions
21: Déterminer la segmentation d’image en utilisant le principe du maximum du degré
d’appartenance
22: Calculer pour chaque classe le seuil T en utilisant l’équation (Eq. (III.10))
23: Fin Pour
24: Déterminer l’ensemble des pixels n’ayant pas le même label dans l’ensemble des solutions
et les pixels ayant un degré d’appartenance inférieur au seuil T . Ces pixels représentent
l’ensemble des pixels potentiellement mal classés.
25: Pour chaque pixel extrait (xi) Faire
26: Pour j = 1 to N3 Faire
27: Calculer la fonction objectif J(j) i à l’aide de l’équation (Eq. (III.11))
28: Fin Pour
29: Trouver j = argmin(J(j)i )
30: Affecter le pixel xi à la classe j
31: Fin Pour


