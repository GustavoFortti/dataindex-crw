from copy import deepcopy

import pandas as pd

import src.lib.utils.data_quality as dq
from src.lib.load.connection.shopify import process_and_ingest_products
from src.lib.utils.dataframe import create_or_read_df, read_df
from src.lib.utils.log import message
from src.lib.utils.file_system import delete_file, path_exists

def load(conf, df_products_transform_csl):
    # Carregar os DataFrames e adicionar a coluna 'is_transform_data'
    columns = df_products_transform_csl.columns
    df_products_transform_csl['is_transform_data'] = 1
    
    df_last_load = create_or_read_df(conf['path_products_memory_shopify'])
    if df_last_load.empty:
        message("flag - carregando df_last_load inicial")
        df_last_load = create_or_read_df(conf['path_products_load_csl'], df_products_transform_csl.columns)
    
    if not df_last_load.empty:
        df_last_load['is_transform_data'] = 0

        # Concatenar DataFrames
        df_union = pd.concat([df_products_transform_csl, df_last_load], ignore_index=True)

        # Remover a coluna 'is_transform_data' e identificar duplicatas
        df_union_no_transform = df_union.drop(columns=['is_transform_data', 'ing_date'], errors='ignore')
        duplicates = df_union_no_transform[df_union_no_transform.duplicated(keep=False)].index
        
        # Remover duplicatas do DataFrame original
        df = df_union.drop(duplicates).query("is_transform_data == 1").reset_index(drop=True)
    else:
        df = deepcopy(df_products_transform_csl)
    
    df = df.drop(columns=['is_transform_data'])
    df = df[columns]
    df_products_transform_csl = df_products_transform_csl.drop(columns=['is_transform_data'])
    
    if (not df.empty):
        refs = df_products_transform_csl["ref"].values
        process_and_ingest_products(conf, df, refs, conf['brand'])
        df.to_csv(conf['path_products_shopify_csl'], index=False)
        message(f"path_products_shopify_csl - {path_exists(conf['path_products_shopify_csl'])}")
        
    df_products_transform_csl.to_csv(conf['path_products_load_csl'], index=False)
    delete_file(conf['path_products_memory_shopify'])
    message(f"path_products_load_csl - {path_exists(conf['path_products_load_csl'])}")
    message("LOAD END")