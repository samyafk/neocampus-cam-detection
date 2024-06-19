import os
import yaml


output_base_path = "/usr/src/ultralytics/videos/datasets/data_modified"
brightness_values = [-50, 0, 50]
contrast_values = [0.5, 1.0, 1.5]
# Créer les fichiers YAML de configuration
def create_yaml_files(base_path, brightness_values, contrast_values):
    for brightness in brightness_values:
        for contrast in contrast_values:
            output_folder = f"brightness_{brightness}_contrast_{contrast}"
            dataset_path = os.path.join(base_path, output_folder)
            
            yaml_content = {
                'path': dataset_path,
                'train': 'images',  # Assuming we use the 'images' folder for validation as well
                'val': 'images',
                'test': 'images',
                'names': {0: 'class_name'}  # Replace with actual class names
            }
            
            yaml_file = os.path.join(dataset_path, f"{output_folder}.yaml")
            with open(yaml_file, 'w') as f:
                yaml.dump(yaml_content, f)

# Créer les fichiers YAML pour chaque ensemble d'images modifiées
create_yaml_files(output_base_path, brightness_values, contrast_values)
