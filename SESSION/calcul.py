import numpy as np
import cv2
from equations import (
    MahalanobisDistance,
    MembershipCalculator,
    CovarianceCalculator,
    JIFCMS,
    JEdge,
    ThresholdCalculator
)


class Calcul:
    def __init__(self, image):
        self.image = image.astype(np.float64)
        self.grad = cv2.Laplacian(self.image, cv2.CV_64F)
        self.local_img = cv2.blur(self.image, (3, 3))


    def compute_membership(self, centers, m=2.0):
        image_flat = self.image.flatten()
        membership_matrix_basic = self._compute_euclidienne_membership(image_flat, centers, m)

        covariance_matrices = CovarianceCalculator.compute_covariance(
            image_flat.reshape(-1, 1),
            centers,
            membership_matrix_basic,
            m
        )

        membership_matrix = MembershipCalculator.compute_membership_matrix(
            image_flat, centers, covariance_matrices, m
        )
        return membership_matrix.T, image_flat


    def _compute_euclidienne_membership(self, data, centers, m=2.0):
        #Méthode des c-moyennes floues
        num_pixels = len(data)
        num_classes = len(centers)
        membership_matrix = np.zeros((num_pixels, num_classes))

        for i in range(num_pixels):
            distances = np.zeros(num_classes)
            for j in range(num_classes):
                distances[j] = (data[i] - centers[j]) ** 2

            distances = np.maximum(distances, 1e-10)

            for j in range(num_classes):
                denominator = 0.0
                for k in range(num_classes):
                    denominator += (distances[j] / distances[k]) ** (2 / (m - 1))
                membership_matrix[i, j] = 1.0 / denominator

        return membership_matrix


    def compute_J_IFCMS(self, centers, m=2.0, lam=1.0):
        # Calcule la fonction objectif J_IFCMS selon l'équation (III.5)
        membership_matrix_T, image_flat = self.compute_membership(centers, m)
        membership_matrix = membership_matrix_T.T  # Remettre dans le bon format
        local_flat = self.local_img.flatten()
        covariance_matrices = self.compute_covariance_matrix(centers, m)

        j_intensity = JIFCMS.compute(
            image_flat.reshape(-1, 1),
            centers,
            covariance_matrices,
            membership_matrix,
            m
        )

        j_spatial = JIFCMS.compute(
            local_flat.reshape(-1, 1),
            centers,
            covariance_matrices,
            membership_matrix,
            m
        )
        return j_intensity + lam * j_spatial


    def compute_J_edge(self, centers, m=2.0):
        #Fonction objectif Edge utilisant les nouvelles classes selon l'équation (III.9)
        membership_matrix_T, _ = self.compute_membership(centers, m)
        membership_matrix = membership_matrix_T.T
        j_edge = JEdge.compute(self.image, membership_matrix)

        sigma_grad = float(np.var(self.grad))

        labels = np.argmax(membership_matrix, axis=1).reshape(self.image.shape)
        num_components, _ = cv2.connectedComponents(labels.astype(np.uint8))
        num_components = int(num_components)

        return sigma_grad + j_edge + float(num_components)


    def compute_covariance_matrix(self, centers, m=2.0):
        image_flat = self.image.flatten()
        membership_matrix_basic = self._compute_euclidienne_membership(image_flat, centers, m)

        covariance_matrices = CovarianceCalculator.compute_covariance(
            image_flat.reshape(-1, 1),
            centers,
            membership_matrix_basic,
            m
        )

        covariance_dict = {i: covariance_matrices[i] for i in range(len(covariance_matrices))}
        return covariance_dict


    def compute_degree_membership(self, centers, m=2.0):
        membership_matrix_T, _ = self.compute_membership(centers, m)
        return membership_matrix_T


    def compute_threshold_T(self, centers, U=None):
        # Calcule les seuils T_j pour chaque classe selon l"équation (III.10)
        if U is None:
            U, _ = self.compute_membership(centers)

        # U est dans le format (C x N) => (N x C)
        membership_matrix = U.T
        thresholds_array = ThresholdCalculator.compute_thresholds(membership_matrix)
        thresholds = {i: thresholds_array[i] for i in range(len(thresholds_array))}
        return thresholds


    def find_misclassified_pixels(self, solutions, U_matrices, labels_list, thresholds_list):
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

    def refine_misclassified_pixels(self, solutions, misclassified_pixels, U_matrices=None, labels_list=None):
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


    def labels_to_centers(self, labels_2d):
        n_clusters = int(np.max(labels_2d)) + 1
        centers = []

        for c in range(n_clusters):
            pixels = self.image[labels_2d == c]
            if len(pixels) > 0:
                centers.append(float(np.mean(pixels)))
            else:
                centers.append(0.0)

        return np.array(centers, dtype=float)