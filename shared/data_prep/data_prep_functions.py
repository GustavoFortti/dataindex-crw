import re
import numpy as np
import pandas as pd
import imagehash
from PIL import Image

from utils.log import message

from utils.general_functions import (
    clean_text,
    remove_spaces,
    find_in_text_with_wordlist,
    path_exist,
    calculate_precise_image_hash,
    create_directory_if_not_exists,
    list_directory,
    save_file,
    convert_image
)

from shared.data_prep.product_def_prep import load_product_def_prep

from utils.wordlist import (
    BLACK_LIST, 
)

def create_product_def_cols(df, conf):
    message("criada colunas de definição do produto")

    product_def_path = conf['product_def_path']

    message("Load_models_prep")
    load_product_def_prep(df, conf)

    path_product_def = f"{product_def_path}/product_def.csv"
    path_product_def_predicted = f"{product_def_path}/product_def_predicted.csv"

    if ((path_exist(path_product_def)) & (path_exist(path_product_def_predicted))):

        df_product_def = pd.read_csv(path_product_def)
        df_product_def_predicted = pd.read_csv(path_product_def_predicted)
        
        df = pd.merge(df, df_product_def, on='ref', how='left')
        df = pd.merge(df, df_product_def_predicted, on='ref', how='left')
    else:
        message("execute _set_product_def_ para criar os arquivos de definição do produto")
        df['product_def'] = None
        df['product_def_pred'] = None

    return df

def filter_nulls(df, data_path):
    """Filter rows with null values in specific columns and save them to a CSV file."""
    df_nulos = df[df[['title', 'price', 'image_url']].isna().any(axis=1)]
    df_nulos.to_csv(data_path + "/origin_del.csv", index=False)
    return df.dropna(subset=['title', 'price', 'image_url']).reset_index(drop=True)

def apply_generic_filters(df, conf):
    """Apply various data cleaning and transformation filters."""
    df['name'] = df['title'].str.lower()
    df['price'] = df['price'].str.replace('R$', '').str.replace(' ', '')
    df['brand'] = conf['brand']
    df['price_numeric'] = df['price'].str.replace(',', '.').astype(float)
    df['title'] = df['title'].apply(clean_text).apply(remove_spaces)
    return df

def create_quantity_column(df):
    """Extract and convert quantity information into a uniform format."""
    df[['quantity', 'unit']] = df['name'].apply(lambda text: find_pattern_for_quantity(text)).apply(pd.Series)
    df['quantity'] = df[['quantity', 'unit']].apply(convert_to_grams, axis=1)
    df['price_qnt'] = df.apply(relation_qnt_price, axis=1)
    df['quantity'] = df['quantity'].astype(str).replace("-1", np.nan)
    return df

def remove_blacklisted_products(df):
    """Remove products based on a blacklist."""
    return df[~df['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))]

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