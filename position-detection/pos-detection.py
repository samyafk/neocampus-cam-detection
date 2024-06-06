import cv2 as cv
import numpy as np
import pickle
import matplotlib.pyplot as plt
import os

# Charger les paramètres de calibration
params_path = "C:/Users/Eliott/Desktop/Stage/neocampus-cam-detection-main/cam-calibration/params/"  # Remplacer par le chemin correct
with open(params_path + "cameraMatrix.pkl", 'rb') as f:
    cameraMatrix = pickle.load(f)
with open(params_path + "dist.pkl", 'rb') as f:
    dist = pickle.load(f)

# Charger l'image à undistorter
image_path = "C:/Users/Eliott/Desktop/Stage/test_homographie/image.jpg"  # Remplacer par le chemin correct
img = cv.imread(image_path)

# Vérifier que l'image a été chargée correctement
if img is None:
    print(f"Erreur lors du chargement de l'image à partir de {image_path}")
    exit()

# Undistortion de l'image
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# Recadrer l'image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

# Sauvegarder ou afficher l'image undistorted
undistorted_image_path = "C:/Users/Eliott/Desktop/Stage/test_homographie/undist_image.jpg"  # Remplacer par le chemin correct
cv.imwrite(undistorted_image_path, dst)

# Variables globales pour stocker les points d'image et leurs coordonnées GPS
image_points = []
gps_points = []

# Fonction de callback pour la sélection des points
def select_points(event, x, y, flags, param):
    global image_points
    if event == cv.EVENT_LBUTTONDOWN:
        image_points.append((x, y))
        print(f"Point sélectionné: ({x}, {y})")

# Charger l'image
image_path = 'C:/Users/Eliott/Desktop/Stage/test_homographie/image.jpg'
image = cv2.imread(image_path)
image_copy = image.copy()

# Affichage de l'image et sélection des points
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', select_points)

print("Sélectionnez 4 points ou plus sur l'image en cliquant. Appuyez sur 'q' pour terminer la sélection.")
while True:
    cv.imshow('Undistorted Image', dst)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv.destroyAllWindows()

# Saisie des coordonnées GPS correspondantes
for i, point in enumerate(image_points):
    lat = float(input(f"Entrez la latitude du point {i+1} ({point}): "))
    lon = float(input(f"Entrez la longitude du point {i+1} ({point}): "))
    gps_points.append((lat, lon))

# Conversion en numpy arrays
image_points_np = np.array(image_points, dtype=np.float32)
gps_points_np = np.array(gps_points, dtype=np.float32)

# Calcul de l'homographie
H, status = cv.findHomography(image_points_np, gps_points_np)

def transform_point(point, H):
    point_homog = np.array([point[0], point[1], 1], dtype=np.float32).reshape(-1, 1)
    transformed_point = np.dot(H, point_homog)
    transformed_point /= transformed_point[2]  # Normaliser les coordonnées homogènes
    return transformed_point[0], transformed_point[1]

# Fonction pour tester la transformation de points
def test_transformation():
    while True:
        # Afficher l'image
        plt.imshow(cv.cvtColor(dst, cv.COLOR_BGR2RGB))
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
