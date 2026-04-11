import cv2
import numpy as np
import os
from algorithm import Algorithm
from calcul import Calcul
import time


if __name__ == "__main__":
    #TODO: Loop on all MRI
    image_path = "mri/0179_ni_slice_002.png"
    try:
        image = cv2.imread(image_path, 0)
        if image is None:
            raise FileNotFoundError(f"Image non trouvée: {image_path}")
    except Exception as e:
        print(f"Erreur: {e}")
        exit(1)
    
    print(f"Image chargée: {image.shape}")
    print(f"Niveaux de gris: [{image.min()}, {image.max()}]")
    
    model = Algorithm(image)
    
    N_CLUSTERS = 4 # nombre de classes pour la segmentation
    N_PARTICLES = 255 # nombre de particules dans la population
    N_ITERATIONS = 1 # nombre d'itérations pour l'optimisation
    start = time.perf_counter()
    centers, archive = model.segmentation(N_CLUSTERS, N_PARTICLES, N_ITERATIONS)
    end = time.perf_counter()
    print(f"Temps d'exécution: {end - start:.4f} seconds")
    print(f"Centres optimaux: {centers}")
    print(f"Solutions non dominées: {archive.size()}")
    
    best_solution, best_obj = archive.solutions[0], archive.objectives[0]
    print(f"Meilleure solution - J_IFCMS: {best_obj[0]:.2f}, J_edge: {best_obj[1]:.2f}")
    
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    results_dir = f"mri_results/{image_name}_classes_{N_CLUSTERS}_particles_{N_PARTICLES}"
    os.makedirs(results_dir, exist_ok=True)
    
    
    formulas = Calcul(image)
    U = formulas.compute_degree_membership(best_solution)
    labels = np.argmax(U, axis=0).reshape(image.shape).astype(np.uint8)
    gray_step = 255 / max(N_CLUSTERS - 1, 1)
    labels_gray = np.uint8(np.round(labels * gray_step))
    
    output_path = os.path.join(results_dir, "segmentation_result.png")
    cv2.imwrite(output_path, labels_gray ) 

    metadata_path = os.path.join(results_dir, f"segmentation_info.txt")
    with open(metadata_path, 'w') as f:
        f.write(f"Image source: {image_path}\n")
        f.write(f"Dimensions: {image.shape}\n")
        f.write(f"Nombre de classes: {N_CLUSTERS}\n")
        f.write(f"Nombre de particules: {N_PARTICLES}\n")
        f.write(f"Centres optimaux: {best_solution}\n")
        f.write(f"J_IFCMS: {best_obj[0]:.4f}\n")
        f.write(f"J_edge: {best_obj[1]:.4f}\n")
        f.write(f"Solutions non dominées: {archive.size()}\n")
        f.write(f"Temps d'exécution: {end - start:.4f} seconds\n")

    print("THE END")