from datetime import datetime, timedelta
import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional

import requests

from src.lib.utils.log import message

DATE_FORMAT = "%Y-%m-%d"


def save_file(text, path):
    create_file_if_not_exists(path, text)
    with open(path, "w") as file:
        message("file path: " + path)
        file.write(str(text))

def save_file_with_line_breaks(file_path, text):
    # Quebra a string em linhas onde houver \n
    create_file_if_not_exists(file_path, text)
    lines = text.split("\n")
    
    # Abre o arquivo para escrita
    with open(file_path, "w") as file:
        # Grava cada linha no arquivo
        for line in lines:
            file.write(line + "\n") 

def read_file(file_path):
    """Reads a file and returns its contents as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def read_json(file_path: str) -> Optional[Any]:
    """Reads a JSON file and returns its content or None in case of an error."""
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
    """Saves data to a JSON file."""
    
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def delete_file(file_path: str) -> None:
    """Deletes a file if it exists, logging the outcome."""
    try:
        os.remove(file_path)
        message(f"File {file_path} has been deleted successfully")
    except FileNotFoundError:
        message(f"The file {file_path} does not exist")
    except Exception as e:
        message(f"An error occurred: {e}")

def file_modified_within_x_hours(file_path, hours):
    # Check if the file exists
    if not os.path.isfile(file_path):
        message("File not exist")
        return False
    
    # Get the current time
    now = datetime.now()
    
    # Get the last modification time of the file
    last_modification = datetime.fromtimestamp(os.path.getmtime(file_path))
    print(last_modification)
    
    # Calculate the difference between now and the last modification
    difference = now - last_modification
    
    # Check if the file was modified within the specified number of hours
    if difference <= timedelta(hours=hours):
        return True
    else:
        return False

def path_exists(path: str) -> bool:
    """Checks if a path exists."""
    message(f"check - {path}")
    return os.path.exists(path)

def create_file_if_not_exists(file_path: str, text: Optional[str] = None) -> None:
    """Creates a file if it doesn't exist. Optionally writes text to it."""
    if not path_exists(file_path):
        try:
            with open(file_path, mode='a', encoding='utf-8') as file:
                if text:
                    file.write(text + "\n")
                message(f"File '{file_path}' created successfully.")
        except FileExistsError:
            message(f"The file '{file_path}' already exists.")
        except Exception as e:
            message(f"An error occurred: {e}")

def create_directory_if_not_exists(directory_path):
    if not path_exists(directory_path):
        try:
            os.makedirs(directory_path)
            message(f"Directory '{directory_path}' created successfully.")
        except OSError as error:
            message(f"Error creating directory '{directory_path}': {error}")
            
def download_image(image_url, image_path, image_name):
    message(f"Download: {image_url}")
    response = requests.get(image_url)

    if response.status_code == 200:
        # Obtendo o tipo de conteúdo da resposta
        content_type = response.headers['Content-Type']
        
        # Determinando a extensão com base no tipo de conteúdo
        if 'image/jpeg' in content_type:
            extension = '.jpg'
        elif 'image/png' in content_type:
            extension = '.png'
        elif 'image/gif' in content_type:
            extension = '.gif'
        # Adicione mais condições conforme necessário para outros formatos de imagem
        else:
            # Se o formato não for reconhecido, usamos uma extensão genérica
            extension = '.img'

        # Definindo o nome completo do arquivo com a extensão apropriada
        file_name_with_extension = image_name + extension

        # Salvando a imagem no formato correto
        with open(image_path + file_name_with_extension, 'wb') as f:
            f.write(response.content)
        return f"Image downloaded successfully! Saved as: {image_path}{file_name_with_extension}"
    else:
        message(f"Failed to download the image. HTTP status code: {response.status_code}")

def save_images(image_urls, image_path, image_names):
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Mapeia cada tarefa futura para a respectiva URL usando um dicionário
        future_to_url = {executor.submit(download_image, url, image_path, name): url for url, name in zip(image_urls, image_names)}

        # Itera sobre as tarefas concluídas conforme elas são finalizadas
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()  # Obtém o resultado da tarefa
                if result:
                    message(result)  # Imprime o resultado se a imagem foi baixada com sucesso
                else:
                    message(f"Download failed for {url}")  # Imprime uma mensagem de falha caso contrário
            except Exception as e:
                message(f"{url} generated an exception: {e}")  # Imprime a exceção, se ocorrer
   
def file_exists(directory, filename):
    file_path = os.path.join(directory, filename)
    message(file_path)
    return os.path.exists(file_path)

def file_exists_with_modification_time(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        # Obtém o timestamp da última modificação do arquivo
        modification_time = os.path.getmtime(file_path)
        # Converte o timestamp para um formato de data legível
        readable_time = datetime.fromtimestamp(modification_time)
        return True, readable_time  # Retorna True e a data de modificação
    else:
        return False, None  # Retorna False e None se o arquivo não existir

def delete_directory_and_contents(directory_path):
    if not os.path.exists(directory_path):
        message("Directory does not exist.")
        return

    shutil.rmtree(directory_path)
    message(f"Directory and all contents deleted: {directory_path}")

def get_old_files_by_percent(directory_path, sort_ascending=True, percentage=5):
    all_files = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
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

    return selected_files

def list_directory(path):
    try:
        # Check if the path is a valid directory
        if os.path.isdir(path):
            contents = os.listdir(path)
            message(f"Contents of directory '{path}':")
            items = []
            for item in contents:
                items.append(item)
            
            return items
        else:
            message(f"'{path}' is not a valid directory.")
    except Exception as e:
        message(f"Error while listing the directory: {str(e)}")
        
def has_files(directory):
    items = os.listdir(directory)
    
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            return True
    return False