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
    remove_spaces,
    read_file,
    find_in_text_with_wordlist,
    flatten_list
)

from utils.wordlist import (
    BLACK_LIST, 
    PRONOUNS,
    find_subject_in_wordlist,
    remove_prepositions_pronouns
)

from shared.data_enrichment.enrichment_general_functions import (
    find_pattern_for_quantity,
    relation_qnt_price,
    convert_to_grams,
    image_processing,
)

from shared.data_enrichment.models_prep import (
    load_models_prep, 
    remove_suffix_to_columns
)

from shared.data_enrichment.models import run_models

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

def data_enrichment(conf, df):
    global CONF
    global WORDLIST
    global DATA_PATH

    CONF = conf
    WORDLIST = CONF['wordlist']
    DATA_PATH = CONF['data_path']

    df = df.drop_duplicates(subset='ref').reset_index(drop=True)
    message("dataframe origin")

    message("filtro de nulos")
    df_nulos = df[df[['title', 'price', 'image_url']].isna().any(axis=1)]
    df_nulos.to_csv(DATA_PATH + "/origin_del.csv", index=False)
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
    df[['quantity', 'unit']] = df['name'].apply(lambda text: find_pattern_for_quantity(text)).apply(pd.Series)

    df['quantity'] = df[['quantity', 'unit']].apply(convert_to_grams, axis=1)
    df['price_qnt'] = df.apply(relation_qnt_price, axis=1)
    df['quantity'] = df['quantity'].astype(str).replace("-1", np.nan)

    message("removendo produtos da blacklist")
    df = df[~df['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))]

    
    df = df[df['ref'].isin(["e266cf88", "46f6caa2", "ee122115", "8b5f971a"])]
    message("Criando colunas de definição para produtos")
    df = create_product_definition_columns(df, CONF)
    exit()
    
    df = df.dropna(subset=["ref", "title", "price", "image_url", "product_url"], how="any")

    print(df.info())

    image_processing(df, DATA_PATH)
    
    df = df[
        [
            'ref',
            'title',
            'price',
            'image_url',
            'product_url',
            'ing_date',
            'name',
            'brand',
            'price_numeric',
            'quantity',
            'price_qnt'
        ] + columns
    ]
    
    return df

def create_product_definition_columns(df, conf):
    message("criada colunas de definição do produto")
    df['product'] = None

    message("Load_models_prep")
    load_models_prep(df, conf)
    exit()

    data_path = conf['data_path']
    df_definition = pd.read_csv(f"{data_path}/model_y.csv")

    message("Add definição")
    refs_prediction = []
    for idx, row in df.iterrows():
        ref = row['ref']

        df_definition_temp = df_definition[df_definition["ref"] == ref].drop(columns=["ref"]).reset_index(drop=True)
        is_defined = (df_definition_temp.values != 0).any()

        keyswords = ""
        if (is_defined):
            message(f"{ref} - definition")
            keyswords = get_keywords(df_definition_temp, False)
            df.loc[df["ref"] == ref, "product" ] = keyswords
        else:
            message(f"{ref} - prediction")
            refs_prediction.append(ref)

    df_prediction = pd.read_csv(f"{data_path}/model_x.csv")
    df_prediction_temp = df_prediction[df_prediction["ref"].isin(refs_prediction)]
    print(df_prediction_temp)
    keyswords = get_keywords(df_prediction_temp, True)

def get_keywords(df, using_model):
    if (using_model):
        df = run_models(df, CONF['models_path'])
        # print(df)
    return

    definition_terms = remove_suffix_to_columns(df, ['ref'])
    columns = list(df.columns[df.iloc[0] != 0])

    keyswords = [find_subject_in_wordlist(term, WORDLIST) for term in definition_terms]
    keyswords = ", ".join(flatten_list(keyswords))

    return keyswords