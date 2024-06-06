import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
import csv
from itertools import cycle

# Charger les paramètres de calibration
params_path = "C:/Users/Eliott/Desktop/Stage/neocampus-cam-detection-main/cam-calibration/params/"
with open(params_path + "cameraMatrix.pkl", 'rb') as f:
    cameraMatrix = pickle.load(f)
with open(params_path + "dist.pkl", 'rb') as f:
    dist = pickle.load(f)

# Charger les images à undistorter
image_path_src = "C:/Users/Eliott/Desktop/Stage/test_homographie/image.jpg"
image_path_tgt = "C:/Users/Eliott/Desktop/Stage/test_homographie/map2.jpg"
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
dst_tgt = img_tgt

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

# Lire les données du fichier CSV
csv_path = "C:/Users/Eliott/Desktop/Stage/object_positions.csv"
data = {}
with open(csv_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        frame_number = int(row['Frame'])
        object_id = row['Object_ID']
        center_x = float(row['Center_X'])
        center_y = float(row['Center_Y'])
        if frame_number not in data:
            data[frame_number] = []
        data[frame_number].append((object_id, center_x, center_y))

# Générer une couleur unique pour chaque classe
unique_classes = set(obj_id for frame in data.values() for obj_id, _, _ in frame)
colors = plt.cm.get_cmap('tab20', len(unique_classes)).colors  # Utiliser une palette de couleurs avec suffisamment de couleurs
class_colors = {cls: colors[i] for i, cls in enumerate(unique_classes)}

# Préparer la figure pour l'animation
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, dst_tgt.shape[1])
ax.set_ylim(dst_tgt.shape[0], 0)  # Inverser l'axe y pour correspondre à l'orientation de l'image
scatters = {cls: ax.scatter([], [], c=[color], label=cls, s=10) for cls, color in class_colors.items()}

# Fonction d'initialisation pour l'animation
def init():
    for scatter in scatters.values():
        scatter.set_offsets(np.zeros((0, 2)))
    return list(scatters.values())

# Fonction de mise à jour pour l'animation
def update(frame_number):
    for cls in class_colors:
        points = [(center_x, center_y) for obj_id, center_x, center_y in data.get(frame_number, []) if obj_id == cls]
        if points:
            transformed_points = [transform_point(point, H) for point in points]
            centers_array = np.array(transformed_points)
        else:
            centers_array = np.zeros((0, 2))
        scatters[cls].set_offsets(centers_array)
    return list(scatters.values())

# Créer l'animation à 10 images par seconde (intervalle de 100 ms)
ani = animation.FuncAnimation(fig, update, init_func=init, frames=max(data.keys())+1, interval=100, blit=True)

# Afficher l'animation avec légende
ax.legend()
plt.imshow(cv.cvtColor(dst_tgt, cv.COLOR_BGR2RGB))
plt.show()
