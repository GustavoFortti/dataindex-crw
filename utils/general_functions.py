import os
import re
import json
import math
import shutil
import base64
import hashlib
import requests
import statistics
import unicodedata
import pandas as pd

from glob import glob
from PIL import Image
from datetime import date, timedelta
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.log import message

DATE_FORMAT = "%Y-%m-%d"

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        message(f"O arquivo {file_path} não foi encontrado.")
        return None
    except json.JSONDecodeError:
        message(f"Erro ao decodificar o arquivo JSON {file_path}.")
        return None
    except Exception as e:
        message(f"Um erro ocorreu ao ler o arquivo {file_path}: {e}")
        return None

def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def delete_file(file_path):
    try:
        os.remove(file_path)
        message(f"File {file_path} has been deleted successfully")
    except FileNotFoundError:
        message(f"The file {file_path} does not exist")
    except Exception as e:
        message(f"An error occurred: {e}")

def path_exist(oath):
    return os.path.exists(oath)

def create_file_if_not_exists(file_path, text=False):
    if not path_exist(file_path):
        try:
            with open(file_path, mode='a', newline='') as file:
                if (text):
                    file.write(text + "\n")
                    message(f"write '{text}' successfully.")
                message(f"File '{file_path}' created successfully.")
        except FileExistsError:
            message(f"The file '{file_path}' already exists.")
        except Exception as e:
            message(f"An error occurred: {e}")
        
def encode_base64(val):
    return base64.b64encode(val.encode('utf-8')).decode('utf-8')

def generate_numeric_hash(data):
    hash_value = hash(data)
    numeric_hash = abs(hash_value)
    
    return numeric_hash

def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()[:8]

def clean_text(texto, clean_spaces=False, remove_final_s=False, remove_break_line=True, remove_accents=True, add_space_firts=False):
    if isinstance(texto, str):
        original_length = len(texto)

        if remove_accents:
            # Substituir acentos pelos caracteres sem acento, sem modificar o tamanho do texto.
            texto = unicodedata.normalize('NFKD', texto)
            texto = ''.join([c if not unicodedata.combining(c) else '' for c in texto])
        else:
            # Manter o texto como está, sem alterar os acentos.
            texto = texto

        # Substituir caracteres não alfanuméricos (exceto espaços) por espaços, mantendo o comprimento.
        texto = re.sub(r'[^\w\s]', lambda match: ' ' if match.group(0) != ' ' else ' ', texto)
        if remove_break_line:
            # Substituir quebras de linha por espaços.
            texto = re.sub(r'\n', ' ', texto)
        
        if remove_final_s:
            # Substituir 's' no final de palavras por espaços, mantendo o comprimento.
            texto = re.sub(r's\b', ' ', texto)
        
        if add_space_firts:

            # Adiciona um espaço no inicio de todo texto
            texto = " " + texto

        if clean_spaces:
            # Neste caso, permitir que o tamanho do texto se altere, removendo espaços extras.
            texto = re.sub(r'\s+', ' ', texto).strip()
        else:
            # Ajustar espaços sem alterar o comprimento do texto.
            texto = re.sub(r'\s+', lambda match: ' ' * len(match.group(0)), texto)

        # Manter o texto em minúsculas.
        texto = texto.lower()

        # Ajustar o texto para garantir que ele tenha exatamente o mesmo número de caracteres que o original, se não estiver removendo espaços.
        if not clean_spaces:
            add_length = 0
            if (add_space_firts):
                add_length = 1
            texto = texto.ljust(original_length + add_length)[:original_length + add_length]

        return texto
    return texto

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
            message(f"Directory '{directory_path}' created successfully.")
        except OSError as error:
            message(f"Error creating directory '{directory_path}': {error}")

def get_old_files_by_percent(directory_path, sort_ascending=True, percentage=5):
    all_files = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    files_info = []

    for file in all_files:
        file_path = os.path.join(directory_path, file)
        last_modification_time = os.path.getmtime(file_path)
        last_modification_date = pd.to_datetime(last_modification_time, unit='s')
        files_info.append((file, last_modification_date))

    files_info.sort(key=lambda x: x[1], reverse=not sort_ascending)

    files_count = len(files_info)
    slice_count = max(1, int(int((percentage / 100.0) * files_count)))

    selected_files = [file_info[0] for file_info in files_info[:slice_count]]

    return selected_files

def create_or_read_df(path, columns):
    message(f"create_or_read_df")
    if (path_exist(path)):
        message(f"read file: {path}")
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=columns)
        message(f"create file: {path}")
        df.to_csv(path, index=False)
    
    return df

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
    message(file_path)
    return os.path.exists(file_path)

def find_in_text_with_wordlist(text, wordlist):
    match = None
    for word in wordlist:
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
        message("file path: " + path)
        file.write(str(text))

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


def download_images_in_parallel(image_urls, image_path, image_names):
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

def check_url_existence(url, timeout=5):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    try:
        response = requests.head(url, headers=headers, timeout=timeout)
        return 200 <= response.status_code < 300
    except Exception as e:
        message(e)
        return False

def check_urls_in_parallel(urls, timeout=5):
    results = []  # Lista para armazenar os resultados

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_url_existence, url, timeout): url for url in urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                exists = future.result()
                message(f"{url} exists: {exists}")
                results.append([url, exists])  # Adiciona a URL e o resultado à lista de resultados
            except Exception as e:
                message(f"{url} generated an exception: {e}")
                results.append([url, False])  # Assume que a URL não existe se uma exceção ocorrer

    return results

def delete_directory_and_contents(directory_path):
    if not os.path.exists(directory_path):
        message("Directory does not exist.")
        return

    shutil.rmtree(directory_path)
    message(f"Directory and all contents deleted: {directory_path}")

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

    message("First execution")

def is_price(string):
    if not isinstance(string, str):
        return False

    pattern = r"""
    (R\$\s?\d{1,3}(?:\.\d{3})*,\d{2})|  # BRL: R$
    (€\s?\d{1,3}(?:\.\d{3})*,\d{2})|    # EUR: €
    (\$\s?\d{1,3}(?:,\d{3})*\.\d{2})|   # USD: $
    (£\s?\d{1,3}(?:,\d{3})*\.\d{2})     # GBP: £
    """

    return bool(re.match(pattern, string, re.VERBOSE))

def read_csvs_on_dir_and_union(directory, get_only_last):
    # Usa glob para encontrar todos os arquivos CSV no diretório
    csv_files = glob(os.path.join(directory, '*.csv'))
    csv_files = sorted(csv_files, reverse=True)

    if get_only_last and csv_files:
        # Encontra o arquivo CSV mais recentemente modificado
        latest_file = csv_files[0]
        message(latest_file)
        return pd.read_csv(latest_file)
    elif csv_files:
        # Lê todos os arquivos CSV e os concatena em um único DataFrame
        dfs = [pd.read_csv(file) for file in csv_files]
        return pd.concat(dfs, ignore_index=True)
    else:
        message("Erro: no historical data")
        exit(1)

def read_file(file_path):
    """Reads a file and returns its contents as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("The file was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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

def calc_string_diff_in_df_col(title_x, title_y):
    distance = levenshtein(title_x, title_y)
    max_len = max(len(title_x), len(title_y))
    percent_diff = (distance / max_len) if max_len != 0 else 0
    return percent_diff

def calculate_statistics(lst):
    # Inicializa o resultado com valores máximos e mínimos
    statistics_result = {
        'maximum': max(lst) if lst else None,
        'minimum': min(lst) if lst else None,
        'mean': None,
        'standard_deviation': None
    }

    # Calcula a média se a lista não estiver vazia
    if lst:
        statistics_result['mean'] = statistics.mean(lst)

    # Calcula o desvio padrão apenas se houver dois ou mais elementos na lista
    if len(lst) >= 2:
        statistics_result['standard_deviation'] = statistics.stdev(lst)

    return statistics_result

def flatten_list(list_of_lists):
    if list_of_lists is None:
        return []

    flattened_list = []
    for element in list_of_lists:
        if isinstance(element, list):
            for subelement in element:
                flattened_list.append(subelement)
        else:
            flattened_list.append(element)
    return flattened_list

def get_all_dfs_in_dir(path, file):
    nome_arquivo = file + '.csv'

    dataframes = []

    for pasta_raiz, _, arquivos in os.walk(path):
        for nome_arquivo_encontrado in arquivos:
            if nome_arquivo_encontrado == nome_arquivo:
                caminho_completo = os.path.join(pasta_raiz, nome_arquivo_encontrado)
                df = pd.read_csv(caminho_completo)
                dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)
    return df
