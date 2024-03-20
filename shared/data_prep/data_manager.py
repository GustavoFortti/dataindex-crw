import pandas as pd

from utils.log import message

from shared.data_prep.data_prep_functions import (
    filter_nulls,
    apply_generic_filters,
    create_quantity_column,
    remove_blacklisted_products,
    create_product_def_cols,
    image_processing
)

def data_prep(conf, df):
    global CONF
    global WORDLIST
    global DATA_PATH

    CONF = conf
    WORDLIST = CONF['wordlist']
    DATA_PATH = CONF['data_path']

    message("Filtro de nulos")
    df = filter_nulls(df, DATA_PATH)

    message("Aplicando filtros de nome|preço|marca")
    df = apply_generic_filters(df, CONF)

    message("Criando coluna quantidade")
    df = create_quantity_column(df)

    message("Removendo produtos da blacklist")
    df = remove_blacklisted_products(df)

    message("Criando colunas de definição para produtos")
    df = create_product_def_cols(df, CONF)

    df = df.dropna(subset=["ref", "title", "price", "image_url", "product_url"], how="any")

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
            'price_qnt',
            'product_def',
            'product_def_pred'
        ]
    ]

    print(df.info())

    return df