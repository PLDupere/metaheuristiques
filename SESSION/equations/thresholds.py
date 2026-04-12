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
    def compute_objective_function(x_i, image, labels, row, col, j):
        #Implémentation fidèle de l'équation (III.11)
        row_start_5 = max(0, row - 2)
        row_end_5 = min(image.shape[0], row + 3)
        col_start_5 = max(0, col - 2)
        col_end_5 = min(image.shape[1], col + 3)

        local_window_5x5 = image[row_start_5:row_end_5, col_start_5:col_end_5]
        labels_5x5 = labels[row_start_5:row_end_5, col_start_5:col_end_5]

        row_start_3 = max(0, row - 1)
        row_end_3 = min(image.shape[0], row + 2)
        col_start_3 = max(0, col - 1)
        col_end_3 = min(image.shape[1], col + 2)
        labels_3x3 = labels[row_start_3:row_end_3, col_start_3:col_end_3]

        classes_3x3 = np.unique(labels_3x3)
        # Nlabel = len(classes_3x3)
        pixels_j = local_window_5x5[labels_5x5 == j]
        N_j = len(pixels_j)

        if N_j == 0:
            return np.inf

        pixels_j_with_xi = np.append(pixels_j, x_i)
        mu_j = np.mean(pixels_j_with_xi)
        sigma_j = np.var(pixels_j_with_xi)
        term1 = -sigma_j
        term2 = np.abs(x_i - mu_j) / (N_j + 1)
        term3 = 0
        for k in classes_3x3:
            if k != j:
                pixels_k = local_window_5x5[labels_5x5 == k]
                if len(pixels_k) > 0:
                    sigma_k = np.var(pixels_k)
                    term3 += sigma_k

        return term1 + term2 + term3
