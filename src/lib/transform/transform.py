import pandas as pd

from src.lib.transform.transform_functions import (
    apply_generic_filters, create_price_discount_percent_col,
    create_product_collection_col, create_product_definition_col,
    create_quantity_column, filter_nulls, remove_blacklisted_products)
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
    df = create_product_definition_col(df, conf)
    
    message("Criando colunas coleção de produtos")
    df = create_product_collection_col(df, conf)
    print(df.head())
    exit()
    
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
            'price_qnt',
            'product_definition',
            'collections',
        ]
    ]

    print(df.info())

    return df