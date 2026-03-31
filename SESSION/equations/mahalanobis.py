import numpy as np


class MahalanobisDistance:

    @staticmethod
    def compute(x, center, cov_matrix):
        # Calcule la distance de Mahalanobis equation III.6 (voir formule II.15 pour comprendre)
        diff = x - center

        if np.isscalar(diff):
            variance = cov_matrix[0, 0] if cov_matrix.size > 0 else 1.0
            if variance < 1e-10:
                variance = 1e-10
            mahal_dist = (diff ** 2) / variance
            return max(mahal_dist, 1e-10)

        try:
            inv_cov = np.linalg.inv(cov_matrix + 1e-6 * np.eye(cov_matrix.shape[0]))
            mahal_dist = diff.T @ inv_cov @ diff
        except (np.linalg.LinAlgError, ValueError):
            mahal_dist = np.sum(diff ** 2)

        return max(mahal_dist, 1e-10)