import os
from ruamel.yaml import YAML

output_base_path = "/usr/src/ultralytics/videos/datasets/data_modified"
brightness_values = [-50, 0, 50]
contrast_values = [0.5, 1.0, 1.5]
class_names = ['bicycle', 'bus', 'car', 'droide', 'motorcycle', 'navette', 'person', 'truck']

# Créer les fichiers YAML de configuration
def create_yaml_files(base_path, brightness_values, contrast_values, class_names):
    yaml = YAML()
    yaml.default_flow_style = None
    
    for brightness in brightness_values:
        for contrast in contrast_values:
            output_folder = f"brightness_{brightness}_contrast_{contrast}"
            dataset_path = os.path.join(base_path, output_folder)
            
            yaml_content = {
                'path': dataset_path,
                'train': 'images',  # Assuming we use the 'images' folder for validation as well
                'val': 'images',
                'test': 'images',
                'nc': len(class_names),
                'names': class_names
            }
            
            yaml_file = os.path.join(dataset_path, f"{output_folder}.yaml")
            os.makedirs(os.path.dirname(yaml_file), exist_ok=True)
            
            with open(yaml_file, 'w') as f:
                yaml.dump(yaml_content, f)
                
            # Reformatter la liste des noms manuellement
            with open(yaml_file, 'r') as f:
                lines = f.readlines()
            with open(yaml_file, 'w') as f:
                for line in lines:
                    if line.startswith("names:"):
                        names_str = ", ".join(f"'{name}'" for name in class_names)
                        f.write(f"names: [{names_str}]\n")
                    else:
                        f.write(line)

# Vérifier les annotations
def check_annotations(base_path, brightness_values, contrast_values, class_names):
    num_classes = len(class_names)
    for brightness in brightness_values:
        for contrast in contrast_values:
            output_folder = f"brightness_{brightness}_contrast_{contrast}"
            labels_path = os.path.join(base_path, output_folder, "labels")
            for label_file in os.listdir(labels_path):
                label_path = os.path.join(labels_path, label_file)
                with open(label_path, 'r') as f:
                    for line in f:
                        class_id = int(line.split()[0])
                        if class_id >= num_classes:
                            print(f"Error: Label class {class_id} in file {label_path} exceeds the number of defined classes {num_classes - 1}")

# Créer les fichiers YAML pour chaque ensemble d'images modifiées
create_yaml_files(output_base_path, brightness_values, contrast_values, class_names)
check_annotations(output_base_path, brightness_values, contrast_values, class_names)
