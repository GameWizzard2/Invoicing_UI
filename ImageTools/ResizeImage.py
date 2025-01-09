import logging
from PIL import Image
import os

def resize_image_by_half(input_path, output_path):
    """
    Resizes an image to reduce its file size while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
        max_size (tuple): Maximum width and height (default is 1024x1024).
        quality (int): JPEG quality for the output image (default is 85).
    """
    try:
        logging.debug(f"Opening image: {input_path}")
        with Image.open(input_path) as img:
            # Maintain aspect ratio and resize to fit within max_size
            
            pic = img.size()
            half_dimensions = (pic[0] / 2, pic[1] / 2)
            img.resize(half_dimensions)
            output_path = os.path.join(output_path, os.path.abspath(input_path))

            # Save the resized image
            img.save(output_path)
            logging.info(f"Image resized and saved to {output_path}")
    except Exception as e:
        logging.error(f"Error resizing image: {e}")

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Replace with actual paths
    input_image = "path/to/your/input_image.jpg"
    output_image = "path/to/your/output_image.jpg"

    resize_image_by_half(input_image, output_image)