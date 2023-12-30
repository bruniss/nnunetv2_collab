from PIL import Image
import os

# Disable the decompression bomb error for large images
Image.MAX_IMAGE_PIXELS = None 

def convert_and_modify_image(image_path, output_folder):
    try:
        with Image.open(image_path) as img:
            # Convert to PNG format
            png_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + '.png')
            img.save(png_path)
            print(f"Converted to PNG and saved: {png_path}")

            # Open the newly created PNG image
            with Image.open(png_path) as editable_img:
                converted = False

                # Convert image to grayscale if not already
                if editable_img.mode != 'L':
                    editable_img = editable_img.convert('L')
                    converted = True

                # Check and convert pixel values
                pixels = editable_img.load()
                for i in range(editable_img.width):
                    for j in range(editable_img.height):
                        if pixels[i, j] == 1:
                            pixels[i, j] = 255
                            converted = True

                if converted:
                    editable_img.save(png_path)
                    print(f"Modified pixel values and saved: {png_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def check_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            base_name = os.path.splitext(filename)[0]
            png_filename = base_name + '.png'
            image_path = os.path.join(input_folder, filename)
            output_png_path = os.path.join(output_folder, png_filename)

            # Check if the PNG version already exists in the output folder
            if not os.path.exists(output_png_path):
                convert_and_modify_image(image_path, output_folder)
            else:
                print(f"Already processed: {png_filename}")

input_folder = '/home/sean/Desktop/segmentation_base/test-out-poly'  # Replace with the path to your input folder
output_folder = '/home/sean/Desktop/segmentation_base/test-out-poly_png'  # Replace with the path to your output folder
check_folder(input_folder, output_folder)
