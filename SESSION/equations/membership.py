import numpy as np
from .mahalanobis import MahalanobisDistance


class MembershipCalculator:

    @staticmethod
    def compute_membership(pixel, centers, cov_matrices, m=2.0):
        # Calcule l'appartenance floue d'un pixel à chaque classe equation III.7 (voir II.15 pour comprendre)
        num_classes = len(centers)
        memberships = np.zeros(num_classes)
        distances = np.zeros(num_classes)
        for i in range(num_classes):
            distances[i] = MahalanobisDistance.compute(pixel, centers[i], cov_matrices[i])

        distances = np.maximum(distances, 1e-10)
        for i in range(num_classes):
            denominator = 0.0
            for j in range(num_classes):
                denominator += (distances[i] / distances[j]) ** (2 / (m - 1))
            memberships[i] = 1.0 / denominator

        return memberships


    @staticmethod
    def compute_membership_matrix(data, centers, cov_matrices, m=2.0):
        num_pixels = len(data)
        num_classes = len(centers)
        membership_matrix = np.zeros((num_pixels, num_classes))

        for i in range(num_pixels):
            membership_matrix[i] = MembershipCalculator.compute_membership(
                data[i], centers, cov_matrices, m
            )

        return membership_matrix