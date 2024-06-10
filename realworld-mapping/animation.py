import csv
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Paramètres
csv_path = 'C:/Users/Eliott/Desktop/Stage/object_positions.csv'
video_path = 'C:/Users/Eliott/Desktop/Stage/output1.mp4'

# Charger la vidéo pour obtenir les dimensions et le nombre de frames
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Erreur lors de l'ouverture de la vidéo")
    exit()
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.release()

# Lire les données du fichier CSV
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

# Préparer la figure pour l'animation
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, frame_width)
ax.set_ylim(frame_height, 0)  # Inverser l'axe y pour correspondre à l'orientation de l'image
scat = ax.scatter([], [], c='r', s=10)

def init():
    scat.set_offsets(np.zeros((0, 2)))
    return scat,

def update(frame_number):
    points = data.get(frame_number, [])
    centers = [(center_x, center_y) for _, center_x, center_y in points]
    centers_array = np.array(centers)
    scat.set_offsets(centers_array)
    return scat,

# Créer l'animation
ani = animation.FuncAnimation(fig, update, init_func=init, frames=frame_count, interval=1000/30, blit=True)

# Afficher l'animation
plt.show()
