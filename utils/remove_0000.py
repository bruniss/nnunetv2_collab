import os

def rename_tif_files(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith("_0000.tif"):
            # Form the full file path
            file_path = os.path.join(folder_path, filename)
            # Generate new file name by removing "_0000"
            new_filename = filename.replace("_0000.tif", ".tif")
            new_file_path = os.path.join(folder_path, new_filename)
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")

    print("Renaming complete.")

# Define the folder path
folder_path = '/home/sean/Desktop/segmentation_base/datasets/nnUNet_raw/Dataset002_sixtyfour/labelsTr/'

# Call the function
rename_tif_files(folder_path)
