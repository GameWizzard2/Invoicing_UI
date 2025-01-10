import logging
from PIL import Image, ImageOps
import os

def resize_image_by_half(input_path, output_path):
    """
    Resizes an image to reduce its file size while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
    """
    try:
        logging.debug(f"Opening image: {input_path}")
        with Image.open(input_path) as img:
            # Maintain aspect ratio, orientation, and resize
            img = ImageOps.exif_transpose(img)
            pic = img.size
            half_dimensions = (pic[0] // 2, pic[1] // 2)
            resized_image = img.resize(half_dimensions)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save the resized image
            resized_image.save(output_path, format=img.format)
            logging.info(f"Image resized and saved to {output_path}")
    except Exception as e:
        logging.error(f"Error resizing image: {e}")

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Replace with actual paths
    input_folder = "D:\\Example_pics\\Source"
    output_folder = "D:\\Example_pics\\Destination"

    # Process each file in the input folder
    for file in os.listdir(input_folder):
        # Construct full input and output file paths
        input_file_path = os.path.join(input_folder, file)
        output_file_path = os.path.join(output_folder, file)

        # Log the current file being processed
        logging.debug(
            f"The current file selected is {file} and has been joined to create "
            f"inputFilePath: {input_file_path} and outputFilePath: {output_file_path}"
        )

        # Filter for valid image files
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            resize_image_by_half(input_file_path, output_file_path)
        else:
            logging.warning(f"Skipping non-image file: {file}")