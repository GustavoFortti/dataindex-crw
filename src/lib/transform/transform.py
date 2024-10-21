import pandas as pd

from src.lib.transform.product_info import create_product_info_cols
from src.lib.transform.transform_functions import (
    apply_generic_filters, create_history_price_col,
    create_price_discount_percent_col,
    create_quantity_column, filter_nulls, remove_blacklisted_products)
from src.lib.utils.log import message


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

def transform(conf, df):
    message("START TRANSFORM")

    message("Filtro de nulos")
    df = filter_nulls(df)

    message("Aplicando filtros de nome|preço|marca")
    df = apply_generic_filters(df, conf)

    message("Criando coluna quantidade")
    df = create_quantity_column(df)

    message("Removendo produtos da blacklist")
    df = remove_blacklisted_products(df)

    message("Criando coluna de desconto")
    df = create_price_discount_percent_col(df, conf['data_path'])
    
    message("Criando coluna de desconto")
    df = create_history_price_col(df, conf)
    
    message("CRIAÇÃO das colunas [product_definition, collections]")
    df = create_product_info_cols(df, conf)
    
    df = df.dropna(subset=["ref", "title", "price", "image_url", "product_url"], how="any")
    
    df = df[
        [
            'ref',
            'title',
            'title_extract',
            'name',
            'price',
            'image_url',
            'product_url',
            'ing_date',
            'brand',
            'page_name',
            'price_numeric',
            'price_discount_percent',
            'compare_at_price',
            'quantity',
            'unit_of_measure',
            'price_qnt',
            'product_tags',
            'collections',
            'prices',
            'title_terms',
        ]
    ]

    print(df.info())

    return df