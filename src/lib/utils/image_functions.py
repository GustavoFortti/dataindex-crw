import hashlib
import os

from PIL import Image


def convert_image(image_path, save_path, output_format='webp'):
    if (not os.path.isfile(image_path)):
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    
    with Image.open(image_path) as img:
        img.save(save_path + '.' + output_format, output_format.upper())

def calculate_precise_image_hash(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        image_hash = hashlib.sha256(image_data).hexdigest()
    return image_hash
