## Structure du Projet

- **discretisation.py** : Contient la classe `Discretisation` qui implémente l'algorithme de discrétisation des couleurs pour les images. Elle inclut des méthodes pour traiter les images et appliquer la technique de discrétisation.
  
- **main.py** : Le point d'entrée principal de l'application. Il gère le chargement des images depuis le répertoire `in`, permet l'interaction avec l'utilisateur pour sélectionner les images, et sauvegarde les images discrétisées dans le répertoire `out`.

- **in/** : Ce répertoire est destiné à contenir les images d'entrée qui seront traitées par l'application.

- **out/** : Ce répertoire est destiné à stocker les images de sortie après leur traitement et discrétisation.

## Utilisation

1. Placez vos images d'entrée dans le répertoire `in`.
2. Exécutez le script `main.py` pour démarrer l'application.
3. Suivez les instructions pour sélectionner une image et spécifier le nombre de couleurs pour la discrétisation.
4. Les images traitées seront sauvegardées dans le répertoire `out`.

## Prérequis

- Python 3.13.11
- Bibliothèque Pillow (pip install Pillow)


## Création d'un environnement virtuel

Pour isoler les dépendances de votre projet, il est recommandé de créer un environnement virtuel.

1. Créez un environnement virtuel nommé `.venv` :
   ```
   python3 -m venv .venv
   ```

2. Activez l'environnement virtuel :
   - Sur Linux/Mac :
     ```
     source .venv/bin/activate
     ```
   - Sur Windows :
     ```
     .env\Scripts\activate
     ```

3. Installez les dépendances nécessaires dans l'environnement virtuel :
   ```
   pip install -r requirements.txt
   ```

4. Pour désactiver l'environnement virtuel, utilisez la commande suivante :
   ```
   deactivate
   ```
