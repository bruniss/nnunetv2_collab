import os
from PIL import Image
import random
import numpy as np

Image.MAX_IMAGE_PIXELS = None

# Configurable parameters
CROP_SIZE = (128, 128)  # Size of the region to be cropped (width, height)
ROI_THRESHOLD = 0.30    # Threshold for the region of interest in the ROI check
BRIGHTNESS_THRESHOLD = 200  # Brightness threshold for the ROI check
OVERLAP_THRESHOLD = 0.10    # Allowed overlap threshold for unique region selection
NUMBER_OF_REGIONS = 150       # Number of regions to select from each image

def contains_roi(inklabels_arr, region):
    region_arr = inklabels_arr[region[1]:region[3], region[0]:region[2]]
    white_pixels = np.sum(region_arr >= BRIGHTNESS_THRESHOLD)
    total_pixels = region_arr.size
    white_ratio = white_pixels / total_pixels
    return white_ratio >= ROI_THRESHOLD

def is_region_sufficiently_unique(region, selected_regions):
    for selected_region in selected_regions:
        intersect_area = max(0, min(region[2], selected_region[2]) - max(region[0], selected_region[0])) * \
                         max(0, min(region[3], selected_region[3]) - max(region[1], selected_region[1]))
        if intersect_area > 0:
            region_area = (region[2] - region[0]) * (region[3] - region[1])
            if intersect_area / region_area > OVERLAP_THRESHOLD:
                return False
    return True

def select_random_region(inklabels_arr, width, height, selected_regions):
    crop_width, crop_height = CROP_SIZE
    attempt_count = 0
    while attempt_count < 100:
        x = random.randint(0, width - crop_width)
        y = random.randint(0, height - crop_height)
        region = (x, y, x + crop_width, y + crop_height)

        if contains_roi(inklabels_arr, region) and is_region_sufficiently_unique(region, selected_regions):
            selected_regions.add(region)
            return region
        attempt_count += 1

    print("Could not find a suitable unique region")
    return None

def get_unique_filename(base_folder, parent_folder_name, tif_number, extension):
    file_name = f"{parent_folder_name}_{tif_number}_0000{extension}"
    counter = 1
    while os.path.exists(os.path.join(base_folder, file_name)):
        file_name = f"{parent_folder_name}_{tif_number}_0000_{counter}{extension}"
        counter += 1
    return file_name

def process_folder(dataset_path, parent_folder_name):
    print(f"Processing dataset: {parent_folder_name}")

    inklabels_file = f"{dataset_path}/inklabels.png"
    if not os.path.exists(inklabels_file):
        print(f"inklabels.png not found in {dataset_path}")
        return

    print("Opening inklabels image")
    inklabels_img = Image.open(inklabels_file).convert('L')

    width, height = inklabels_img.size
    print(f"Image dimensions: width={width}, height={height}")

    inklabels_arr = np.array(inklabels_img)
    selected_regions = set()

    imagesTr_folder = os.path.join(dataset_path, "imagesTr")
    labelsTr_folder = os.path.join(dataset_path, "labelsTr")
    os.makedirs(imagesTr_folder, exist_ok=True)
    os.makedirs(labelsTr_folder, exist_ok=True)

    for tif_number in range(20, 46):
        tif_file = f"{dataset_path}/layers/{tif_number}.tif"
        if not os.path.exists(tif_file):
            print(f"File not found: {tif_file}")
            continue

        for _ in range(NUMBER_OF_REGIONS):
            region = select_random_region(inklabels_arr, width, height, selected_regions)
            if region is None:
                break  # Break out of the loop if no suitable region is found

            layer_img = Image.open(tif_file)
            layer_crop = layer_img.crop(region)
            inklabels_crop = inklabels_img.crop(region)

            cropped_tif_file = get_unique_filename(imagesTr_folder, parent_folder_name, tif_number, ".tif")
            layer_crop.save(os.path.join(imagesTr_folder, cropped_tif_file))
            print(f"Processed and saved tif file: {cropped_tif_file}")

            cropped_label_file = get_unique_filename(labelsTr_folder, parent_folder_name, tif_number, ".png")
            inklabels_crop.save(os.path.join(labelsTr_folder, cropped_label_file))
            print(f"Saved corresponding label file: {cropped_label_file}")

    print(f"Completed processing dataset: {parent_folder_name}")

# Parent folder containing all dataset folders
parent_folder = "e:/modelmain/newest-train/"  # Replace with your actual parent folder path

for folder_name in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, folder_name)
    if os.path.isdir(subfolder_path):
        print(f"Processing folder: {subfolder_path}")
        process_folder(subfolder_path, folder_name)

print("All folders processed successfully.")
