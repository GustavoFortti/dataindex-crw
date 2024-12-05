import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple

import requests

from src.lib.utils.log import message

DATE_FORMAT = "%Y-%m-%d"

def save_file(text: str, path: str) -> None:
    """
    Saves text to a file at the specified path.

    Args:
        text (str): The text content to save.
        path (str): The file path where the text will be saved.
    """
    create_file_if_not_exists(path, text)
    with open(path, "w", encoding='utf-8') as file:
        message(f"File path: {path}")
        file.write(str(text))


def save_file_with_line_breaks(file_path: str, text: str) -> None:
    """
    Saves text to a file, ensuring line breaks are preserved.

    Args:
        file_path (str): The path to the file.
        text (str): The text content to save, potentially containing line breaks.
    """
    create_file_if_not_exists(file_path, text)
    lines: List[str] = text.split("\n")

    with open(file_path, "w", encoding='utf-8') as file:
        for line in lines:
            file.write(line + "\n")


def read_file(file_path: str, return_date: bool = False) -> Optional[str]:
    """
    Reads a file and returns its contents as a string.

    If return_date is True, returns the last modification date of the file.

    Args:
        file_path (str): The path to the file.
        return_date (bool, optional): Whether to return the last modification date. Defaults to False.

    Returns:
        Optional[str]: The file contents as a string or the modification date if return_date is True.
    """
    try:
        if return_date:
            file_stats = os.stat(file_path)
            # Return the last modification date in readable format
            return datetime.fromtimestamp(file_stats.st_mtime).strftime(DATE_FORMAT)
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        message(f"An error occurred: {e}")
        return None


def read_json(file_path: str) -> Optional[Any]:
    """
    Reads a JSON file and returns its content or None in case of an error.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Optional[Any]: The content of the JSON file, or None if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        message(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        message(f"Error decoding the JSON file {file_path}.")
    except Exception as e:
        message(f"An error occurred while reading the file {file_path}: {e}")
    return None


def save_json(file_name: str, data: Any) -> None:
    """
    Saves data to a JSON file.

    Args:
        file_name (str): The path to the JSON file.
        data (Any): The data to be saved as JSON.
    """
    message(f"Saving JSON to {file_name}")
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def delete_file(file_path: str) -> None:
    """
    Deletes a file if it exists, logging the outcome.

    Args:
        file_path (str): The path to the file to delete.
    """
    try:
        os.remove(file_path)
        message(f"File {file_path} has been deleted successfully")
    except FileNotFoundError:
        message(f"The file {file_path} does not exist")
    except Exception as e:
        message(f"An error occurred: {e}")


def file_modified_within_x_hours(file_path: str, hours: int) -> bool:
    """
    Checks if the file was modified within the specified number of hours.

    Args:
        file_path (str): The path to the file.
        hours (int): The number of hours to check.

    Returns:
        bool: True if the file was modified within the specified hours, False otherwise.
    """
    if not os.path.isfile(file_path):
        message("File does not exist")
        return False

    now = datetime.now()
    last_modification = datetime.fromtimestamp(os.path.getmtime(file_path))
    message(f"{file_path} last modification: {last_modification}")

    difference = now - last_modification

    return difference <= timedelta(hours=hours)


def file_or_path_exists(path: str) -> bool:
    """
    Checks if a path exists.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)


def create_file_if_not_exists(file_path: str, text: Optional[str] = None) -> None:
    """
    Creates a file if it doesn't exist. Optionally writes text to it.

    Args:
        file_path (str): The path to the file.
        text (Optional[str]): The text content to write to the file.
    """
    if not file_or_path_exists(file_path):
        try:
            with open(file_path, mode='a', encoding='utf-8') as file:
                if text:
                    file.write(text + "\n")
                message(f"File '{file_path}' created successfully.")
        except FileExistsError:
            message(f"The file '{file_path}' already exists.")
        except Exception as e:
            message(f"An error occurred: {e}")


def create_directory_if_not_exists(directory_path: str) -> None:
    """
    Creates a directory if it doesn't exist.

    Args:
        directory_path (str): The path to the directory.
    """
    if not file_or_path_exists(directory_path):
        try:
            os.makedirs(directory_path)
            message(f"Directory '{directory_path}' created successfully.")
        except OSError as error:
            message(f"Error creating directory '{directory_path}': {error}")


def download_image(image_url: str, image_path: str, image_name: str) -> Optional[str]:
    """
    Downloads an image from a URL and saves it to the specified path.

    Args:
        image_url (str): The URL of the image to download.
        image_path (str): The directory path where the image will be saved.
        image_name (str): The base name of the image file.

    Returns:
        Optional[str]: Success message if download is successful, None otherwise.
    """
    message(f"Downloading: {image_url}")
    try:
        response = requests.get(image_url, timeout=10)

        if response.status_code == 200:
            # Obtain the content type of the response
            content_type = response.headers.get('Content-Type', '')
            
            # Determine the file extension based on content type
            if 'image/jpeg' in content_type:
                extension = '.jpg'
            elif 'image/png' in content_type:
                extension = '.png'
            elif 'image/gif' in content_type:
                extension = '.gif'
            else:
                # Use a generic extension if format is not recognized
                extension = '.img'

            # Define the full file name with the appropriate extension
            file_name_with_extension = image_name + extension
            full_path = os.path.join(image_path, file_name_with_extension)

            # Save the image in the correct format
            with open(full_path, 'wb') as f:
                f.write(response.content)
            return f"Image downloaded successfully! Saved as: {full_path}"
        else:
            message(f"Failed to download the image. HTTP status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        message(f"Error downloading image {image_url}: {e}")
        return None


def save_images(image_urls: List[str], image_path: str, image_names: List[str]) -> None:
    """
    Downloads multiple images concurrently and saves them to the specified path.

    Args:
        image_urls (List[str]): List of image URLs to download.
        image_path (str): The directory path where images will be saved.
        image_names (List[str]): List of base names for the image files.
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Map each future task to its respective URL using a dictionary
        future_to_url = {
            executor.submit(download_image, url, image_path, name): url
            for url, name in zip(image_urls, image_names)
        }

        # Iterate over completed tasks as they finish
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                if result:
                    message(result)
                else:
                    message(f"Download failed for {url}")
            except Exception as e:
                message(f"{url} generated an exception: {e}")


def file_exists(directory: str, filename: str) -> bool:
    """
    Checks if a file exists in a specified directory.

    Args:
        directory (str): The directory path.
        filename (str): The name of the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    file_path = os.path.join(directory, filename)
    message(f"Checking if file exists: {file_path}")
    return os.path.exists(file_path)


def file_exists_with_modification_time(directory: str, filename: str) -> Tuple[bool, Optional[str]]:
    """
    Checks if a file exists and returns its last modification date.

    Args:
        directory (str): The directory path.
        filename (str): The name of the file.

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the file exists,
        and the modification date in YYYY-MM-DD format if it exists.
    """
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        # Get the last modification timestamp of the file
        modification_time = os.path.getmtime(file_path)
        # Convert the timestamp to a readable date format
        readable_time = datetime.fromtimestamp(modification_time).strftime(DATE_FORMAT)
        return True, readable_time
    else:
        return False, None


def delete_directory_and_contents(directory_path: str) -> None:
    """
    Deletes a directory and all its contents.

    Args:
        directory_path (str): The path to the directory to delete.
    """
    if not os.path.exists(directory_path):
        message("Directory does not exist.")
        return

    shutil.rmtree(directory_path)
    message(f"Directory and all contents deleted: {directory_path}")


def get_old_files_by_percent(
    directory_path: str, sort_ascending: bool = True, percentage: float = 5.0
) -> List[str]:
    """
    Retrieves a list of files from a directory sorted by modification date.

    Args:
        directory_path (str): The path to the directory.
        sort_ascending (bool, optional): If True, sorts files from oldest to newest.
        percentage (float, optional): The percentage of files to retrieve.

    Returns:
        List[str]: A list of selected file names.
    """
    all_files = [
        file for file in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, file))
    ]
    files_info = []

    for file in all_files:
        file_path = os.path.join(directory_path, file)
        last_modification_time = os.path.getmtime(file_path)
        last_modification_date = datetime.fromtimestamp(last_modification_time)
        files_info.append((file, last_modification_date))

    files_info.sort(key=lambda x: x[1], reverse=not sort_ascending)

    files_count = len(files_info)
    slice_count = max(1, int((percentage / 100.0) * files_count))

    selected_files = [file_info[0] for file_info in files_info[:slice_count]]

    if len(selected_files) > 30:
        selected_files = selected_files[:30]

    return selected_files


def list_directory(path: str) -> Optional[List[str]]:
    """
    Lists the contents of a directory.

    Args:
        path (str): The path to the directory.

    Returns:
        Optional[List[str]]: A list of directory contents, or None if an error occurs.
    """
    try:
        if os.path.isdir(path):
            contents = os.listdir(path)
            message(f"Contents of directory '{path}':")
            items: List[str] = []
            for item in contents:
                items.append(item)
            return items
        else:
            message(f"'{path}' is not a valid directory.")
            return None
    except Exception as e:
        message(f"Error while listing the directory: {str(e)}")
        return None


def has_files(directory: str) -> bool:
    """
    Checks if a directory contains any files.

    Args:
        directory (str): The directory path.

    Returns:
        bool: True if the directory contains files, False otherwise.
    """
    try:
        items = os.listdir(directory)

        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                return True
        return False
    except FileNotFoundError:
        message(f"The directory '{directory}' does not exist.")
        return False
    except Exception as e:
        message(f"An error occurred while checking files in '{directory}': {e}")
        return False
