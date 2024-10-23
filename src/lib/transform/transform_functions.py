import os
import re
from copy import deepcopy

import imagehash
import numpy as np
import pandas as pd
from PIL import Image

from src.lib.utils.dataframe import read_and_stack_historical_csvs_dataframes, read_df
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       list_directory, path_exists, save_file)
from src.lib.utils.image_functions import (calculate_precise_image_hash,
                                           convert_image)
from src.lib.utils.log import message
from src.lib.utils.text_functions import (clean_text,
                                          find_in_text_with_wordlist,
                                          remove_spaces)
from src.lib.wordlist.wordlist import BLACK_LIST


def ensure_columns_exist(df, columns):
    for column in columns:
        if column not in df.columns:
            df[column] = np.nan  # Adiciona a coluna com valores NaN (nulos)
    return df

def filter_nulls(df):
    """Filter rows with null values in specific columns and save them to a CSV file."""
    return df.dropna(subset=['title', 'price', 'image_url']).reset_index(drop=True)

def apply_generic_filters(df, conf):
    """Apply various data cleaning and transformation filters."""
    df['title_extract'] = df['title']
    df['name'] = df['title'].str.lower()
    df['price'] = df['price'].str.replace('R$', '').str.replace(' ', '')
    df['brand'] = conf['brand']
    df['page_name'] = conf['page_name']
    df['price_numeric'] = df['price'].str.replace(',', '.').astype(float)
    df['title'] = df['title'].apply(clean_text).apply(remove_spaces)
    return df

def apply_platform_data(df, conf):
    df['cupom_code'] = conf['cupom_code']
    df['discount_percent_cupom'] = conf['discount_percent_cupom']
    df['tail_platform_link'] = None
    if (conf['tail_platform_link']):
        df['tail_platform_link'] = df["product_url"] + conf['tail_platform_link']
    
    return df

def create_quantity_column(df):
    """Extract and convert quantity information into a uniform format."""
    # Garantir que sempre retornamos dois elementos para evitar o erro de tamanho de coluna
    df['quantity_unit'] = df['name'].apply(lambda text: find_pattern_for_quantity(text))

    # Separar a coluna 'quantity_unit' em 'quantity' e 'unit'
    df[['quantity', 'unit_of_measure']] = pd.DataFrame(df['quantity_unit'].tolist(), index=df.index)

    # Aplicar conversão para gramas
    df['quantity'] = df[['quantity', 'unit_of_measure']].apply(convert_to_grams, axis=1)
    
    # Calcular o preço por quantidade
    df['price_qnt'] = df.apply(relation_qnt_price, axis=1)
    
    # Substituir valores inválidos por NaN
    df['quantity'] = df['quantity'].astype(str).replace("-1", np.nan)
    
    return df

def remove_blacklisted_products(df):
    """Remove products based on a blacklist."""
    return df[~df['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))]

def find_pattern_for_quantity(text):
    # Adicionar unidades de medida líquidas (ml e l) e também caps/comps
    pattern = r'(\d+[.,]?\d*)\s*(kg|g|gr|gramas|ml|l|litro|litros|cápsula|capsula|capsule|cap|caps|comprimido|comp|comps)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    quantity, unit = None, None
    if len(matches) == 1:
        quantity, unit = matches[0]
        quantity = str(quantity).replace(',', '.')
        
        # Ajustar unidades de gramas e mililitros para números inteiros quando necessário
        if unit in ['g', 'gr', 'gramas', 'ml'] and "." in quantity:
            quantity = quantity.replace(".", "")
        
        quantity = float(quantity)
        
        # Verificar se há múltiplos de unidades, como "3x"
        padrao = r'(\d+)x'
        matches_multiply = re.findall(padrao, text)
        if len(matches_multiply) == 1 and quantity is not None:
            quantity *= float(matches_multiply[0])

    return quantity, unit

def convert_to_grams(row):
    value = row['quantity']
    unit = row['unit_of_measure']
    
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
        difference = set(dict_imgs.keys()) - set(refs)
        message(difference)
        raise Exception("ERROR IMAGE PROCESSING")

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
        if path_exists(path_ref_img_hash):
            
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
    
def filter_df_price_when_alter_price(df, refs):
    for ref in refs:
        df_temp = df[df["ref"] == ref].sort_values('ing_date')
        
        last_price = False
        for idx, row in df_temp.iterrows():
            price = row['price_numeric']
            is_alter_price = False
            
            if ((not last_price) | bool(last_price != price)):
                last_price = price
                is_alter_price = True
                
            df.loc[idx, "is_alter_price"] = is_alter_price
    
    df = df[df['is_alter_price']]
    return df

def create_price_discount_percent_col(df, data_path):
    df_new = deepcopy(df)
    
    refs = df['ref'].values

    path = f"{data_path}/history"
    df_temp = read_and_stack_historical_csvs_dataframes(path, False, dtype={'ref': str})

    if (df_temp.empty):
        df["price_discount_percent"] = 0
        df["compare_at_price"] = None
        
        return df
    
    df_temp = df_temp[df_temp["ref"].isin(refs)]
    df_price = pd.concat([df, df_temp], ignore_index=True)
    
    df_price_temp = filter_df_price_when_alter_price(df_price, refs)
    df_price_temp = df_price_temp[['ref', 'price_numeric', 'ing_date']]

    refs_processed = []
    
    for idx, row in df_price_temp.iterrows():
        ref = row['ref']
        if (ref in refs_processed):
            continue
        
        refs_processed.append(ref)
        
        df_price_temp_sorted = df_price_temp[df_price_temp["ref"] == ref].sort_values('ing_date', ascending=False)
        prices = df_price_temp_sorted["price_numeric"].values
        
        price_discount_percent = 0.0
        compare_at_price = None
        if (len(prices) > 1):
            price_discount_percent = round((prices[0] / prices[1]), 2)
            if (price_discount_percent < 1.0):
                compare_at_price = prices[1]
                price_discount_percent = 0.0
            
        df_new.loc[df_new['ref'] == ref, "price_discount_percent"] = price_discount_percent
        df_new.loc[df_new['ref'] == ref, "compare_at_price"] = compare_at_price

    return df_new

def create_history_price_col(df, conf):
    df_history = read_df(f"{conf['src_data_path']}/history_price/history_price_csl.csv")
    df_history = df_history[df_history['brand'] == conf['brand']]
    df_history = df_history[['ref', 'prices']]
    
    df = pd.merge(df, df_history, on='ref', how='left')

    return df