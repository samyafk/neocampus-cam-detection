import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
import csv

model_path = '/usr/src/ultralytics/runs/detect/train7/weights/best.pt'
video_path = '/usr/src/ultralytics/videos/output1.mp4'
output_csv_path = '/usr/src/ultralytics/videos/object_positions.csv'

model = YOLO(model_path)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erreur lors de l'ouverture de la vidéo")
    exit()

fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

header = ['Frame', 'Object_ID', 'Center_X', 'Center_Y']

with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    
    for frame_number in range(frame_count):
        ret, img = cap.read()
        if not ret:
            break
        
        results = model(img)

        boxes = results[0].boxes

      
        for box in boxes:
            xmin, ymin, xmax, ymax = box.xyxy[0].cpu().numpy()
            center_x = (xmin + xmax) / 2
            center_y = ymin
            object_id = model.names[int(box.cls.cpu().numpy())]  # Obtenir l'identifiant de l'objet

           
            writer.writerow([frame_number, object_id, center_x, center_y])

cap.release()

print(f"Les positions des objets détectés ont été sauvegardées dans {output_csv_path}")
