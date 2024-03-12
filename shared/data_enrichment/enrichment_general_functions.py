import os
import re
import ast
import imagehash
import hashlib

import numpy as np
import pandas as pd

from PIL import Image
from bs4 import BeautifulSoup
from copy import deepcopy
from sklearn.preprocessing import MinMaxScaler

from utils.log import message

from utils.general_functions import (
    clean_text,
    path_exist,
    remove_spaces,
    flatten_list,
    save_file,
    list_directory,
    convert_image,
    read_file,
    calculate_precise_image_hash,
    create_directory_if_not_exists,
    find_in_text_with_wordlist
)

from utils.wordlist import (
    BLACK_LIST, 
    PRONOUNS,
    get_word_index_in_text,
    find_subject_in_wordlist
)

def find_pattern_for_quantity(text):
    pattern = r'(\d+[.,]?\d*)\s*(kg|g|gr|gramas)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    quantity = None
    if ((len(matches) == 1)): 
        quantity, unit = matches[0]
        quantity = str(quantity).replace(',', '.')

        if ((unit in ['g', 'gr', 'gramas']) & ("." in quantity)):
            quantity = quantity.replace(".", "")

        quantity = float(quantity)
    
        padrao = r'\d+x'
        matches_multiply = re.findall(padrao, text)
        if ((len(matches_multiply) == 1) & (quantity != None)):
            quantity = quantity * float(matches_multiply[0].replace('x', ''))
        
        return quantity, unit
    
    return None, None

def convert_to_grams(row):
    value = row['quantity']
    unit = row['unit']
    
    if pd.notna(value):
        if unit in ['kg']:
            value = float(value) * 1000
        try:
            value = int(float(value))
        except ValueError:
            pass
    else:
        value = -1
    
    return value

def replace_for_comprimidos(texto):
    palavras_substituir = ['caps', 'cap', 'vcaps', 'capsulas', 'capsules', 'comprimidos', 'comps', 'comp', 'capsulas', 'soft', 'softgel']
    if pd.notna(texto):
        for palavra in palavras_substituir:
            if clean_text(palavra) in clean_text(texto):
                return 'comprimidos'
    return texto

def relation_qnt_price(row):
    resultado = (row['price_numeric'] / row['quantity']) if (row['quantity'] > 0) else -1
    if resultado < 0:
        return np.nan
    return round(resultado, 3)

def image_processing(df, data_path):
    message("image_processing")
    path_img_tmp = data_path + "/img_tmp/"
    path_img_hash = data_path + "/img_hash/"
    path_img_csl = data_path + "/img_csl/"
    create_directory_if_not_exists(path_img_hash)
    create_directory_if_not_exists(path_img_csl)

    refs = sorted(df['ref'])

    dict_imgs = {i.split(".")[0]: i for i in list_directory(path_img_tmp) if i.split(".")[0] in refs}
    dict_imgs = dict(sorted(dict_imgs.items(), key=lambda item: item[1]))

    if (not set(dict_imgs.keys()).issubset(refs)):
        print("ERROR IMAGE PROCESSING")
        difference = set(dict_imgs.keys()) - set(refs)
        print(difference)
        exit(1)

    message("LOADING IMAGES")
    def describe_image(image, img_path):
        width, height = image.size
        file_size = os.path.getsize(img_path)  
        return {
            "dimensions": (width, height),
            "size": file_size,
            "img_path": img_path
        }
    
    images_info = {}

    for index, (ref, img_file_name) in enumerate(dict_imgs.items()):
        img_path = path_img_tmp + img_file_name
        image = Image.open(img_path)
        new_image_hash = calculate_precise_image_hash(img_path)
        new_image_hash = imagehash.hex_to_hash(new_image_hash)

        path_ref_img_hash = path_img_hash + ref + ".txt"
        if path_exist(path_ref_img_hash):
            
            with open(path_ref_img_hash, "r") as file:
                old_image_hash_str = file.read()
                old_image_hash = imagehash.hex_to_hash(old_image_hash_str)

            if new_image_hash != old_image_hash:
                save_file(new_image_hash, path_ref_img_hash)
                images_info[ref] = describe_image(image, img_path)
        else:
            save_file(new_image_hash, path_ref_img_hash)
            images_info[ref] = describe_image(image, img_path)
    
    for ref, image_info in images_info.items():
        save_path = path_img_csl + ref
        img_path = image_info["img_path"]
        convert_image(img_path, save_path)
    message("Images processing ok")

def normalize_spec_columns(df, size_specs):
    columns = []
    for col in range(size_specs):
        columns.append("spec_" + str(col + 1))

    for col in columns:
        spects_to_string = lambda row: " ".join(ast.literal_eval(row)) if not pd.isna(row) else None
        df[col] = df[col].apply(spects_to_string)
        
    return df

def create_spec_columns_with_keywords(df, spec_title, spec_route, spec, size_specs):
    for col in range(size_specs):
        df["spec_" + str(col + 1)] = None
        df["spec_" + str(col + 1) + "_score"] = None

    for ref in df["ref"]:
        
        spec_title_route = combine_and_sum_scores(spec_title[ref], spec_route[ref])
        spec_all = combine_and_sum_scores(spec_title_route, spec[ref])
        spec_reduced = [i for i in spec_all[:size_specs]]

        for index, item in enumerate(spec_reduced):
            df.loc[df["ref"] == ref, "spec_" + str(index + 1) ] = str(item['subject'])
            df.loc[df["ref"] == ref, "spec_" + str(index + 1) + "_score"] = str(item['score'])
    
    return df

def combine_and_sum_scores(list1, list2):
    list1_sets = [{tuple(sorted(item['subject'])): item['score']} for item in list1]
    list2_sets = [{tuple(sorted(item['subject'])): item['score']} for item in list2]

    combined = {}

    for item in list1_sets:
        for subjects, score in item.items():
            combined[subjects] = combined.get(subjects, 0) + score

    for item in list2_sets:
        for subjects, score in item.items():
            combined[subjects] = combined.get(subjects, 0) + score

    result = [{'subject': list(subject), 'score': score} for subject, score in combined.items()]

    return result

def filter_unique_elements_from_dict(data, column):
    unique_elements = {}

    for key, value in data.items():
        location = value[column]
        if location not in unique_elements:
            unique_elements[location] = (key, value)

    return {key: value for key, value in unique_elements.values()}