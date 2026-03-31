import numpy as np
from .mahalanobis import MahalanobisDistance


class JIFCMS:

    @staticmethod
    def compute(data, centers, cov_matrices, membership_matrix, m=2.0):
    #Calcule la fonction objectif J_IFCMS selon l'équation (III.5)
        num_pixels = len(data)
        num_classes = len(centers)
        j_ifcms = 0.0

        for i in range(num_pixels):
            for j in range(num_classes):
                mahal_dist = MahalanobisDistance.compute(
                    data[i], centers[j], cov_matrices[j]
                )
                d_ij_squared = mahal_dist ** 2

                u_ij_m = membership_matrix[i, j] ** m
                j_ifcms += u_ij_m * d_ij_squared

        return j_ifcms
