import numpy as np
from calcul import Calcul
from archive import ArchivePareto
from equations.thresholds import ThresholdCalculator
from sklearn.cluster import KMeans


class Particle:
    def __init__(self, n_clusters, min_val, max_val, k_means):
        if k_means:
            # min_val == images
            values = min_val.reshape(-1, 1)
            kmeans = KMeans(
                n_clusters=n_clusters,
                init="k-means++",
                n_init=10
            )
            kmeans.fit(values)
            self.position = kmeans.cluster_centers_.flatten().astype(float)
        else:
            # Ancienne initialisation : aléatoire
            self.position = np.random.uniform(min_val, max_val, n_clusters)

        self.position = self.position.astype(float)
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
    def __init__(self,image, background_threshold=1):
        self.image = image
        self.calcul = Calcul(image, background_threshold)

    def segmentation(self, use_improvement=True, n_clusters=3, n_particles=20, n_iter=10, 
                        w=0.7, c1=1.5, c2=1.5):

        # Étape 1 : Initialiser aléatoirement les positions des particules
        min_val = np.min(self.image)
        max_val = np.max(self.image)

        if use_improvement:
            # Nouvelle initialisation : uniforme
            particles = [
                Particle(n_clusters, self.image, max_val, k_means=True)
                for _ in range(n_particles)
            ]
        else:
            # Ancienne initialisation : aléatoire
            particles = [
                Particle(n_clusters, min_val, max_val, k_means=False)
                for _ in range(n_particles)
            ]

        # Étape 5 : Sauvegarder les solutions non dominées dans l’archive
        archive = ArchivePareto(max_size=100)

        for p in particles:
            # Étape 3 : Calculer les fonctions objectifs en utilisant les équation (III.5 et III.9)
            J_ifcms = self.calcul.compute_J_IFCMS(p.position)
            J_edge = self.calcul.compute_J_edge(p.position)
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
                Select_leader = archive.select_russian_roulette()
                
                if Select_leader is None:
                    Select_leader = p.best_position
                
                # Étape 10 : Mettre à jour les vitesses des particules en utilisant l’équation (III.3)
                rand1, rand2 = np.random.rand(2)
                p.velocity = (
                    w * p.velocity
                    + c1 * rand1 * (p.best_position - p.position)
                    + c2 * rand2 * (Select_leader - p.position)
                )
                
                # Étape 11 : Mettre à jour les positions des particules (centres des classes) en utilisant l’équation (III.4)
                p.position += p.velocity
                
                # Étape 12 : Maintenir les positions des particules dans l’espace de recherche
                p.position = np.clip(p.position, min_val, max_val)
                # Si sort du domaine, multiplier la vitesse par -1
                out_of_bounds = (p.position < min_val) | (p.position > max_val)
                p.velocity[out_of_bounds] *= -1
                
                # Étape 13 : Calculer les fonctions objectifs en utilisant les équations (III.5 et III.9)
                J_ifcms = self.calcul.compute_J_IFCMS(p.position)
                J_edge = self.calcul.compute_J_edge(p.position)
                objectives = [J_ifcms, J_edge]
                
                # Étape 14 : Mettre à jour la mémoire des particules
                p.update_best(objectives)
            # Étape 15 : Fin Pour
            # Étape 16 : Mettre à jour le contenu de l’archive
            for p in particles:
                J_ifcms = self.calcul.compute_J_IFCMS(p.position)
                J_edge = self.calcul.compute_J_edge(p.position)
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
        sorted_solutions = []

        # Étape 19 : Calculer les degrés d’appartenance en utilisant l’équation
        for solution in solutions:
            U = self.calcul.compute_degree_membership(solution)
            U_matrices.append(U)

        # Étape 20 : Trier les centres de classes pour que chaque classe ait le même label
        for solution in solutions:
            sorted_solution = np.sort(solution)
            sorted_solutions.append(sorted_solution)

        # Étape 21 : Déterminer la segmentation d’image en utilisant le principe du maximum
        for U in U_matrices:
            labels = np.argmax(U, axis=0).reshape(self.image.shape).astype(int)
            labels_list.append(labels.flatten())
        
        # for solution in solutions:
        #     # Étape 20 : Trier les centres
        #     # Étape 19 : Calculer les degrés d’appartenance (II.12)
        #     U = self.calcul.compute_degree_membership(solution)
        #     # Étape 21 : Déterminer la segmentation d’image en utilisant le principe du maximum de l’appartenance
        #     labels = np.argmax(U, axis=0).reshape(self.image.shape).astype(int)
        #     U_matrices.append(U)
        #     labels_list.append(labels.flatten())
        
        # Étape III.3.4.1 : Détection des pixels mal classés
        # Étape 22 :  Calculer pour chaque classe le seuil T en utilisant l’équation (III.10)
        thresholds_list = []
        for U in U_matrices:
            thresholds = ThresholdCalculator.compute_thresholds(U.T)
            thresholds_list.append(thresholds)
        # Étape 23 : Fin Pour
        # Étape 24 : Déterminer l’ensemble des pixels représentent l'ensemble des pixels potentiellement mal classés
        misclassified_pixels = self.calcul.find_misclassified_pixels(
            solutions, U_matrices, labels_list, thresholds_list
        )

        # Étape III.3.4.2 : Reclassification des pixels mal classés
        # Étape 25-31 : Raffinement des pixels mal classés
        if len(misclassified_pixels) > 0:
            refined_labels = self.calcul.refine_misclassified_pixels(
                solutions, misclassified_pixels, U_matrices, labels_list
            )
            best_solution = self.calcul.labels_to_centers(refined_labels.reshape(self.image.shape))
        else:
            refined_labels = labels_list[0].reshape(self.image.shape)
            best_solution = solutions[0]

        return best_solution, archive, refined_labels






