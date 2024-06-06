import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import sys

# Check if the number of arguments is correct
if len(sys.argv) != 4:
    print("Please check the README for more information on the usage of the Homography script.")
    sys.exit()
else:
    camera_name = sys.argv[1]
    camera_img_name = sys.argv[2]
    map_img_name = sys.argv[3]

# Get the directory of the current file
curr_path = os.path.dirname(os.path.abspath(__file__))
parent_path = parent_directory = os.path.abspath(os.path.join(curr_path, os.pardir))
# Replace backslashes with forward slashes
curr_path = curr_path.replace('\\', '/')
parent_path = parent_path.replace('\\', '/')
# Create the paths to the source images, results, and parameters
images_path = curr_path + "/images/"
params_path = curr_path + "/params-" + camera_name + "/"
calib_params_path = parent_path + "/cam-calibration/params-" + camera_name + "/"
print(parent_path)


# Charger les paramètres de calibration
with open(calib_params_path + "cameraMatrix.pkl", 'rb') as f:
    cameraMatrix = pickle.load(f)
with open(calib_params_path + "dist.pkl", 'rb') as f:
    dist = pickle.load(f)
    
# Check if directory exists, if not, create it
if not os.path.exists(params_path):
    os.makedirs(params_path)

# Load images
img_cam = cv.imread(images_path + camera_img_name)
img_map = cv.imread(images_path + map_img_name)

# Vérifier que les images ont été chargées correctement
if img_cam is None or img_map is None:
    print("Erreur lors du chargement des images")
    exit()


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
    cv.imshow('Image Source', img_cam)
    cv.imshow('Image Cible', img_map)
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
H, _ = cv.findHomography(points_src_np, points_tgt_np)

# Save the homography matrix result for later use
pickle.dump(H, open( params_path + "homographyMatrix.pkl", "wb" ))

