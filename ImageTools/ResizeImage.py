from PIL import Image
def resize_image(input_path, output_path, width, height, quality=85):
    with Image.open(input_path) as img:
        img = img.resize((width, height), Image.LANCZOS)
        img.save(output_path, "JPEG", quality=quality)

resize_image("input.jpg", "output.jpg", 800, 600, quality=75)