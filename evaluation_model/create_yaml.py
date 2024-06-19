import os
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import SingleQuotedScalarString

output_base_path = "/usr/src/ultralytics/videos/datasets/data_modified"
brightness_values = [-50, 0, 50]
contrast_values = [0.5, 1.0, 1.5]

# Créer les fichiers YAML de configuration
def create_yaml_files(base_path, brightness_values, contrast_values):
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
                'nc': 8,
                'names': ['bicycle', 'bus', 'car', 'droide', 'motorcycle', 'navette', 'person', 'truck']
            }
            
            yaml_file = os.path.join(dataset_path, f"{output_folder}.yaml")
            os.makedirs(os.path.dirname(yaml_file), exist_ok=True)
            
            # Ecrire le contenu YAML
            with open(yaml_file, 'w') as f:
                yaml.dump(yaml_content, f)

            # Charger le YAML pour le reformatter en ligne
            with open(yaml_file, 'r') as f:
                content = yaml.load(f)

            # Reformater la liste des noms en ligne
            names_list = '[' + ', '.join(f"'{name}'" for name in yaml_content['names']) + ']'
            content['names'] = names_list

            # Sauvegarder le YAML reformatté en ligne
            with open(yaml_file, 'w') as f:
                yaml.dump(content, f)

# Créer les fichiers YAML pour chaque ensemble d'images modifiées
create_yaml_files(output_base_path, brightness_values, contrast_values)
