import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score
from ultralytics import YOLO
import os

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

def yolo_detection(frame, model, confidence_threshold=0.5):
    results = model(frame)
    boxes = results[0].boxes.xyxy.cpu().numpy()  # Format: (x1, y1, x2, y2)
    confidences = results.boxes.conf.numpy()
    class_ids = results.boxes.cls.numpy().astype(int)
    
    indices = np.where(confidences >= confidence_threshold)[0]
    return indices, boxes, confidences, class_ids

def plot_metrics(metric_values, parameter_values, parameter_name, metric_name, filename):
    plt.plot(parameter_values, metric_values)
    plt.xlabel(parameter_name)
    plt.ylabel(metric_name)
    plt.title(f'{metric_name} vs {parameter_name}')
    plt.savefig(filename)
    plt.close()

# Fonction pour lire les annotations depuis un fichier .txt
def read_annotations(txt_file, img_width, img_height):
    boxes = []
    with open(txt_file, 'r') as file:
        for line in file.readlines():
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1]) * img_width
            y_center = float(parts[2]) * img_height
            width = float(parts[3]) * img_width
            height = float(parts[4]) * img_height
            x1 = x_center - width / 2
            y1 = y_center - height / 2
            x2 = x_center + width / 2
            y2 = y_center + height / 2
            boxes.append([x1, y1, x2, y2, class_id])
    return boxes

# Exemple de chemin vers le dataset
dataset_path = "/usr/src/ultralytics/videos/datasets/dataset4_mix/test"
images_path = os.path.join(dataset_path, "images")
labels_path = os.path.join(dataset_path, "labels")

# Paramètres de variation
brightness_values = [-50, 0, 50]
contrast_values = [0.5, 1.0, 1.5]
precision_scores = []
recall_scores = []

for brightness in brightness_values:
    for contrast in contrast_values:
        y_true = []
        y_pred = []
        
        for img_file in os.listdir(images_path):
            if img_file.endswith('.jpg') or img_file.endswith('.png'):
                img_path = os.path.join(images_path, img_file)
                label_path = os.path.join(labels_path, img_file.replace('.jpg', '.txt').replace('.png', '.txt'))
                
                frame = cv2.imread(img_path)
                img_height, img_width = frame.shape[:2]

                # Lire les annotations Ground Truth
                img_gt_boxes = read_annotations(label_path, img_width, img_height)

                # Ajuster la luminosité et le contraste
                frame = adjust_brightness(frame, brightness)
                frame = adjust_contrast(frame, contrast)

                # Détection YOLO
                indices, boxes, confidences, class_ids = yolo_detection(frame, model)

                # Ajouter les classes détectées à y_pred
                y_pred.extend([class_ids[i] for i in indices])

                # Ajouter les classes Ground Truth à y_true pour l'image actuelle
                y_true.extend([box[4] for box in img_gt_boxes])
        
        # Calculer les métriques de précision et de rappel
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        precision_scores.append(precision)
        recall_scores.append(recall)

# Visualiser les résultats
plot_metrics(precision_scores, brightness_values, "Brightness", "Precision", "precision_vs_brightness.png")
plot_metrics(recall_scores, contrast_values, "Contrast", "Recall", "recall_vs_contrast.png")

