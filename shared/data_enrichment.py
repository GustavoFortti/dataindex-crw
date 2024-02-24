import os
import re
import imagehash
import hashlib
import numpy as np
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
from copy import deepcopy

from utils.wordlist import BLACK_LIST, PRONOUNS
from utils.log import message
from utils.general_functions import (clean_text,
                                    path_exist,
                                    remove_spaces,
                                    calculate_statistics,
                                    flatten_list,
                                    save_file,
                                    list_directory,
                                    convert_image,
                                    read_file,
                                    calculate_precise_image_hash,
                                    create_directory_if_not_exists,
                                    find_in_text_with_word_list)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def process_data(conf, df):
    global CONF
    global WORD_LIST

    CONF = conf
    WORD_LIST = CONF['word_list']
    product_desc_tag = CONF['product_desc_tag']
    file_path = CONF['data_path']

    df = df.drop_duplicates(subset='ref').reset_index(drop=True)
    message("dataframe origin")
    print(df)
    print()

    message("filtro de nulos")
    df_nulos = df[df[['title', 'price', 'image_url']].isna().any(axis=1)]
    df_nulos.to_csv(file_path + "/origin_del.csv", index=False)
    df = df.dropna(subset=['title', 'price', 'image_url'])
    df = df.reset_index(drop=True)

    message("outros filtros")
    df['name'] = df['title'].str.lower()
    df['price'] = df['price'].str.replace('R$', '').str.replace(' ', '')
    df['brand'] = CONF['brand']
   
    df['price_numeric'] = df['price'].str.replace(',', '.').astype(float)
    df['title'] = df['title'].apply(clean_text)
    df['title'] = df['title'].apply(remove_spaces)
    
    message("criando coluna quantidade")
    pattern = r'(\d+([.,]\d+)?)\s*(kg|g|gr|gramas)\s*\w*'
    df[['quantity', 'unit']] = df['name'].apply(lambda text: find_pattern_for_quantity(text, pattern)).apply(pd.Series)
    df['quantity'] = df[['quantity', 'unit']].apply(convert_to_grams, axis=1)
    df['price_qnt'] = df.apply(relation_qnt_price, axis=1)
    df['quantity'] = df['quantity'].astype(str).replace("-1", np.nan)

    message("removendo produtos da blacklist")
    df = df[~df['title'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]

    spec_title = find_keywords(df=df, file_path=file_path, column="title")
    spec_route = find_keywords(df=df, file_path=file_path, product_desc_tag=product_desc_tag)
    spec = find_keywords(df=df, file_path=file_path)

    df = processing_keywords(df, spec_title, spec_route, spec)

    df = df.dropna(subset=["ref", "title", "price", "image_url", "product_url"], how="any")

    print(df.info())

    image_processing(df, file_path)
    
    df = df[['ref', 'title', 'price', 'image_url', 'product_url', 'ing_date',
            'name', 'brand', 'price_numeric', 'quantity', 'price_qnt', 'spec_5',
            'spec_4', 'spec_3', 'spec_2', 'spec_1']]
    
    return df

def processing_keywords(df, spec_title, spec_route, spec):
    df["spec_5"] = None
    df["spec_4"] = None
    df["spec_3"] = None
    df["spec_2"] = None
    df["spec_1"] = None

    for ref in df["ref"]:
        
        spec_title_route = combine_and_sum_scores(spec_title[ref], spec_route[ref])
        spec_all = combine_and_sum_scores(spec_title_route, spec[ref])
        spec_reduced = [i['subject'] for i in spec_all[:5]]

        for index, item in enumerate(spec_reduced):
            reversed_index = 5 - index
            df.loc[df["ref"] == ref, "spec_" + str(reversed_index)] = " ".join(item)
    
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

def find_keywords(df, file_path=None, product_desc_tag=None, column=None):
    refs = {}
    for index, ref in enumerate(df["ref"]):
        keywords = []
        page_path = f"{file_path}/products/{ref}.txt"
        file_exist = path_exist(page_path)
        matchs = None
        if (column != None):
            text = df[df['ref'] == ref][column].values[0]
            matchs = find_matches(text, is_substring=True, score_by_index=True)

        elif ((product_desc_tag != None) & (file_exist)):
            text_html = read_file(page_path)

            if (not text_html):
                keywords.append(None)
                continue
            matchs = find_keyword_in_text_html_with_tag(text_html, product_desc_tag)
            

        elif (file_exist):
            text_html = read_file(page_path)

            if (not text_html):
                keywords.append(None)
                continue
            
            text_html = clear_page(text_html)
            matchs = find_matches(text_html)

        if (matchs):
            keywords.append(matchs)
        else:
            keywords = None

        refs[ref] = flatten_list(keywords)

    return refs

def find_keyword_in_text_html_with_tag(text_html, locations):
    soup = BeautifulSoup(text_html, 'html.parser')
    keywords = []
    for location in locations[:]:
        tag = soup.find(location['tag'], class_=location['class'])
        if (tag == None): continue
        matches = find_matches(tag.text, score_by_index=True)
        if (not matches):
            continue
        
        keywords += matches
        
    if (not keywords):
        return None
    
    return keywords

def find_matches(text, limit_words=10, is_substring=False, score_by_index=False):
    text = clean_text(text, False)
    text_words_size = len(text.split())
    text_char_size = len(text)
    keywords = {}

    for value, subject in enumerate(WORD_LIST):
        scores = []
        score = 0
        matches = None
        key = " ".join(subject)
        text_temp = deepcopy(text)
        for word in subject:
            word_clean = r'\b' + re.escape(clean_text(word, False)) + r'\b'
            if (is_substring):
                word_clean = clean_text(word, False)

            if (score_by_index):
                matches = re.finditer(word_clean, text_temp)
                for match in matches:
                    score += abs((match.start() / text_char_size) - 1)
                if (is_substring):
                    text_temp = text_temp.replace(word, (len(word) * "*"))
            else:
                matches = re.findall(word_clean, text_temp)
                score = len(matches) / text_words_size

        if (matches):
            scores.append(score)
        keywords[key] = {"subject": subject, "score": sum(scores)}
                
    keywords = sorted(keywords.values(), key=lambda x: x['score'], reverse=True)
    keywords = [x for x in keywords if x['score'] != 0]

    if (keywords == []):
        return None
    
    return keywords

def clear_page(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    remove_tags = ['header', 'footer', 'fieldset', 'select', 'script', 'style', 'iframe', 'svg', 'img', 'link', 'button', 'noscript']
    for remove_tag in remove_tags:
        for tag in soup.find_all(remove_tag):
            tag.decompose()

    tags_com_hidden = soup.find_all(lambda tag: tag.get('class') and 'hidden' in ' '.join(tag.get('class')))
    for tag in tags_com_hidden:
        tag.extract()
        
    def remove_empty_tags(tag):
        if not tag.text.strip():
            tag.extract()

    for tag in soup.find_all():
        remove_empty_tags(tag)

    tags_with_char_count = [(tag, len(tag.get_text(strip=True))) for tag in soup.find_all()]
    sorted_tags = sorted(tags_with_char_count, key=lambda x: x[1], reverse=True)
    half_count = int(len(sorted_tags) // 3)

    for tag, _ in sorted_tags[half_count:]:
        tag.decompose()

    page_texts = soup.get_text().split("\n\n")
    page_texts = " ".join([clean_text(i, False).replace("\n", " ").replace("  ", "") for i in page_texts if i != ''])

    return page_texts

def remove_prepositions_pronouns(text):
    pronouns = set(PRONOUNS[CONF['country']])

    for pronoun in pronouns:
        text = text.replace(pronoun, "")
    
    return text

def find_pattern_for_quantity(text, pattern):
    pattern = r'(\d+[.,]?\d*)\s*(kg|g|gr|gramas)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    quantity = None
    if ((len(matches) == 1)): 
        quantity, unit = matches[0]
        quantity = float(str(quantity).replace(',', '.'))
    
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

def replace_empty_list_with_none(element):
    if isinstance(element, list) and not element:
        return None
    return element

def create_range_list(statistics_dict):
    if not statistics_dict:
        return []

    std_dev = statistics_dict.get("standard_deviation", 0) or 0

    mean = statistics_dict.get("mean", 0)

    range_list = [
        statistics_dict.get("maximum"),
        mean - std_dev,
        mean + std_dev,
        statistics_dict.get("minimum")
    ]

    range_list = [x for x in range_list if x is not None]

    return range_list