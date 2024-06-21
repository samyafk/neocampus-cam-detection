import cv2 as cv
import numpy as np
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
    csv_name = sys.argv[3]

# Get the directory of the current file
curr_path = os.path.dirname(os.path.abspath(__file__))
parent_path = parent_directory = os.path.abspath(os.path.join(curr_path, os.pardir))
# Replace backslashes with forward slashes
curr_path = curr_path.replace('\\', '/')
parent_path = parent_path.replace('\\', '/')
# Create the paths to the source images, results, and parameters
setup_path = curr_path + "/setup-data/"
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
img_cam = cv.imread(setup_path + camera_img_name)

# Vérifier que les images ont été chargées correctement
if img_cam is None:
    print("Erreur lors du chargement des images")
    exit()


# Variables globales pour stocker les points d'image
image_points = []
gps_points = np.loadtxt(setup_path + csv_name, delimiter=',')
print(gps_points)

# Fonction de callback pour la sélection des points sur l'image source
def select_points_src(event, x, y, flags, param):
    global image_points
    if event == cv.EVENT_LBUTTONDOWN:
        image_points.append((x, y))
        print(f"Point source sélectionné: ({x}, {y})")

# Affichage des images et sélection des points
cv.namedWindow('Image Source')
cv.setMouseCallback('Image Source', select_points_src)

print("Sélectionnez 4 points ou plus sur chaque image en cliquant. Appuyez sur 'q' pour terminer la sélection.")
while True:
    cv.imshow('Image Source', img_cam)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or len(image_points) == len(gps_points):
        break

cv.destroyAllWindows()

# Vérifier que le nombre de points sélectionnés est le même pour les deux images
if len(image_points) != len(gps_points):
    print("Vous devez sélectionner {} points".format(len(gps_points)))
    exit()

# Conversion en numpy arrays
points_image_np = np.array(image_points, dtype=np.float32)
points_gps_np = np.array(gps_points, dtype=np.float32)

# Calcul de l'homographie
H, _ = cv.findHomography(points_image_np, points_gps_np)

# Save the homography matrix result for later use
pickle.dump(H, open( params_path + "homographyMatrix.pkl", "wb" ))

