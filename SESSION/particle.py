import numpy as np
from calcul import Calcul
from archive import ArchivePareto
from equations.thresholds import ThresholdCalculator


class Agent:
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


class Particle:
    def __init__(self, image):
        self.image = image
        self.formulas = Calcul(image)

    def PSO_segmentation(self, n_clusters=3, n_particles=20, n_iter=1, 
                        w=0.7, c1=1.5, c2=1.5):

        # Étape 1 : Initialiser aléatoirement les positions des particules
        min_val = np.min(self.image)
        max_val = np.max(self.image)

        particles = [
            Agent(n_clusters, min_val, max_val)
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
            # Étape 16 : Pour chaque solution (particule) dans l’archive
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
        misclassified_pixels = self._find_misclassified_pixels(
            solutions, U_matrices, labels_list, thresholds_list
        )

        # Étape III.3.4.2 : Reclassification des pixels mal classés
        # Étape 25-31 : Raffinement des pixels mal classés
        if len(misclassified_pixels) > 0:
            refined_labels = self._refine_misclassified_pixels(
                solutions, misclassified_pixels, U_matrices, labels_list
            )
            best_solution = self._labels_to_centers(refined_labels.reshape(self.image.shape))
        else:
            best_solution = solutions[0]

        print(f"{len(misclassified_pixels)} pixels raffinés")

        return best_solution, archive





    def _find_misclassified_pixels(self, solutions, U_matrices, labels_list, thresholds_list):
        """
        # Étape 24 : Déterminer l'ensemble des pixels n'ayant pas le même label dans l'ensemble des solutions
                    et les pixels ayant un degré d'appartenance inférieur au seuil T
        """
        if len(solutions) == 0 or len(U_matrices) == 0:
            return []

        n_pixels = self.image.size
        misclassified = set()

        if len(labels_list) > 1:
            for pixel_index in range(n_pixels):
                labels_for_pixel = [labels[pixel_index] for labels in labels_list]
                if len(set(labels_for_pixel)) > 1:
                    misclassified.add(pixel_index)

        for index, U in enumerate(U_matrices):
            thresholds = thresholds_list[index]
            for pixel_index in range(n_pixels):
                current_label = labels_list[index][pixel_index]
                membership_value = U[current_label, pixel_index]
                if membership_value < thresholds[current_label]:
                    misclassified.add(pixel_index)

        return sorted(list(misclassified))

    def _refine_misclassified_pixels(self, solutions, misclassified_pixels, U_matrices=None, labels_list=None):
        """ Étape 25-31 : Raffinement des pixels mal classés
            25: Pour chaque pixel extrait (xi) Faire
            26: Pour j = 1 to N3 Faire
            27: Calculer la fonction objectif J(j) i à l'aide de l'équation (III.11)
            28: Fin Pour
            29: Trouver j = argmin(J(j)i )
            30: Affecter le pixel xi à la classe j
            31: Fin Pour
        """
        if len(solutions) == 0:
            raise ValueError("Aucune solution pour raffinement")

        if labels_list is None or len(labels_list) == 0:
            labels_flat = np.argmax(U_matrices[0], axis=0).copy()
        else:
            labels_flat = labels_list[0].copy()

        image_flat = self.image.flatten()
        n_clusters = int(np.max(labels_flat)) + 1

        for pixel_idx in misclassified_pixels:
            x_i = float(image_flat[pixel_idx])

            best_j = None
            best_J = float("inf")

            for j in range(n_clusters):
                J_value = ThresholdCalculator.compute_objective_function(
                    x_i=x_i,
                    local_window=image_flat,
                    labels=labels_flat,
                    j=j,
                    beta=1.0,
                )

                if J_value < best_J:
                    best_J = J_value
                    best_j = j

            if best_j is not None:
                labels_flat[pixel_idx] = best_j

        return labels_flat.reshape(self.image.shape)


    def _labels_to_centers(self, labels_2d):
        n_clusters = int(np.max(labels_2d)) + 1
        centers = []

        for c in range(n_clusters):
            pixels = self.image[labels_2d == c]
            if len(pixels) > 0:
                centers.append(float(np.mean(pixels)))
            else:
                centers.append(0.0)

        return np.array(centers, dtype=float)
