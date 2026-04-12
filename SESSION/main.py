import cv2
import numpy as np
import os
import time
from algorithm import Algorithm
from PIL import Image
from helper import Helper
from skimage.exposure import match_histograms


if __name__ == "__main__":

    images_dir = "mri"
    N_MONTE_CARLO = 5
    USE_IMPROVEMENT = False ### TODO:
    N_CLUSTERS = 6
    N_PARTICLES = 1
    N_ITERATIONS = 1
    BACKGROUND_MASK = 5

    for image_file in sorted(os.listdir(images_dir)):

        if not image_file.lower().endswith((".png")):
            continue

        image_path = os.path.join(images_dir, image_file)

        try:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise FileNotFoundError(f"Image non trouvée: {image_path}")
            background_mask = image < BACKGROUND_MASK
            image_masked = image.copy()
            image_masked[background_mask] = 0 # 0 = Noir
        except Exception as e:
            print(f"Erreur: {e}")
            continue

        print(f"\nTraitement image: {image_file}")
        print(f"Dimensions: {image.shape}")
        print(f"Niveaux de gris: [{image.min()}, {image.max()}]")

        image_name = os.path.splitext(image_file)[0]

        for iteration in range(1, N_MONTE_CARLO + 1):

            print(f"Monte Carlo {iteration}/{N_MONTE_CARLO}")
            model = Algorithm(image_masked.copy(), background_threshold=BACKGROUND_MASK)
            start = time.perf_counter()
            centers_reconstructed, archive, labels_final = model.segmentation(
                USE_IMPROVEMENT,
                N_CLUSTERS,
                N_PARTICLES,
                N_ITERATIONS
            )
            end = time.perf_counter()

            centers_reconstructed = np.array(centers_reconstructed).copy()
            labels_final = labels_final.copy()
            best_solution, best_obj = archive.solutions[0], archive.objectives[0]
            results_dir = os.path.join(
                "mri_results",
                image_name,
                f"iteration_{iteration}"
            )

            os.makedirs(results_dir, exist_ok=True)
            output_path = os.path.join(
                results_dir,
                f"segmentation_iteration_{iteration}.png"
            )
            labels = labels_final.astype(np.uint8)
            gray_step = 254 / max(N_CLUSTERS - 1, 1)
            labels_gray = np.round(labels * gray_step).astype(np.uint8)
            labels_gray = np.where(background_mask, 0, labels_gray)
            Image.fromarray(labels_gray, mode='L').save(output_path)

            # Reconstruction de l'image segmentée pour visualiser les centres
            # output_reconstructed = os.path.join(
            #     results_dir,
            #     f"segmentation_reconstructed_iteration_{iteration}.png"
            # )
            # reconstructed = centers_reconstructed[labels].astype(np.uint8)
            # reconstructed = match_histograms(reconstructed, image).astype(np.uint8)
            # reconstructed[background_mask] = 0
            # Image.fromarray(reconstructed, mode='L').save(output_reconstructed)

            # Sauvegarde metadata
            Helper.save_to_csv(f'J_IFCMS_{image_file}', iteration, best_solution, best_obj[0])
            Helper.save_to_csv(f'J_edge_{image_file}', iteration, best_solution, best_obj[1])
            metadata_path = os.path.join(
                results_dir,
                f"segmentation_info_iteration_{iteration}.txt"
            )

            with open(metadata_path, 'w') as f:
                f.write(f"Image source: {image_path}\n")
                f.write(f"Iteration: {iteration}\n")
                f.write(f"Dimensions: {image.shape}\n")
                f.write(f"Nombre de classes: {N_CLUSTERS}\n")
                f.write(f"Nombre de particules: {N_PARTICLES}\n")
                f.write(f"Centres optimaux: {best_solution}\n")
                f.write(f"J_IFCMS: {best_obj[0]:.4f}\n")
                f.write(f"J_edge: {best_obj[1]:.4f}\n")
                f.write(f"Solutions non dominées: {archive.size()}\n")
                f.write(f"Temps d'exécution: {end - start:.4f} seconds\n")

        # Helper().save_stats_from_csv()
        # Helper.plot_cost_boxplot_overall()
        # Helper.plot_costs_sorted_overall()
print("THE END")