import pandas as pd

from src.lib.transform.transform_functions import (
    apply_generic_filters, create_price_discount_percent_col,
    create_product_def_cols, create_quantity_column, filter_nulls,
    image_processing, remove_blacklisted_products)
from src.lib.utils.log import message


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
    
    message("Criando colunas de definição para produtos")
    df = create_product_def_cols(df, conf)
    
    message("Criando colunas coleção de produtos")
    df = create_product_collection_col(df)
    
    # message("Processamento de novas imagens dos produtos")
    # image_processing(df, conf['data_path'])

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
            'price_numeric',
            'price_discount_percent',
            'compare_at_price',
            'quantity',
            'price_qnt',
            'product_def',
            'product_def_tag',
            'product_def_pred',
            'product_def_pred_tag',
            'collection'
        ]
    ]

    print(df.info())

    return df

def create_product_collection_col(df):
    import numpy as np
    
    def assign_collection(row):
        if (row['price_discount_percent'] > 0):
            return 'Promoção'
        elif ('whey' in str(row['product_def']).lower() or 'whey' in str(row['product_def_pred']).lower()):
            return 'Whey Protein'
        elif ('barrinha' in str(row['product_def']).lower() or 'barrinha' in str(row['product_def_pred']).lower()):
            return 'Barrinhas'
        elif ('creatina' in str(row['product_def']).lower() or 'creatina' in str(row['product_def_pred']).lower()):
            return 'Creatina'
        elif ('pretreino' in str(row['product_def']).lower() or 'pretreino' in str(row['product_def_pred']).lower()):
            return 'Pré-treino'
        else:
            return 'Outros'

    df['collection'] = df.apply(assign_collection, axis=1)
    return df