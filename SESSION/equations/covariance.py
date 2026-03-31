import numpy as np


class CovarianceCalculator:

    @staticmethod
    def compute_covariance(data, centers, membership_matrix, m=2.0):
        num_pixels, num_features = data.shape if data.ndim > 1 else (len(data), 1)
        num_classes = len(centers)
        cov_matrices = []

        for c in range(num_classes):
            weights = membership_matrix[:, c] ** m
            total_weight = np.sum(weights)

            if total_weight < 1e-10:
                cov_matrix = np.eye(num_features) # matrice identité
            else:
                weighted_sum = np.zeros((num_features, num_features))

                for i in range(num_pixels):
                    diff = data[i] - centers[c]
                    if num_features == 1: #dimension
                        diff = np.array([diff])
                        weighted_sum += weights[i] * np.outer(diff, diff)
                    else:
                        weighted_sum += weights[i] * np.outer(diff, diff)

                cov_matrix = weighted_sum / total_weight
                cov_matrix += 1e-6 * np.eye(num_features)

            cov_matrices.append(cov_matrix)

        return cov_matrices

