import ast
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

from utils.log import message

from utils.general_functions import (
    clean_text,
    read_file,
    path_exist,
    delete_file,
    save_json,
    flatten_list,
    read_json,
    generate_numeric_hash,
)

from utils.wordlist import (
    get_word_index_in_text,
    find_subject_in_wordlist,
    get_back_words
)

def load_models_prep(df, conf):
    message("Running model prep...")
    global CONF
    global WORDLIST
    global DATA_PATH

    CONF = conf
    WORDLIST = conf["wordlist"]
    DATA_PATH = CONF["data_path"]

    keywords_json_file = f"{DATA_PATH}/keywords.json"
    
    # keywords_data = extract_keywords_from_products(df)
    # save_json(keywords_json_file, keywords_data)
    # exit()
    
    # usado para desenvolvimento
    if (not path_exist(keywords_json_file)):
        keywords_data = extract_keywords_from_products(df)
        save_json(keywords_json_file, keywords_data)
    else:
        keywords_data = read_json(keywords_json_file)

    exponent = 8 # calc_best_exponent(df, keywords_data)

    global FILE_PATH_PRODUCT_X
    global FILE_PATH_PRODUCT_Y
    global FILE_PATH_PREP_SCORES

    FILE_PATH_PRODUCT_X = f"{DATA_PATH}/product_models_x.csv"
    FILE_PATH_PRODUCT_Y = f"{DATA_PATH}/product_models_y.csv"
    FILE_PATH_PREP_SCORES = f"{DATA_PATH}/score_models.csv"

    # delete old data for new load
    delete_file(FILE_PATH_PRODUCT_X)
    delete_file(FILE_PATH_PRODUCT_Y)
    delete_file(FILE_PATH_PREP_SCORES)

    for idx, row in df.iterrows():
        ref = row['ref']
        message(f"Preparando {ref}")

        load_prep_scores(ref, keywords_data)

        # keywords_exponent = lambda index: exponent if ((index > 0) & (index < (len(keywords_data[ref]) - 1))) else 1
        # keywords_score = [calc_keywords_score(keywords, keywords_exponent(index))
        #                   if keywords != {} else None for index, keywords in enumerate(keywords_data[ref])]
        
        # export_keywords_score(ref, keywords_score)

def load_prep_scores(ref, keywords_data):
    title_keywords = keywords_data[ref][0]
    subjects = {keyword['subject'] for keyword in title_keywords.values()}
    excluded_title_keywords = keywords_data[ref][1:]

    if title_keywords:
        for contained in (True, False):
            dfs_temp = [create_scores_dataframe(keywords, subjects, ref, contained) for keywords in excluded_title_keywords]
            df_prep_scores = pd.concat(dfs_temp, ignore_index=True)
            df_prep_scores['target'] = int(contained)
            append_new_df_and_save(FILE_PATH_PREP_SCORES, df_prep_scores)
    else:
        df_prep_scores = pd.concat([create_scores_dataframe(keywords, subjects, ref, False) for keywords in excluded_title_keywords], ignore_index=True)
        df_prep_scores['target'] = -1
        append_new_df_and_save(FILE_PATH_PREP_SCORES, df_prep_scores)

def create_scores_dataframe(keywords, subjects, ref, contained):
    prep_scores = [
        {
            "ref": ref, 
            "back_word": keyword['back_words'], 
            "subject": keyword['subject'],
            "location": int(keyword['location']), 
            "word_number": int(keyword['word_number']),
            "sum_locations": int(keyword['sum_locations']),
            "qnt_locations": int(keyword['qnt_locations']),
            "document_size": int(keyword['document_size'])
        } 
        for keyword in keywords.values() 
        if (keyword['subject'] in subjects) == contained 
    ]

    df = pd.DataFrame(prep_scores)

    if df.empty:
        return pd.DataFrame(columns=df.columns)
    
    df['document_num_words'] = int(df.shape[0])
    df['sum_locations_document'] = int(sum(list(df['location'].values)))
    df['num_of_possible_titles'] = df['subject'].nunique()

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

def export_keywords_score(ref, keywords_score):
    keys = list(WORDLIST.keys())

    qnt_documents = len(keywords_score)
    df = pd.DataFrame(0.0, index=range(qnt_documents), columns=keys)
 
    df['ref'] = ref
    df['index'] = df.index
    df['brand'] = generate_numeric_hash(CONF['brand'])

    title_subject = []    
    first_doc = True
    for index, keywords_document in enumerate(keywords_score):
        if (not keywords_document):
            continue

        for subject in keywords_document:
            word = keys[subject["index"]]
            if (first_doc):
                title_subject.append(word)
                subject["score_normalized"] = 1

            df.loc[((df['ref'] == ref) & (df.index == index)), word] = subject["score_normalized"]
            
        first_doc = False

    df_title = df[df['index'] == 0]
    df_tags = df[((df['index'] != 0) & (df['index'] != (qnt_documents - 1)))]
    df_all = df[df['index'] == (qnt_documents - 1)]

    cols_to_order = ["ref", "brand", "index"]
    order_cols = lambda df_temp: df_temp[cols_to_order + [col for col in df.columns if col not in cols_to_order]]
    df_title = order_cols(df_title)
    df_tags = order_cols(df_tags)
    df_all = order_cols(df_all)

    df_title = df_title.drop(columns=["index"])
    excluded_cols = ["ref", "brand"]
    df_title = add_suffix_to_columns(df_title, excluded_cols, "target")

    df_tags = df_tags.groupby(["ref", "brand"]).sum().reset_index()
    df_tags = df_tags.drop(columns=["brand"])
    excluded_cols = ["ref"]
    df_tags = add_suffix_to_columns(df_tags, excluded_cols, "tags")
    df_tags = normalize_rows(df_tags, ["ref", "index_tags"])

    df_all = df_all.reset_index(level=0, drop=True)
    df_all = df_all.drop(columns=["brand"])
    excluded_cols = ["ref"]
    df_all = add_suffix_to_columns(df_all, excluded_cols, "all")
    
    df_temp = pd.merge(df_title, df_tags, on="ref")
    df = pd.merge(df_temp, df_all, on="ref")

    save_model_df(df)

def add_suffix_to_columns(df, excluded_cols, suffix="target"):
    return df.rename(columns=lambda col: col + "_" + suffix if col not in excluded_cols else col)

def remove_suffix_to_columns(df, excluded_cols, suffix="target"):
    return df.rename(columns=lambda col: col.replace("_" + suffix, "") if col not in excluded_cols else col)

def save_model_df(df):
    cols_without_target = [col for col in df.columns if 'target' not in col]
    df_x = df[cols_without_target]
    cols_with_target = [col for col in df.columns if 'target' in col]
    df_y = df[['ref'] + cols_with_target]

    df_y = convert_float_to_int(df_y, ['ref'])

    append_new_df_and_save(FILE_PATH_PRODUCT_X, df_x)
    append_new_df_and_save(FILE_PATH_PRODUCT_Y, df_y)

def convert_float_to_int(df, exclude_cols):
    df_copy = df.copy()
    for col in df.columns:
        if col not in exclude_cols:
            df_copy[col] = df_copy[col].round().astype(int)
    return df_copy

def calc_best_exponent(df, keywords_data):
    bests_score_exponents = []
    for idx, row in df.iterrows():
        ref = row['ref']
        title = row['title']

        keywords_documents = keywords_data[ref]
        title = keywords_documents[0]

        if (title == {}):
            continue
        message(f"{ref} - {title} - calc exponent")

        target_score = calc_keywords_score(title, 1)

        target_keywords = [list(WORDLIST.keys())[target_item["index"]] for target_item in target_score]
        bests_score_exponent = [calc_keywords_exponent_score(keywords_document, target_keywords) for keywords_document in keywords_documents]
        bests_score_exponents.append(bests_score_exponent)

    num_exponents = len(bests_score_exponents[0])

    exponent_sums = [sum(sublist[i] for sublist in bests_score_exponents) for i in range(num_exponents)]

    average_per_exponent = [round(exponent_sum / len(bests_score_exponents), 2) for exponent_sum in exponent_sums]

    message(f"best_exponent = {average_per_exponent}")
    return average_per_exponent

def calc_keywords_exponent_score(keywords, target_keywords):
    index_best_score = 0
    best_score = None
    for i in range(-10, 11):
        keywords_scores = calc_keywords_score(keywords, i)

        worst_scores = keywords_scores[-1:][0]['score'] # pega o ultimo score que menor valor
        scores = [keyword_score['score'] for keyword_score in keywords_scores if any(target_keyword in keyword_score['subject'] 
                                                                                         for target_keyword in target_keywords)]
        
        if (scores == []):
            return 0

        score_aux = [score / worst_scores for score in scores]
        scores_avg = sum(score_aux) / len(score_aux)
        if ((not best_score) or (best_score > scores_avg)):
            best_score = scores_avg
            index_best_score = i

    return index_best_score

def calc_keywords_score(keywords, exponent):
    keywords_calc = []
    for word in (keywords.values()):
        if (exponent != 1):
            score = ((abs(1 - (word['location_normalized']))) + 1) ** exponent
        else:
            score = ((abs(1 - (word['location_normalized']) * (word['qnt_locations']))) + 1)
        
        keywords_calc.append({
                        "subject": word['subject'], 
                        "score": score,
                        "location": word['location'],
                        "location_normalized": word['location_normalized'],
                        "qnt_locations": word['qnt_locations'],
                        "size_word": word['size_word'],
                    }) 
        
    keywords_calc = sorted(keywords_calc, key=lambda x: x['score'], reverse=True)

    keywords_agg = {}
    for item in keywords_calc:
        subject = item['subject']
        score = item['score']
        if subject in keywords_agg:
            keywords_agg[subject] += score
        else:
            keywords_agg[subject] = score

    keywords_agg = [{
        'subject': find_subject_in_wordlist(key, WORDLIST),
        'score': value
    } for key, value in keywords_agg.items()]
    
    keywords_data = sorted(keywords_agg, key=lambda x: x['score'], reverse=True)
    keywords_data = normalize_data(keywords_data, ["score"])

    for keyword_data in keywords_data:
        keyword_data["index"] = next((index for index, key in enumerate(WORDLIST.keys()) if key in keyword_data['subject']), None)

    return keywords_data

def extract_keywords_from_products(df):
    keywords_data = {}
    for idx, row in df.iterrows():
        ref = row['ref']
        title = row['title']
        
        message(f"extraindo dados de {ref} - {title}")

        page_path = f"{DATA_PATH}/products/{ref}.txt"

        html_text = read_file(page_path)

        product_documents = []

        product_documents.append(title)

        product_documents.extend([extract_subject_from_html_text(html_text, tag) for tag in  CONF["product_definition_tag"]])

        text_from_html = extract_subject_from_html_text(html_text)
        product_documents.append(text_from_html)

        keywords_info = [get_keywords_info(document) for document in product_documents]
        keywords_data[ref] = keywords_info
    
    return keywords_data

def get_keywords_info(document):
    documents_accents = clean_text(document, False, False, False, False, True)
    documents_cleaned = clean_text(document, False, False, False, True, True)

    keywords_info = {}
    for key, value in WORDLIST.items():
        subject = value['subject']

        for word in subject:
            locations = get_word_index_in_text(word, documents_cleaned)
            if (locations != []):
                back_words = get_back_words(documents_cleaned, documents_accents, locations, len(word))

                for location, sub_prep_scores in zip(locations, back_words):

                    keywords_info[f"{word}_{location}"] = {}
                    keywords_info[f"{word}_{location}"]["location"] = location
                    keywords_info[f"{word}_{location}"]["word_number"] = len(documents_cleaned[:location].split())
                    keywords_info[f"{word}_{location}"]["size_word"] = len(word)
                    keywords_info[f"{word}_{location}"]["qnt_locations"] = len(locations)
                    keywords_info[f"{word}_{location}"]["sum_locations"] = sum(locations)
                    keywords_info[f"{word}_{location}"]["subject"] = key
                    keywords_info[f"{word}_{location}"]["back_words"] = sub_prep_scores[-5:]
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
            score = entry[col]
            max_val = max_values[col]
            min_val = min_values[col]
            normalized_score = (score - min_val) / (max_val - min_val) if max_val != min_val else 0
            normalized_entry[col + '_normalized'] = normalized_score
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

def extract_subject_from_html_text(html_text, tag=None):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = ""

    if (not tag):
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

        text = soup.get_text()
    else:
        html = soup.find(tag['tag'], class_=tag['class'])
        if (html != None):
            text = html.text

    return text

def append_new_df_and_save(path, new_df):
    if path_exist(path):
        existing_df = pd.read_csv(path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    combined_df.to_csv(path, index=False)