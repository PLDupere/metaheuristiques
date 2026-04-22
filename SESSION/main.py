import cv2
import numpy as np
import os
import time
from algorithm import Algorithm
from PIL import Image
from helper import Helper


if __name__ == "__main__":

    IMAGES_DIR = os.getenv("IMAGES_DIR", "mri")
    IMAGES_RESULTS_DIR = os.getenv("IMAGES_RESULTS_DIR", "mri_results")
    N_MONTE_CARLO = int(os.getenv("N_MONTE_CARLO", 5))
    USE_IMPROVEMENT = os.getenv("USE_IMPROVEMENT", "True") == "True"
    N_CLUSTERS = int(os.getenv("N_CLUSTERS", 4))
    N_PARTICLES = int(os.getenv("N_PARTICLES", 1))
    N_ITERATIONS = int(os.getenv("N_ITERATIONS", 1))
    BACKGROUND_MASK = int(os.getenv("BACKGROUND_MASK", 1))

    for image_file in sorted(os.listdir(IMAGES_DIR)):

        if not image_file.lower().endswith((".png")):
            continue

        image_path = os.path.join(IMAGES_DIR, image_file)

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
                IMAGES_RESULTS_DIR,
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

            # Sauvegarde metadata
            Helper.save_to_csv(f'J_IFCMS_{image_file}', iteration, best_solution, best_obj[0], results_dir=IMAGES_RESULTS_DIR)
            Helper.save_to_csv(f'J_edge_{image_file}', iteration, best_solution, best_obj[1], results_dir=IMAGES_RESULTS_DIR)
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

print("THE END")