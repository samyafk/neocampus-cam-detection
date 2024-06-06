import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

# Charger les paramètres de calibration
params_path = "C:/Users/Eliott/Desktop/Stage/neocampus-cam-detection-main/cam-calibration/params/"
with open(params_path + "cameraMatrix.pkl", 'rb') as f:
    cameraMatrix = pickle.load(f)
with open(params_path + "dist.pkl", 'rb') as f:
    dist = pickle.load(f)

# Charger les images à undistorter
image_path_src = "C:/Users/Eliott/Desktop/Stage/test_homographie/image.jpg"
image_path_tgt = "C:/Users/Eliott/Desktop/Stage/test_homographie/map.jpg"
img_src = cv.imread(image_path_src)
img_tgt = cv.imread(image_path_tgt)

# Vérifier que les images ont été chargées correctement
if img_src is None or img_tgt is None:
    print("Erreur lors du chargement des images")
    exit()

# Undistortion des images
def undistort_image(img, cameraMatrix, dist):
    h, w = img.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))
    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

dst_src = undistort_image(img_src, cameraMatrix, dist)
dst_tgt = undistort_image(img_tgt, cameraMatrix, dist)

# Variables globales pour stocker les points d'image
points_src = []
points_tgt = []

# Fonction de callback pour la sélection des points sur l'image source
def select_points_src(event, x, y, flags, param):
    global points_src
    if event == cv.EVENT_LBUTTONDOWN:
        points_src.append((x, y))
        print(f"Point source sélectionné: ({x}, {y})")

# Fonction de callback pour la sélection des points sur l'image cible
def select_points_tgt(event, x, y, flags, param):
    global points_tgt
    if event == cv.EVENT_LBUTTONDOWN:
        points_tgt.append((x, y))
        print(f"Point cible sélectionné: ({x}, {y})")

# Affichage des images et sélection des points
cv.namedWindow('Image Source')
cv.setMouseCallback('Image Source', select_points_src)
cv.namedWindow('Image Cible')
cv.setMouseCallback('Image Cible', select_points_tgt)

print("Sélectionnez 4 points ou plus sur chaque image en cliquant. Appuyez sur 'q' pour terminer la sélection.")
while True:
    cv.imshow('Image Source', dst_src)
    cv.imshow('Image Cible', dst_tgt)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv.destroyAllWindows()

# Vérifier que le nombre de points sélectionnés est le même pour les deux images
if len(points_src) != len(points_tgt):
    print("Le nombre de points sélectionnés dans chaque image doit être le même.")
    exit()

# Conversion en numpy arrays
points_src_np = np.array(points_src, dtype=np.float32)
points_tgt_np = np.array(points_tgt, dtype=np.float32)

# Calcul de l'homographie
H, status = cv.findHomography(points_src_np, points_tgt_np)

def transform_point(point, H):
    point_homog = np.array([point[0], point[1], 1], dtype=np.float32).reshape(-1, 1)
    transformed_point = np.dot(H, point_homog)
    transformed_point /= transformed_point[2]  # Normaliser les coordonnées homogènes
    return transformed_point[0], transformed_point[1]

# Fonction pour tester la transformation de points
def test_transformation():
    while True:
        # Afficher l'image source
        plt.figure(figsize=(12, 6))
        
        # Afficher l'image source
        plt.subplot(1, 2, 1)
        plt.imshow(cv.cvtColor(dst_src, cv.COLOR_BGR2RGB))
        plt.title('Cliquez pour sélectionner un point (Image Source)')
        
        # Afficher l'image cible
        plt.subplot(1, 2, 2)
        plt.imshow(cv.cvtColor(dst_tgt, cv.COLOR_BGR2RGB))
        plt.title('Point transformé (Image Cible)')
        
        # Sélectionner un point sur l'image source
        points = plt.ginput(1, timeout=-1)  # Timeout=-1 pour attendre indéfiniment un clic
        plt.close()
        
        if len(points) == 0:
            break

        point = points[0]
        transformed_point = transform_point(point, H)

        # Afficher le point transformé sur l'image cible
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.imshow(cv.cvtColor(dst_src, cv.COLOR_BGR2RGB))
        plt.title('Image Source')
        plt.scatter(point[0], point[1], color='red')
        
        plt.subplot(1, 2, 2)
        plt.imshow(cv.cvtColor(dst_tgt, cv.COLOR_BGR2RGB))
        plt.title('Image Cible')
        plt.scatter(transformed_point[0], transformed_point[1], color='red')
        
        plt.show()

# Test de la transformation
test_transformation()
