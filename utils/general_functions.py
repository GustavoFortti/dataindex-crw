import os
import re
import csv
import json
import math
import shutil
import base64
import hashlib
import requests
import unicodedata
import pandas as pd
from PIL import Image
from datetime import date, timedelta

DATE_FORMAT = "%Y-%m-%d"

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"O arquivo {file_path} não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON {file_path}.")
        return None
    except Exception as e:
        print(f"Um erro ocorreu ao ler o arquivo {file_path}: {e}")
        return None

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted successfully")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")

def path_exist(oath):
    return os.path.exists(oath)

def create_file_if_not_exists(file_path, text=False):
    if not path_exist(file_path):
        try:
            with open(file_path, mode='a', newline='') as file:
                if (text):
                    file.write(text + "\n")
                    print(f"write '{text}' successfully.")
                print(f"File '{file_path}' created successfully.")
        except FileExistsError:
            print(f"The file '{file_path}' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
def encode_base64(val):
    return base64.b64encode(val.encode('utf-8')).decode('utf-8')

def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()[:8]

def clean_text(texto):
    # Normaliza o texto para decompor acentos e caracteres especiais
    if isinstance(texto, str):
        texto = unicodedata.normalize('NFKD', texto)
        # Mantém apenas caracteres alfanuméricos e espaços
        texto = u"".join([c for c in texto if not unicodedata.combining(c)])
        # Remove tudo que não for letra, número ou espaço
        return remove_spaces(re.sub(r'[^A-Za-z0-9 ]+', '', texto).lower())
    return texto

def list_directory(path):
    try:
        # Check if the path is a valid directory
        if os.path.isdir(path):
            contents = os.listdir(path)
            print(f"Contents of directory '{path}':")
            items = []
            for item in contents:
                items.append(item)
            
            return items
        else:
            print(f"'{path}' is not a valid directory.")
    except Exception as e:
        print(f"Error while listing the directory: {str(e)}")

def slice_text(original, start, end):
    start_index = original.find(start)
    if start_index == -1:
        return None

    end_index = original.rfind(end)
    if end_index == -1:
        return None

    if end_index < start_index:
        return None

    return original[start_index:end_index + len(end)]

def create_directory_if_not_exists(directory_path):
    if not path_exist(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        except OSError as error:
            print(f"Error creating directory '{directory_path}': {error}")

def check_if_is_old_file(file_path):
    if path_exist(file_path):
        modification_time = os.path.getmtime(file_path)
        last_modified_date = date.fromtimestamp(modification_time)

        today = date.today()

        return False
        return last_modified_date != today
    return True

def filter_df_by_days(df, column, n_days_back):
    if (len(df) == 0): return df
    df[column] = pd.to_datetime(df[column], format=DATE_FORMAT, dayfirst=True)
    days = date.today() - timedelta(days=n_days_back)
    days = pd.to_datetime(days)
    df = df[df[column] >= days]

    return df

def format_column_date(df, column):
    df[column] = pd.to_datetime(df[column], format=DATE_FORMAT, dayfirst=True)
    df[column] = df[column].dt.strftime(DATE_FORMAT)

    return df

def remove_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

def clean_string_break_line(value):
    return remove_spaces(str(value).replace('\n', '').replace('\xa0', ' '))
    
def remove_numbers(input_string):
    return re.sub(r'\d', '', input_string)

def loading(index, size):
    progress = index / size * 100
    bar_length = 50
    block = int(round(bar_length * index / size))
    progress_bar = "[" + "=" * block + "-" * (bar_length - block) + "]"
    print(f"Progresso: {progress:.2f}% {progress_bar}", end="\r")

def remove_nan_from_dict(document):
    new_document = {}
    for chave, valor in document.items():
        if isinstance(valor, float):
            if not math.isnan(valor):
                new_document[chave] = valor
        else:
            new_document[chave] = valor  # Se não for um float, inclua no novo dicionário

    return new_document

def file_exists(directory, filename):
    file_path = os.path.join(directory, filename)
    print(file_path)
    return os.path.exists(file_path)

def find_in_text_with_word_list(text, word_list):
    match = None
    for word in word_list:
        clean_word = clean_text(word)
        text = clean_text(text)
        
        match = re.search(clean_word, clean_text(text))  # Expressão regular para encontrar dígitos
        if match:
            break
            
    if match:
        return True
    return False

def save_file(text, path):
    with open(path, "w") as file:
        print("file path: " + path)
        file.write(str(text))

def download_image(image_url, image_path, image_name):
    print(f"Download: {image_url}")
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
        return f"Image downloaded successfully! Saved as: {file_name_with_extension}"
    else:
        print(f"Failed to download the image. HTTP status code: {response.status_code}")

def convert_image(image_path, save_path, output_format='webp'):
    if (not os.path.isfile(image_path)):
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    
    with Image.open(image_path) as img:
            # Converte a imagem para WebP e salva
            img.save(save_path + '.' + output_format, output_format.upper())

def calculate_precise_image_hash(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        image_hash = hashlib.sha256(image_data).hexdigest()
    return image_hash

def check_url_existence(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        return False
    
def delete_directory_and_contents(directory_path):
    if not os.path.exists(directory_path):
        print("Directory does not exist.")
        return

    shutil.rmtree(directory_path)
    print(f"Directory and all contents deleted: {directory_path}")

def first_exec(data_path):
    origin = file_exists(data_path, "origin.csv")
    tree = file_exists(data_path, "tree.csv")
    img_tmp = file_exists(data_path, "img_tmp")
    products = file_exists(data_path, "products")
    
    if (origin & tree & img_tmp & products):
        exit(0)

    if (origin or tree or img_tmp or products):
        delete_file(f"{data_path}/origin.csv")
        delete_file(f"{data_path}/tree.csv")
        delete_directory_and_contents(f"{data_path}/img_tmp")
        delete_directory_and_contents(f"{data_path}/products")

    print("First execution")

def is_price(string):
    pattern = r"""
    (R\$\s?\d{1,3}(\.\d{3})*,\d{2})|  # BRL: R$
    (€\s?\d{1,3}(\.\d{3})*,\d{2})|    # EUR: €
    (\$\s?\d{1,3}(,\d{3})*\.\d{2})|   # USD: $
    (£\s?\d{1,3}(,\d{3})*\.\d{2})     # GBP: £
    """

    return bool(re.match(pattern, string, re.VERBOSE))

def read_csvs_on_dir_and_union(directory):
    dfs = []

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)
    
    result_df = pd.concat(dfs, ignore_index=True)
    
    return result_df

def has_files(directory):
    items = os.listdir(directory)
    
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            return True
    return False

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def calc_string_diff_in_df_col(row):
    distance = levenshtein(row['title_x'], row['title_y'])
    max_len = max(len(row['title_x']), len(row['title_y']))
    percent_diff = (distance / max_len) if max_len != 0 else 0
    return percent_diff