import html2text
import pandas as pd
from bs4 import BeautifulSoup

from src.lib.extract.extract import products_metadata_update_old_pages_by_ref
from src.lib.extract.page_elements import Page
from src.lib.utils.file_system import (delete_file, path_exists, read_file,
                                       save_file)
from src.lib.utils.log import message
from src.lib.utils.text_functions import clean_text
from src.lib.wordlist.wordlist import get_back_words, get_word_index_in_text
from src.lib.utils.dataframe import read_df


def load_product_definition(df, conf):
    message("RUNNING MODEL PREP...")
    global CONF
    global WORDLIST
    global DATA_PATH
    global FILE_PATH_PRODUCT_METADATA

    CONF = conf
    WORDLIST = conf["wordlist"]
    DATA_PATH = CONF["data_path"]

    FILE_PATH_PRODUCT_METADATA = CONF["path_products_metadata_transform"]
    message("Extrai palavras chave das paginas dos produtos")
    keywords_data = extract_keywords_from_products(df, conf)

    delete_file(FILE_PATH_PRODUCT_METADATA)

    for idx, row in df.iterrows():
        ref = row['ref']
        message(f"prepere data {ref}")

        generates_and_stacks_product_metadata_by_ref(ref, keywords_data)

def generates_and_stacks_product_metadata_by_ref(ref, keywords_data):
    title_keywords = keywords_data[ref][0]
    valid_keywords, others_keywords = treat_relationship_between_keywords(title_keywords)
    excluded_title_keywords = keywords_data[ref][1:]

    if valid_keywords:
        for contained in (True, False):
            dfs_temp = [create_product_metadata_dataframe(keywords, valid_keywords, ref, contained, index) for index, keywords in enumerate(excluded_title_keywords)]
            df_product_ref_info = pd.concat(dfs_temp, ignore_index=True)
            df_product_ref_info['target'] = int(contained)

            append_new_df_and_save(FILE_PATH_PRODUCT_METADATA, df_product_ref_info)
    else:
        dfs_temp = [create_product_metadata_dataframe(keywords, [], ref, False, index) for index, keywords in enumerate(excluded_title_keywords)]
        df_product_ref_info = pd.concat(dfs_temp, ignore_index=True)
        df_product_ref_info['target'] = -1
        append_new_df_and_save(FILE_PATH_PRODUCT_METADATA, df_product_ref_info)

def create_product_metadata_dataframe(keywords, subjects, ref, contained, index):
    product_ref_info = [
        {
            "ref": ref, 
            "back_word": keyword['back_words'], 
            "subject": keyword['subject'],
            "location": int(keyword['location']), 
            "word_number": int(keyword['word_number']),
            "document_size": int(keyword['document_size']),
            "document_index": int(index),
            "brand": CONF['brand']
        } 
        for keyword in keywords.values()
        if (keyword['subject'] in subjects) == contained 
    ]

    df = pd.DataFrame(product_ref_info)

    if df.empty:
        return pd.DataFrame(columns=df.columns)
    
    split_columns = df['back_word'].apply(pd.Series)
    split_columns = split_columns.reindex(columns=range(5), fill_value=None)
    split_columns.columns = ['word_5', 'word_4', 'word_3', 'word_2', 'word_1']

    df = pd.concat([df.drop('back_word', axis=1), split_columns], axis=1)
    df = shift_words(df, split_columns.columns)

    return df

def shift_words(df, columns):
    for col in columns:
        if df[col].dtype != 'object':
            df[col] = df[col].astype('object')

    def shift_words_to_right(row):
        words = [row[col] for col in columns]
        filtered_words = [w for w in words if pd.notna(w)]
        none_filled = [None] * (len(columns) - len(filtered_words))
        return none_filled + filtered_words

    for index, row in df.iterrows():
        new_words = shift_words_to_right(row)
        for i, col in enumerate(columns):
            df.at[index, col] = new_words[i]

    return df

def treat_relationship_between_keywords(keywrods):
    if (keywrods == {}):
        return False, False
    
    subjects_keywords = list(set([keyword['subject'] for keyword in keywrods.values()]))
    valid_keywords = []
    others_keywords = []
    for subject_keywords in subjects_keywords:
        subject = WORDLIST[subject_keywords]

        if ((subject['product']) &
            (not bool(set(subject['conflict']).intersection(subjects_keywords)))):
            valid_keywords.append(subject_keywords)
            continue

        others_keywords.append(subject_keywords)

    return valid_keywords, others_keywords

def extract_keywords_from_products(df, conf):
    keywords_data = {}
    document_from_tag_count = 3
    for idx, row in df.iterrows():
        ref = str(row['ref'])
        title = row['title']

        products_path = f"{DATA_PATH}/products"
        description_path = f"{DATA_PATH}/products/{ref}_description.txt"
        page_path = f"{products_path}/{ref}.txt"

        html_text = read_file(page_path)
        document_from_tag_flag = True
        if (html_text == None):
            url = row['product_url']
            products_metadata_update_old_pages_by_ref(conf, Page, url)
            html_text = read_file(page_path)
            document_from_tag_flag = False
            
        product_documents = []

        product_documents.append(title)
        
        document_from_tag = [extract_subject_from_html_text(html_text, tag_map) for tag_map in CONF["product_definition_tag_map"]]
        document_from_tag = list(filter(lambda elemento: elemento is not None, document_from_tag))
        
        if ((document_from_tag == []) & (document_from_tag_flag)):
            message(f"extract products_metadata_update_old_pages_by_ref {ref} - {title}")
            url = row['product_url']
            products_metadata_update_old_pages_by_ref(conf, Page, url)
            
            html_text = read_file(page_path)
            document_from_tag = [extract_subject_from_html_text(html_text, tag_map) for tag_map in CONF["product_definition_tag_map"]]
            document_from_tag = list(filter(lambda elemento: elemento is not None, document_from_tag))
        
        description_document_from_tag = [desc for desc in [get_product_description(html_text, tag_map) for tag_map in CONF["product_description_tag_map"]] if desc is not None]
        if (len(description_document_from_tag) >= 1):
            save_file(description_document_from_tag[0], description_path)
        
        if (document_from_tag == []):
            message(f"A tag especificada está pode estar desatualizada. - CONTAGEM PARA ERRO {document_from_tag_count}")
            document_from_tag_count -= 1
        
        if (document_from_tag_count == 0):
            raise ValueError("A tag especificada está desatualizada.")
        
        product_documents.extend(document_from_tag)

        text_from_html = extract_subject_from_html_text(html_text)
        product_documents.append(text_from_html)

        keywords_info = [get_keywords_info(document, index) for index, document in enumerate(product_documents)]
        keywords_data[ref] = keywords_info
    
    return keywords_data

def get_keywords_info(document, index):
    documents_accents = clean_text(document, False, False, False, False, True)
    documents_cleaned = clean_text(document, False, False, False, True, True)

    first_doc = False
    if (index == 0):
        first_doc = True

    keywords_info = {}
    for key, value in WORDLIST.items():
        subject = value['subject']

        for word in subject:
            locations = get_word_index_in_text(word, documents_cleaned, first_doc)
            if (locations != []):
                loc_back_words = get_back_words(documents_accents, locations)

                for location, back_words in zip(locations, loc_back_words):

                    keywords_info[f"{word}_{location}"] = {}
                    keywords_info[f"{word}_{location}"]["location"] = location
                    keywords_info[f"{word}_{location}"]["word_number"] = len(documents_cleaned[:location].split())
                    keywords_info[f"{word}_{location}"]["size_word"] = len(word)
                    keywords_info[f"{word}_{location}"]["subject"] = key
                    keywords_info[f"{word}_{location}"]["back_words"] = back_words[-5:]
                    keywords_info[f"{word}_{location}"]["document_size"] = len(documents_cleaned)

    if (keywords_info == {}):
        return {}
    
    keywords_info = filter_unique_locations(keywords_info)
    keywords_info = normalize_data(keywords_info, ["location"])
    return keywords_info

def filter_unique_locations(data):
    sorted_items = sorted(data.items(), key=lambda x: (x[1]['location'], -x[1]['size_word']))

    filtered_data = {}
    last_location = -1

    for key, value in sorted_items:
        if value['location'] != last_location:
            filtered_data[key] = value
            last_location = value['location']

    return filtered_data

def normalize_data(data, columns):
    if isinstance(data, dict):
        return normalize_dict_of_dicts(data, columns)
    elif isinstance(data, list):
        return normalize_list_of_dicts(data, columns)
    else:
        return None
    
def normalize_dict_of_dicts(data, columns):
    records = list(data.values())
    
    min_max_values = {}
    for col in columns:
        col_values = [record[col] for record in records if col in record]
        if col_values:
            min_max_values[col] = {
                'min': min(col_values),
                'max': max(col_values)
            }
        else:
            min_max_values[col] = {'min': 0, 'max': 0}
    
    for record in records:
        for col in columns:
            min_val = min_max_values[col]['min']
            max_val = min_max_values[col]['max']
            if max_val - min_val != 0:
                if col in record:
                    record[col + "_normalized"] = (record[col] - min_val) / (max_val - min_val)
                else:
                    record[col + "_normalized"] = 0
            else:
                record[col + "_normalized"] = 0

    normalized_data = dict(zip(data.keys(), records))
    return normalized_data

def normalize_list_of_dicts(data, columns):
    max_values = {col: max(entry[col] for entry in data) for col in columns}
    min_values = {col: min(entry[col] for entry in data) for col in columns}

    normalized_data = []
    for entry in data:
        normalized_entry = entry.copy()
        for col in columns:
            array = entry[col]
            max_val = max_values[col]
            min_val = min_values[col]
            normalized_array = (array - min_val) / (max_val - min_val) if max_val != min_val else 0
            normalized_entry[col + '_normalized'] = normalized_array
        normalized_data.append(normalized_entry)

    return normalized_data

def normalize_rows(df, exclude_columns):
    # Cria uma cópia do DataFrame para não modificar o original.
    df_normalized = df.copy()

    # Itera sobre as linhas do DataFrame.
    for index, row in df.iterrows():
        # Seleciona os valores das colunas que não estão na lista de exclusão.
        values_to_normalize = row.drop(exclude_columns)
        
        # Calcula o mínimo e o máximo dos valores selecionados.
        min_val = values_to_normalize.min()
        max_val = values_to_normalize.max()
        
        # Verifica se o máximo é diferente do mínimo para evitar divisão por zero.
        if max_val > min_val:
            # Aplica a normalização Min-Max.
            df_normalized.loc[index, ~df_normalized.columns.isin(exclude_columns)] = (values_to_normalize - min_val) / (max_val - min_val)
        else:
            # Se o máximo e o mínimo são iguais, define os valores como 0 (ou poderia escolher outro valor padrão)
            df_normalized.loc[index, ~df_normalized.columns.isin(exclude_columns)] = 0
        
    return df_normalized

def extract_subject_from_html_text(html_text, tag_map=None):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = ""

    if (not tag_map):
        remove_tags = ['header', 'footer', 'fieldset', 'select', 'script', 'style', 'iframe', 'svg', 'img', 'link', 'button', 'noscript']
        for remove_tag in remove_tags:
            for tag_map in soup.find_all(remove_tag):
                tag_map.decompose()

        tags_com_hidden = soup.find_all(lambda element: element.get('class') and 'hidden' in ' '.join(element.get('class')))
        for tag_map in tags_com_hidden:
            tag_map.extract()
            
        def remove_empty_tags(tag_map):
            if not tag_map.text.strip():
                tag_map.extract()

        for tag_map in soup.find_all():
            remove_empty_tags(tag_map)

        tags_with_char_count = [(element, len(element.get_text(strip=True))) for element in soup.find_all()]
        sorted_tags = sorted(tags_with_char_count, key=lambda x: x[1], reverse=True)
        half_count = int(len(sorted_tags) // 3)

        for tag_map, _ in sorted_tags[half_count:]:
            tag_map.decompose()

        text = soup.get_text()
    else:
        tag_type = list(tag_map.keys())[1]
        if (tag_type in "path"):
            html = soup.select_one(tag_map['path'])
        else:
            html = soup.find(tag_map['tag'], id=tag_map[tag_type])
        
        if html is None:
            return None
        text = html.text

    return text

def append_new_df_and_save(path, new_df):
    if path_exists(path):
        existing_df = read_df(path, dtype={'ref': str})
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    combined_df.to_csv(path, index=False)
    
def get_product_description(html_text, tag_map):
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        
        html_content = soup.select_one(tag_map['path'])
        if not html_content:
            return None
        
        # Criar o conversor
        h = html2text.HTML2Text()
        
        # Configurações para remover formatação Markdown
        h.ignore_links = True   # Ignorar links
        h.ignore_images = True  # Ignorar imagens
        h.ignore_emphasis = True  # Ignorar negrito/itálico (sem asteriscos ou underlines)
        h.body_width = 0  # Não adicionar quebras de linha automáticas
        
        # Converter HTML para texto simples
        plain_text = h.handle(str(html_content))
        
        return plain_text
    except Exception:
        return None