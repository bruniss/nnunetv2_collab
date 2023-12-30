import os
from typing import Tuple
import json
from os.path import join

def save_json(data, filename, sort_keys=True):
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=sort_keys, indent=4)

def generate_dataset_json(output_folder: str,
                          channel_names: dict,
                          labels: dict,
                          num_training_cases: int,
                          file_ending: str,
                          spacing: Tuple[float, float, float],
                          regions_class_order: Tuple[int, ...] = None,
                          dataset_name: str = None,
                          reference: str = None,
                          release: str = None,
                          license: str = None,
                          description: str = None,
                          overwrite_image_reader_writer: str = None, **kwargs):
    """
    Generates a dataset.json file in the output folder.

    [Add the rest of your function's documentation here as necessary.]
    """
    # Prepare channel names and labels
    channel_names = {str(k): v for k, v in channel_names.items()}
    labels = {k: (tuple(map(int, v)) if isinstance(v, (tuple, list)) else int(v)) for k, v in labels.items()}

    # Create the dataset JSON structure
    dataset_json = {
        'channel_names': channel_names,
        'labels': labels,
        'numTraining': num_training_cases,
        'file_ending': file_ending,
        'spacing': spacing
    }

    # Add optional metadata
    if dataset_name: dataset_json['name'] = dataset_name
    if reference: dataset_json['reference'] = reference
    if release: dataset_json['release'] = release
    if license: dataset_json['licence'] = license
    if description: dataset_json['description'] = description
    if overwrite_image_reader_writer: dataset_json['overwrite_image_reader_writer'] = overwrite_image_reader_writer
    if regions_class_order: dataset_json['regions_class_order'] = regions_class_order

    # Include any additional kwargs
    dataset_json.update(kwargs)

    # Save the dataset.json file
    dataset_json_path = join(output_folder, 'dataset.json')
    if not os.path.exists(dataset_json_path):
        save_json(dataset_json, dataset_json_path, sort_keys=False)
    else:
        print(f"File {dataset_json_path} already exists. Skipping.")

def process_all_datasets(parent_folder):
    for dataset_folder in os.listdir(parent_folder):
        dataset_path = os.path.join(parent_folder, dataset_folder)

        # Set parameters for each dataset
        channel_names = {0: 'CT'}  # Adjust as needed
        labels = {'background': 0, 'tumor': 1}  # Adjust as needed
        num_training_cases = 100  # Adjust as needed
        file_ending = '.tif'
        spacing = (7.91, 7.91, 7.91)  # Spacing in micrometers

        # Call the function for each dataset
        generate_dataset_json(dataset_path, channel_names, labels,
                              num_training_cases, file_ending, spacing)
        print(f"Processed dataset in {dataset_folder}")

# Example usage
parent_folder = '/home/sean/Desktop/segmentation_base/datasets/'  # Replace with your datasets' parent folder path
process_all_datasets(parent_folder)