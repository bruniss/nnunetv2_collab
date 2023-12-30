import os

def rename_files(folder_path):
    # Replace 'YOUR_FOLDER_PATH' with the path of your target folder
    for filename in os.listdir(folder_path):
        if filename.endswith("_0001.tif"):
            # Construct the old and new file paths
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, filename.replace("_0001.tif", "_0000.tif"))
            
            # Renaming the file
            os.rename(old_file, new_file)
            print(f"Renamed: {old_file} to {new_file}")

# Call the function with your folder path
rename_files('/home/sean/Desktop/segmentation_base/datasets/nnUNet_raw/Dataset003_pol2/imagesTr')
