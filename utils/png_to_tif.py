import os
from PIL import Image

def convert_png_to_tif(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            # Form the full file path
            file_path = os.path.join(folder_path, filename)
            # Open the image
            with Image.open(file_path) as img:
                # Convert and save as .tif
                tif_path = os.path.splitext(file_path)[0] + ".tif"
                img.save(tif_path)
                print(f"Converted {filename} to .tif")

    print("Conversion complete.")


# Example usage
folder_path = '/content/gdrive/MyDrive/nnUNetv2/nnUNetv2_raw/Dataset0001_3dlabels'  # Replace with your folder path
convert_png_to_tif(folder_path)