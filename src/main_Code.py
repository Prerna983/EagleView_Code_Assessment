import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

def process_image(file_path, output_dir):
    # Read the image
    image = cv2.imread(file_path)

    if image is None:
        print(f"Error reading image: {file_path}")
        return 0  # Return 0 if image could not be read

    # Create binary mask where all channels are above 200
    # print(image[:,:,:])
    mask = np.all(image > 200, axis=-1).astype(np.uint8) * 255

    # Construct output file path in the specified directory
    base_name = os.path.basename(file_path)
    mask_file_name = f"mask_{base_name.rsplit('.', 1)[0]}.png"  # Save as PNG
    mask_file_path = os.path.join(output_dir, mask_file_name)

    # Save mask as PNG
    if cv2.imwrite(mask_file_path, mask):
        print(f"Saved mask image: {mask_file_path}")
    else:
        print(f"Failed to save mask image: {mask_file_path}")

    # Count pixels where mask is max
    pixel_count = np.sum(mask == 255)
    return pixel_count

def main(image_dir, output_dir):
    # List all jpg and png files in the directory
    image_files = [
        os.path.join(image_dir, f) 
        for f in os.listdir(image_dir) 
        if f.endswith(('.jpg', '.png'))
    ]

    total_pixel_count = 0

    # Process images in parallel
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda f: process_image(f, output_dir), image_files)
        total_pixel_count = sum(results)

    # Log the total count of pixels where mask is max
    print(f"Total pixels where mask is max across all images: {total_pixel_count}")

image_directory = r"D:/git_Code/EagleView_Code_Assessment/Online-test"
output_directory = r"D:/git_Code/EagleView_Code_Assessment/Online-test-output"
main(image_directory, output_directory)