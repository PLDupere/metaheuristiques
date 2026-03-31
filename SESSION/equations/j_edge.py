import numpy as np


class JEdge:

    @staticmethod
    def compute(image, membership_matrix):
        #Calcule J_edge selon l' Equation (III.9)
        hard_membership = np.argmax(membership_matrix, axis=1)
        height, width = image.shape
        num_classes = membership_matrix.shape[1]
        segmentation = hard_membership.reshape(height, width)
        variances = []

        for c in range(num_classes):
            class_pixels = image[segmentation == c]

            if class_pixels.size > 0:
                variances.append(np.var(class_pixels))
            else:
                variances.append(0.0)

        max_variance = np.max(variances)
        gx, gy = np.gradient(image)
        gradient_magnitude = np.sqrt(gx**2 + gy**2)

        sigma_gamma = np.var(gradient_magnitude)

        changes_h = segmentation[:, 1:] != segmentation[:, :-1]
        changes_v = segmentation[1:, :] != segmentation[:-1, :]
        card_omega = np.sum(changes_h) + np.sum(changes_v)

        return sigma_gamma + max_variance + card_omega
