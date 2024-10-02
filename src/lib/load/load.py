from copy import deepcopy

import pandas as pd

import src.lib.utils.data_quality as dq
from src.lib.load.connection.shopify import process_and_ingest_products
from src.lib.utils.dataframe import create_or_read_df
from src.lib.utils.log import message


def load(conf):
    # Carregar os DataFrames e adicionar a coluna 'transform'
    df_products_transform_csl = pd.read_csv(conf['data_path'] + '/products_transform_csl.csv')
    df_products_transform_csl['is_transform_data'] = 1
    
    products_load_csl_path = conf['data_path'] + '/products_load_csl.csv'
    
    df_products_load_csl = create_or_read_df(products_load_csl_path, df_products_transform_csl.columns)
    if (not df_products_load_csl.empty):
        df_products_load_csl['is_transform_data'] = 0

        # Unir os DataFrames
        df_union = pd.concat([df_products_transform_csl, df_products_load_csl])

        # Remover a coluna 'is_transform_data' apenas para identificar duplicatas
        df_union_no_transform = df_union.drop(columns=['is_transform_data'])

        # Identificar as duplicatas sem considerar a coluna 'is_transform_data'
        duplicates = df_union_no_transform[df_union_no_transform.duplicated(keep=False)]

        # Remover duplicatas e suas originais do DataFrame original (com 'is_transform_data')
        df = df_union.drop(duplicates.index)
        df = df.drop(columns=['is_transform_data'])
        df = df[df['is_transform_data'] == 1]
    else:
        df = deepcopy(df_products_transform_csl)
        df = df.drop(columns=['is_transform_data'])

    df_products_transform_csl = df_products_transform_csl.drop(columns=['is_transform_data'])
    
    if (conf['exec_flag'] == "data_quality"):
        message("Running Data Quality...")
        dq.data_history_analysis(conf, df)
        exit(0)
    
    dq.save_history_data(conf, df_products_transform_csl)
    message("Data ready for ingestion")
    
    if (not df.empty):
        process_and_ingest_products(df)
        df.to_csv(conf['data_path'] + "/products_shopify_csl.csv", index=False)
        
    df_products_transform_csl.to_csv(conf['data_path'] + "/products_load_csl.csv", index=False)