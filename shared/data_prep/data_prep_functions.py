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
    find_in_text_with_wordlist,
)

from utils.wordlist import (
    BLACK_LIST, 
)

from shared.data_enrichment.enrichment_general_functions import (
    find_pattern_for_quantity,
    relation_qnt_price,
    convert_to_grams,
)

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
