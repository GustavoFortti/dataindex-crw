import os
import re
import csv
import json
import math
import base64
import hashlib
import unicodedata
import pandas as pd
from datetime import date, timedelta

DATE_FORMAT = "%d/%m/%Y"

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
    texto = unicodedata.normalize('NFKD', texto)
    # Mantém apenas caracteres alfanuméricos e espaços
    texto = u"".join([c for c in texto if not unicodedata.combining(c)])
    # Remove tudo que não for letra, número ou espaço
    return remove_spaces(re.sub(r'[^A-Za-z0-9 ]+', '', texto).lower())

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