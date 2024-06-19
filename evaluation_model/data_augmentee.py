import cv2
import os
from ultralytics import YOLO

# Charger le modèle YOLOv8
model = YOLO('/usr/src/ultralytics/videos/trains/train_100_data_mix/train33/weights/best.pt')

def adjust_brightness(frame, value):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)
    final_hsv = cv2.merge((h, s, v))
    frame_bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return frame_bright

def adjust_contrast(frame, alpha):
    frame_contrast = cv2.convertScaleAbs(frame, alpha=alpha, beta=0)
    return frame_contrast

# Chemins de base
dataset_path = "/usr/src/ultralytics/videos/datasets/dataset4_mix/test"
images_path = os.path.join(dataset_path, "images")
labels_path = os.path.join(dataset_path, "labels")

# Créer des dossiers pour les images modifiées
output_base_path = "/usr/src/ultralytics/videos/datasets/data_modified"
brightness_values = [-50, 0, 50]
contrast_values = [0.5, 1.0, 1.5]

for brightness in brightness_values:
    for contrast in contrast_values:
        output_folder = f"brightness_{brightness}_contrast_{contrast}"
        output_path = os.path.join(output_base_path, output_folder, "images")
        os.makedirs(output_path, exist_ok=True)
        
        for img_file in os.listdir(images_path):
            if img_file.endswith('.jpg') or img_file.endswith('.png'):
                img_path = os.path.join(images_path, img_file)
                frame = cv2.imread(img_path)

                # Ajuster la luminosité et le contraste
                frame = adjust_brightness(frame, brightness)
                frame = adjust_contrast(frame, contrast)

                # Sauvegarder l'image modifiée
                output_img_path = os.path.join(output_path, img_file)
                cv2.imwrite(output_img_path, frame)

        # Copier les fichiers de labels correspondants
        output_label_path = os.path.join(output_base_path, output_folder, "labels")
        os.makedirs(output_label_path, exist_ok=True)
        for label_file in os.listdir(labels_path):
            label_src = os.path.join(labels_path, label_file)
            label_dst = os.path.join(output_label_path, label_file)
            os.system(f"cp {label_src} {label_dst}")
