import numpy as np
from calcul import Calcul
from archive import ArchivePareto
from equations.thresholds import ThresholdCalculator


class Particle:
    def __init__(self, n_clusters, min_val, max_val):
        # Étape 1 : Initialiser des positions et vitesses à 0
        self.position = np.random.uniform(min_val, max_val, n_clusters)
        self.velocity = np.zeros(n_clusters)
        # Étape 6 : Initialiser les meilleures solutions personnelles
        self.best_position = self.position.copy()
        self.best_objectives = [float('inf'), float('inf')]  # [J_IFCMS, J_edge]

    def update_best(self, objectives):
        objectives = [float(obj) for obj in objectives]
        # Si la nouvelle solution domine l'ancienne
        if (objectives[0] < self.best_objectives[0] and objectives[1] <= self.best_objectives[1]) or \
            (objectives[0] <= self.best_objectives[0] and objectives[1] < self.best_objectives[1]):
            self.best_position = self.position.copy()
            self.best_objectives = objectives
        # Si aucune ne domine l'autre, choisir aléatoirement
        elif not ((self.best_objectives[0] < objectives[0] and self.best_objectives[1] <= objectives[1]) or \
                    (self.best_objectives[0] <= objectives[0] and self.best_objectives[1] < objectives[1])):
            if np.random.rand() < 0.5:
                self.best_position = self.position.copy()
                self.best_objectives = objectives


class Algorithm:
    def __init__(self, image):
        self.image = image
        self.formulas = Calcul(image)

    def segmentation(self, n_clusters=3, n_particles=20, n_iter=1, 
                        w=0.7, c1=1.5, c2=1.5):

        # Étape 1 : Initialiser aléatoirement les positions des particules
        min_val = np.min(self.image)
        max_val = np.max(self.image)

        particles = [
            Particle(n_clusters, min_val, max_val)
            for _ in range(n_particles)
        ]

        # Étape 5 : Sauvegarder les solutions non dominées dans l’archive
        archive = ArchivePareto(max_size=100)

        for p in particles:
            # Étape 3 : Calculer les fonctions objectifs en utilisant les équation (III.5 et III.9)
            J_ifcms = self.formulas.compute_J_IFCMS(p.position)
            J_edge = self.formulas.compute_J_edge(p.position)
            objectives = [J_ifcms, J_edge]
            
            # Étape 5 : Sauvegarder les solutions non dominées dans l’archive
            archive.update(p.position, objectives)
            
            # Étape 6 : Initialiser les meilleures solutions personnelles pour chaque particule
            p.update_best(objectives)
        
        print(f"Archive initiale: {archive.size()} solutions")
        
        # Étape 7 : Pour k = 1 Jusqu’au nombre maximal d’itérations
        for iteration in range(n_iter):
            # Étape 8 : Pour chaque particule Faire
            for p in particles:
                # Étape 9 : Choisir un leader de l’archive externe en utilisant la roulette russe
                Rep_h = archive.select_russian_roulette()
                
                if Rep_h is None:
                    Rep_h = p.best_position
                
                # Étape 10 : Mettre à jour les vitesses des particules en utilisant l’équation (III.3)
                rand1, rand2 = np.random.rand(2)
                p.velocity = (
                    w * p.velocity
                    + c1 * rand1 * (p.best_position - p.position)
                    + c2 * rand2 * (Rep_h - p.position)
                )
                
                # Étape 11 : Mettre à jour les positions des particules (centres des classes) en utilisant l’équation (III.4)
                p.position += p.velocity
                
                # Étape 12 : Maintenir les positions des particules dans l’espace de recherche
                p.position = np.clip(p.position, min_val, max_val)
                # Si sort du domaine, multiplier la vitesse par -1
                out_of_bounds = (p.position < min_val) | (p.position > max_val)
                p.velocity[out_of_bounds] *= -1
                
                # Étape 13 : Calculer les fonctions objectifs en utilisant les équations (III.5 et III.9)
                J_ifcms = self.formulas.compute_J_IFCMS(p.position)
                J_edge = self.formulas.compute_J_edge(p.position)
                objectives = [J_ifcms, J_edge]
                
                # Étape 14 : Mettre à jour la mémoire des particules
                p.update_best(objectives)
            # Étape 15 : Fin Pour
            # Étape 16 : Mettre à jour le contenu de l’archive externe
            for p in particles:
                J_ifcms = self.formulas.compute_J_IFCMS(p.position)
                J_edge = self.formulas.compute_J_edge(p.position)
                archive.update(p.position, [J_ifcms, J_edge])
            
            if (iteration + 1) % max(1, n_iter // 10) == 0:
                print(f"Itération {iteration + 1}/{n_iter}: Archive={archive.size()} solutions")
        # Étape 17 : Fin Pour
        # Étape 18 : Pour chaque solution (particule) dans l’archive externe
        solutions, objectives = archive.get_all_solutions()
        
        if len(solutions) == 0:
            print("Aucune solution dans l'archive")
            return np.array([]), archive

        U_matrices = []
        labels_list = []
        
        for solution in solutions:
            # Étape 19 : Calculer les degrés d’appartenance
            U = self.formulas.compute_degree_membership(solution)
            # Étape 20 : Trier les centres de classes pour que chaque classe ait le même label
            labels = np.argmax(U, axis=0).reshape(self.image.shape).astype(int)
            U_matrices.append(U)
            labels_list.append(labels.flatten())
        
        # Étape III.3.4.1 : Détection des pixels mal classés
        # Étape 22 :  Calculer pour chaque classe le seuil T en utilisant l’équation (III.10)
        thresholds_list = []
        for U in U_matrices:
            thresholds = ThresholdCalculator.compute_thresholds(U.T)
            thresholds_list.append(thresholds)
        # Étape 23 : Fin Pour
        # Étape 24 : Déterminer l’ensemble des pixels représentent l'ensemble des pixels potentiellement mal classés
        misclassified_pixels = self.formulas.find_misclassified_pixels(
            solutions, U_matrices, labels_list, thresholds_list
        )

        # Étape III.3.4.2 : Reclassification des pixels mal classés
        # Étape 25-31 : Raffinement des pixels mal classés
        if len(misclassified_pixels) > 0:
            refined_labels = self.formulas.refine_misclassified_pixels(
                solutions, misclassified_pixels, U_matrices, labels_list
            )
            best_solution = self.formulas.labels_to_centers(refined_labels.reshape(self.image.shape))
        else:
            best_solution = solutions[0]

        print(f"{len(misclassified_pixels)} pixels raffinés")

        return best_solution, archive






