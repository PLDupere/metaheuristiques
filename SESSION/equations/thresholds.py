import numpy as np


class ThresholdCalculator:

    @staticmethod
    def compute_thresholds(membership_matrix):
        # Calcule les seuils T_j pour chaque classe selon l"équation (III.10)
        num_pixels, num_classes = membership_matrix.shape
        thresholds = np.zeros(num_classes)

        for j in range(num_classes):
            memberships_j = membership_matrix[:, j]
            average = np.mean(memberships_j)
            sigma = np.std(memberships_j)
            thresholds[j] = average - sigma

        return thresholds


    @staticmethod
    def compute_objective_function(x_i, local_window, labels, j, beta=1.0):
        # Calcule J_i^(j) selon l'équation (III.11)
        classes = np.unique(labels)
        N_j = np.sum(labels == j)

        if N_j == 0:
            return np.inf

        mu_j = np.mean(local_window[labels == j])
        term1 = ((x_i - mu_j) ** 2) / (beta * N_j)

        term2 = 0
        for k in classes:
            if k != j:
                pixels_k = local_window[labels == k]
                if len(pixels_k) > 0:
                    sigma_k = np.var(pixels_k)
                    term2 += sigma_k

        return term1 + term2
