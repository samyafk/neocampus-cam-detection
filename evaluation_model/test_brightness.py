import os
from ultralytics import YOLO

# Charger le modèle YOLOv8
model = YOLO('/usr/src/ultralytics/videos/trains/train_100_data_mix/train33/weights/best.pt')

# Chemin de base pour les images modifiées
output_base_path = "/usr/src/ultralytics/videos/datasets/data_modified"
brightness_values = [-50, 0, 50]
contrast_values = [0.5, 1.0, 1.5]

results = {}

for brightness in brightness_values:
    for contrast in contrast_values:
        output_folder = f"brightness_{brightness}_contrast_{contrast}"
        dataset_path = os.path.join(output_base_path, output_folder)
        
        # Évaluer le modèle
        result = model.val(data=dataset_path, split='images')
        results[(brightness, contrast)] = result

# Afficher les résultats
for (brightness, contrast), result in results.items():
    print(f"Brightness: {brightness}, Contrast: {contrast}")
    print(result)
