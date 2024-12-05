import hashlib
import os
from PIL import Image


def convert_image(image_path: str, save_path: str, output_format: str = 'webp') -> None:
    """
    Converts an image to a specified format and saves it to the given path.

    Args:
        image_path (str): Path to the input image file.
        save_path (str): Path where the converted image will be saved (excluding extension).
        output_format (str, optional): Desired output format (e.g., 'webp', 'png'). Defaults to 'webp'.

    Raises:
        FileNotFoundError: If the input image file does not exist.
        OSError: If there is an issue processing or saving the image.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    try:
        with Image.open(image_path) as img:
            img.save(f"{save_path}.{output_format}", output_format.upper())
    except OSError as e:
        raise OSError(f"Error converting or saving the image: {e}")


def calculate_precise_image_hash(image_path: str) -> str:
    """
    Calculates a SHA-256 hash of an image file for precise comparison.

    Args:
        image_path (str): Path to the input image file.

    Returns:
        str: The SHA-256 hash of the image.

    Raises:
        FileNotFoundError: If the input image file does not exist.
        OSError: If there is an issue reading the image file.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            image_hash = hashlib.sha256(image_data).hexdigest()
        return image_hash
    except OSError as e:
        raise OSError(f"Error reading the image file: {e}")
