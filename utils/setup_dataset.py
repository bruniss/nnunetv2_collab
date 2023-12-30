import os
import shutil
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None  # Removes limit on image size

def process_folders(parent_dir):
    # Create directories for imagesTr and labelsTr if they don't exist
    if not os.path.exists('imagesTr'):
        os.makedirs('imagesTr')
    if not os.path.exists('labelsTr'):
        os.makedirs('labelsTr')

    # Iterate through each subfolder in the parent directory
    for folder in os.listdir(parent_dir):
        folder_path = os.path.join(parent_dir, folder)

        if os.path.isdir(folder_path):
            layers_folder = os.path.join(folder_path, 'layers')
            inklabel_file = os.path.join(folder_path, 'inklabels.png')

            if os.path.exists(layers_folder) and os.path.exists(inklabel_file):
                # Copy and rename TIFF files
                for tif_number in range(20, 46):
                    new_number = tif_number - 19  # Adjusting the number from 20-45 to 1-26
                    tif_file = os.path.join(layers_folder, f'{tif_number}.tif')
                    if os.path.exists(tif_file):
                        new_tif_name = f'{folder}-{new_number}_0001.tif'
                        shutil.copy(tif_file, os.path.join('imagesTr', new_tif_name))

                    # Copy and rename inklabel file
                    new_label_name = f'{folder}-{new_number}.tif'
                    inklabel_copy_path = os.path.join('labelsTr', new_label_name)
                    shutil.copy(inklabel_file, inklabel_copy_path)

                    # Convert inklabel file from 0-255 to 0-1
                    img = Image.open(inklabel_copy_path)
                    img_array = np.array(img)
                    img_array = (img_array > 0).astype(np.uint8)
                    Image.fromarray(img_array * 255).save(inklabel_copy_path)

process_folders('/home/sean/Desktop/poly-preds/new-sections/')  # Replace with your parent directory path