
---

# Optimisation par Métaheuristiques : Recherche Aléatoire, Hill Climbing et Recuit Simulé


Dans cet article, nous explorons plusieurs **métaheuristiques d’optimisation** utilisées pour résoudre un problème d’optimisation classique.

L’objectif est de comparer trois approches :

- Recherche aléatoire
- Hill Climbing
- Recuit simulé

Ces méthodes ont été testées via plusieurs simulations Monte-Carlo afin d’évaluer leur performance, leur capacité d’exploration et leur convergence.

---

# Contexte du problème

Le problème consiste à optimiser les paramètres d’un ressort :

- diamètre du fil
- diamètre moyen de la spirale
- nombre de spires

Ces variables doivent respecter plusieurs contraintes physiques.

La fonction objective cherche à minimiser un coût tout en respectant ces contraintes.

Certaines solutions générées sont donc invalides.

---

# Interface CLI

Une interface en ligne de commande permet de configurer :

- nombre d’itérations
- nombre de simulations Monte-Carlo
- paramètres des métaheuristiques

Ces paramètres sont partagés entre les algorithmes afin de permettre une comparaison équitable.

Exemples de paramètres :

- seuil de stagnation
- nombre de voisins (Hill Climbing)
- taux de refroidissement (recuit simulé)

---

# 1. Recherche Aléatoire

## Principe

La recherche aléatoire est la méthode la plus simple.

1. Générer une solution aléatoire
2. Vérifier les contraintes
3. Calculer le coût
4. Garder la meilleure solution trouvée

Pseudo-processus :

```
best = random_solution()

repeat N times:
    s = random_solution()
    if cost(s) < cost(best):
        best = s
```

## Observations

Lors de 100 exécutions avec 100 itérations :

- seulement **0 à 1** solutions valides en moyenne
- environ **0.5 %** de solutions valides

---

# 2. Hill Climbing

Le Hill Climbing est une méthode d’optimisation locale.

On part d’une solution initiale et on cherche une meilleure solution dans son voisinage.

---

# Hill Climbing simple (1+1)

## Principe

1. Générer un voisin
2. Si la solution est meilleure → on l’accepte
3. Sinon → on la rejette

```
courant = solution_aleatoire()

répéter :
    voisin = variation(courant)
    si coût(voisin) < coût(courant) :
        courant = voisin
```

## Problème rencontré

Modifie une seule variable à la fois.

Résultat :

- exploration très limitée
- stagnation rapide

---

# Hill Climbing généralisé (1, λ)

On génère plusieurs voisins.

```
courant = solution_aleatoire()
voisins = générer_variations(courant,variation, λ)

répéter :
    pour chaque i de 0 à λ - 1 :
        voisin = variation(voisins[i])
        si coût(voisin) < coût(courant) :
            courant = voisin
```

Avantages :

- meilleure couverture de l’espace
- réduction du risque de stagnation
- convergence plus stable

Cependant :

- plus de calcul
- plus de temps CPU

---

# Gestion des contraintes

Une pénalité est ajoutée lorsque :

- les bornes sont dépassées
- les contraintes sont violées

Lorsque trop de pénalités apparaissent :

- on réduit le pourcentage de variation.

Cela permet de recentrer la recherche.

---

# 3. Recuit Simulé

Le recuit simulé est inspiré de la métallurgie.

L’idée :

- accepter parfois des solutions pires
- afin d’éviter les minima locaux.

La probabilité dépend de la **température**.

```
répéter:

    Créer tmp_solution, current_solution

    Pour chaque variable dans tmp_solution:
        Générer une variation aléatoire
        Mettre à jour de tmp_solution

        Calculer tmp_cost avec tmp_solution
        delta = tmp_cost - current_cost

        Si la nouvelle cost est meilleure ou acceptée par probabilité :
            Mettre à jour current_solution et current_cost

        Si la solution est valide et meilleure :
			Mettre à jour best_solution

        Réduire temperature
```

---

# Stratégies de refroidissement

## Refroidissement exponentiel

```
T = T * cooling_rate
```

Avantages :

- exploration rapide au début
- convergence rapide

Inconvénient :

- peut geler trop vite

---

# Refroidissement linéaire

```
T = T0 - k * iteration
```

Avantages :

- comportement stable
- contrôle simple

---

# Refroidissement logarithmique

```
T = T0 / log(iteration)
```

Avantages :

- exploration plus longue

Inconvénient :

- plus coûteux

---

# Réchauffement

Lorsque l’algorithme stagne :

- on augmente temporairement la température.

Cela permet :

- d’explorer une nouvelle zone
- d’éviter un minimum local

Cependant :

- trop de réchauffement peut dégrader la convergence.


---

# Protocole expérimental

Paramètres :

- 1000 simulations Monte-Carlo
- 1000 itérations par exécution

Hill Climbing :

- 250 voisins
    
- variation de 25 %
    

Recuit simulé :

- réchauffement : +20 %
- stagnation : 50 itérations
- coefficient : 0.95

---

# Résultats

## Recherche aléatoire

| Min     | Médiane  | Moyenne    |
| ------- | -------- | ---------- |
| 4,09349 | 10,51418 | 10,8249027 |

- 47 % de solutions invalides
- 0 a 2 solution valide par 100 itérations rend 
- respecte la courbe de distributions par une exploration uniforme

Cette méthode utilise beaucoup de temps calcule pour obtenir aucune information.

---

# Hill Climbing

| Min     | Médiane  | Moyenne    |
| ------- | -------- | ---------- |
| 4,00626 | 12,53497 | 20,1367856 |

- seulement **1 solution invalide**
- favorise l'exploitation d'une solution valide


L'algorithme prend beaucoup de temps de calcul lorsqu'il y a beaucoup de voisin a calculer.

---

# Recuit simulé exponentiel

| Min     | Médiane | Moyenne    |
| ------- | ------- | ---------- |
| 4,00466 | 8,01789 | 8,37838168 |

- meilleure exploration
- plus de solutions invalides.

---

# Recuit simulé linéaire

| Min     | Médiane | Moyenne    |
| ------- | ------- | ---------- |
| 4,00478 | 4,00815 | 5,27217935 |

C’est la **meilleure performance globale**.

- convergence stable
- résultats robustes.

---

# Recuit simulé logarithmique

| Min     | Médiane | Moyenne    |
| ------- | ------- | ---------- |
| 4,00455 | 5,28598 | 5,71571398 |

Bon résultat minimal mais convergence plus lente.

---

# Analyse des résultats

Observations importantes :

### Recherche aléatoire

- exploration totale
- efficacité très faible.

### Hill Climbing

- convergence rapide
- forte dépendance aux paramètres.

### Recuit simulé

- meilleur compromis
- évite les minima locaux.

Le refroidissement linéaire offre le **meilleur équilibre**.

---
