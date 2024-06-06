import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Variables globales pour stocker les points d'image et leurs coordonnées GPS
image_points = []
gps_points = []

# Fonction de callback pour la sélection des points
def select_points(event, x, y, flags, param):
    global image_points
    if event == cv2.EVENT_LBUTTONDOWN:
        image_points.append((x, y))
        print(f"Point sélectionné: ({x}, {y})")


# Get the directory of the current file
curr_path = os.path.dirname(os.path.abspath(__file__))
# Replace backslashes with forward slashes
curr_path = curr_path.replace('\\', '/')
# Create the paths to the source images, results, and parameters
src_path = curr_path + "/images/"

# Charger l'image
image_path = src_path + 'undistorted-cam_metro.png'
image = cv2.imread(image_path)
image_copy = image.copy()

# Affichage de l'image et sélection des points
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', select_points)

print("Sélectionnez 4 points ou plus sur l'image en cliquant. Appuyez sur 'q' pour terminer la sélection.")
while True:
    cv2.imshow('Image', image_copy)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()

# Saisie des coordonnées GPS correspondantes
for i, point in enumerate(image_points):
    lat = float(input(f"Entrez la latitude du point {i+1} ({point}): "))
    lon = float(input(f"Entrez la longitude du point {i+1} ({point}): "))
    gps_points.append((lat, lon))

# Conversion en numpy arrays
image_points_np = np.array(image_points, dtype=np.float32)
gps_points_np = np.array(gps_points, dtype=np.float32)

# Calcul de l'homographie
H, status = cv2.findHomography(image_points_np, gps_points_np)

def transform_point(point, H):
    point_homog = np.array([point[0], point[1], 1], dtype=np.float32).reshape(-1, 1)
    transformed_point = np.dot(H, point_homog)
    transformed_point /= transformed_point[2]  # Normaliser les coordonnées homogènes
    return transformed_point[0], transformed_point[1]

# Fonction pour tester la transformation de points
def test_transformation():
    while True:
        # Afficher l'image
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title('Cliquez pour tester les coordonnées GPS, fermez la fenêtre pour terminer.')
        points = plt.ginput(1, timeout=-1)  # Timeout=-1 pour attendre indéfiniment un clic
        plt.close()
        
        if len(points) == 0:
            break

        point = points[0]
        print(point, "============================")
        gps_point = transform_point(point, H)
        print(f"Point image: {point} -> Coordonnées GPS: {gps_point}")

# Test de la transformation
test_transformation()
