import os
import yaml

output_base_path = "/usr/src/ultralytics/videos/datasets/data_modified"
brightness_values = [-50, 0, 50]
contrast_values = [0.5, 1.0, 1.5]

class CustomDumper(yaml.SafeDumper):
    pass

def str_presenter(dumper, data):
    if '\n' in data:  # if the string contains newlines, use the block format
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

CustomDumper.add_representer(str, str_presenter)

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
                'nc': 8,
                'names': ["bicycle"]  # Replace with actual class names
            }
            
            yaml_file = os.path.join(dataset_path, f"{output_folder}.yaml")
            with open(yaml_file, 'w') as f:
                yaml.dump(yaml_content, f, Dumper=CustomDumper, default_flow_style=None, sort_keys=False)

# Créer les fichiers YAML pour chaque ensemble d'images modifiées
create_yaml_files(output_base_path, brightness_values, contrast_values)
