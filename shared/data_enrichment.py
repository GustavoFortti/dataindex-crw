import os
import re
import imagehash
import hashlib
import numpy as np
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup

from utils.wordlist import BLACK_LIST
from utils.general_functions import (clean_text,
                                 path_exist,
                                 remove_spaces,
                                 save_file,
                                 list_directory,
                                 convert_image,
                                 calculate_precise_image_hash,
                                 loading,
                                 create_directory_if_not_exists,
                                 find_in_text_with_word_list)

pd.set_option('display.max_rows', None)

def process_data(conf):
    global CONF
    global WORD_LIST

    CONF = conf
    WORD_LIST = CONF['word_list']
    locations = CONF['location_type_product']
    file_path = CONF['data_path']

    df = pd.read_csv(file_path + "/origin.csv")
    df = df.drop_duplicates(subset='product_url').reset_index(drop=True)

    df_nulos = df[df[['title', 'price', 'image_url']].isna().any(axis=1)]
    df_nulos.to_csv(file_path + "/origin_del.csv", index=False)

    df = df.dropna(subset=['title', 'price', 'image_url'])
    df = df.reset_index(drop=True)

    df['name'] = df['title'].str.lower()
    df['price'] = df['price'].str.replace('R$', '').str.replace(' ', '')
    df['brand'] = CONF['brand']
   
    df['price_numeric'] = df['price'].str.replace(',', '.').astype(float)
    df['title'] = df['title'].apply(clean_text)
    df['title'] = df['title'].apply(remove_spaces)
    
    pattern = r'(\d+([.,]\d+)?)\s*(kg|g|gr|gramas)\s*\w*'
    df[['quantity', 'unit']] = df['name'].apply(lambda text: find_pattern_for_quantity(text, pattern)).apply(pd.Series)
    df['quantity'] = df[['quantity', 'unit']].apply(convert_to_grams, axis=1)
    df['price_qnt'] = df.apply(relation_qnt_price, axis=1)
    df['quantity'] = df['quantity'].astype(str).replace("-1", np.nan)

    # pattern = r'(\d+)\s*(caps|cap|vcaps|capsules|comprimidos|comps|comp|capsulas|soft|softgel)\b'
    # df[['quantity_formato', 'formato']] = df['name'].apply(lambda text: find_pattern_for_quantity(clean_text(text), pattern)).apply(pd.Series)
    # df['formato'] = df['formato'].apply(replace_for_comprimidos)

    df = df[~df['title'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]
    df = keywords_page_specification(df, file_path, locations)
    df = df.dropna(subset=["ref", "title", "price", "image_url", "product_url"], how="any")

    image_processing(df, file_path)
    df = df[['ref', 'title', 'price', 'image_url', 'product_url', 'ing_date',
            'name', 'brand', 'price_numeric', 'quantity', 'price_qnt',
            'spec', 'spec_route']]
    
    return df

def keywords_page_specification(df, file_path, locations):
    products_path = f"{file_path}/products"

    df['spec_route'] = None
    for index, ref in enumerate(df["ref"]):
        loading(index, len(df))
        page_path = f"{products_path}/{ref}.txt"
        keywords_path = f"{products_path}/{ref}_spec.txt"
        
        if path_exist(page_path):
            product_keywords_path = page_path
        else:
            continue            
        
        try:
            with open(product_keywords_path, 'r') as product_file:
                product = product_file.read()
                keywords = []
                
                if (product):
                    soup = BeautifulSoup(product, 'html.parser')
                    for location in locations:
                        tag = soup.find(location['tag'], class_=location['class'])
                        if (tag == None): continue
                        keywords = find_matches(tag.text, 3)
                        
                        if (keywords != []): break
                else:
                    keywords = ''

                df.loc[df['ref'] == ref, 'spec_route'] = keywords
                with open(keywords_path, 'w') as new_file:
                    new_file.write(keywords)
        except:
            df.loc[df['ref'] == ref, 'spec_route'] = None

    print()
    keywords_page(df, file_path)
    print()
    df['spec'] = df.apply(lambda row: None if row['spec_route'] is not None else row['spec'], axis=1)

    return df

def keywords_page(df, file_path):
    products_path = f"{file_path}/products"

    df['spec'] = ""
    for index, ref in enumerate(df["ref"]):
        loading(index, len(df))
        text_path = f"{products_path}/{ref}_text.txt"
        page_path = f"{products_path}/{ref}.txt"
        text_exist = path_exist(text_path)
        
        try:
            product_text_path = text_path if text_exist else page_path

            with open(product_text_path, 'r') as product_file:
                product = product_file.read()

                if (not text_exist):
                    product = clear_page(product)
                    product = ' '.join(product.split())

                words = best_words(product)
                df.loc[df['ref'] == ref, 'spec'] = words

                with open(text_path, 'w') as new_file:
                    new_file.write(product)
        except:
            df.loc[df['ref'] == ref, 'spec'] = None
            print("")
            print("error file: " + str(ref))
            print("")

    return df

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

    return soup.get_text()

def best_words(text):
    text = clean_text(text)

    words_count = {}
    for item in WORD_LIST:
        for sub_item in item:
            count = len(re.findall(clean_text(sub_item), text))
            if (count != 0):
                words_count[sub_item] = count
                break

    if (words_count == {}):
        return None

    words_count = dict(sorted(words_count.items(), key=lambda item: item[1], reverse=True))
    limit = int(list(words_count.values())[0] * 0.30)
    words = ""
    limit_size = 3
    for item, value in words_count.items():
        if ((value >= limit) & (limit_size > 0)): 
            limit_size -= 1
            words += f" {item}"
        else: break

    return words

def find_matches(text, max_size=10):
    text = clean_text(text)
    keywords = []
    
    for item in WORD_LIST:
        for sub_item in item:
            word = clean_text(sub_item)
            if (re.search(word, text)):
                keywords.append(word)
                break

    if (keywords):
        keywords = keywords[:max_size] if (len(keywords) > max_size) else keywords
        return ' '.join(keywords)
    return None

def create_table(soup):
    try:
        dfs = []
        tables = soup.find_all('table')
        for table in tables:
            table_data = []

            # Loop pelas linhas da tabela
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                data_row = [cell.text.strip() for cell in cells]
                table_data.append(data_row)

            # Remova as linhas vazias
            table_data = [row for row in table_data if row]

            # Verifique se há dados suficientes para criar um DataFrame
            if len(table_data) > 1 and all(len(row) == len(table_data[0]) for row in table_data):
                # A primeira linha contém os cabeçalhos das colunas
                columns = table_data[0]
                
                # Os dados reais começam na segunda linha
                data = table_data[1:]
                
                # Criar um DataFrame pandas a partir dos dados
                df = pd.DataFrame(data, columns=columns)
                
                # Exibir o DataFrame
                primeira_coluna = df['A']
                for valor in primeira_coluna:
                    comando = f'echo {valor}>>./wordlist.txt'
                    os.system(comando)

                dfs.append(df)
            else:
                print("Não há dados suficientes para criar um DataFrame.")

            return dfs
    except:
        return None

def create_table_2(soup):
    try: 
        tables = []
        tags = [tag for tag in soup.find_all() if any(re.search(r'\b(tabela|table)\b', class_, re.IGNORECASE) for class_ in tag.get('class', []))]
        for tag in tags:
            body_el = tag.find_all(recursive=False)
            for table_el in body_el:
                table = []
                rows_el = table_el.find_all(recursive=False)
                for row_el in rows_el:
                    row = row_el.find_all()
                    table.append([(clean_text(col.text)) for col in row])
                tables.append(table)

        dfs = []
        for table in tables:
            data = []
            if (len(table) > 1):
                for row in table:
                    if (len(row) == 3):
                        data.append(row)
                        palavra = row[0]
                        comando = f'echo {palavra}>>./wordlist.txt'
                        os.system(comando)

            df = pd.DataFrame(data)
            dfs.append(df)

        return dfs
    except:
        return None
    
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
    path_img_tmp = data_path + "/img_tmp/"
    path_img_hash = data_path + "/img_hash/"
    path_img_csl = data_path + "/img_csl/"
    create_directory_if_not_exists(path_img_hash)
    create_directory_if_not_exists(path_img_csl)

    refs = sorted(df['ref'])
    dict_imgs = {i.split(".")[0]: i for i in list_directory(path_img_tmp)}
    dict_imgs = dict(sorted(dict_imgs.items(), key=lambda item: item[1]))
    
    if (not (list(dict_imgs.keys()) == refs)):
        print("ERROR IMAGE PROCESSING")
        exit(1)

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
        loading(index, len(df))

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
        manipulating_image(img_path, save_path)

def manipulating_image(img_path, save_path, img_format='webp'):
    
    convert_image(img_path, save_path, img_format)