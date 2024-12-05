import importlib
from copy import deepcopy
from typing import Optional

from src.jobs.pipeline import JobBase
from src.lib.utils.dataframe import (create_or_read_df,
                                     read_and_stack_csvs_dataframes)
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       list_directory)
from src.lib.utils.log import message
from src.lib.utils.page_functions import get_pages_with_status_true
from src.pages.page import Page
from src.lib.load.shopify.shopify import process_and_ingest_products


def run(job_base: JobBase) -> Optional[None]:
    """
    Executes the data load pipeline for a given job.

    Args:
        job_base (JobBase): An instance of JobBase containing job-specific configurations.

    Returns:
        Optional[None]: Exits the program after transformations and saves the result.
    """
    # Load the appropriate page module dynamically
    message("Load process started.")
    
    pages = list_directory(job_base.pages_path)
    pages = [page for page in pages if ("." not in page) and ("__" not in page)]
    
    for page in pages:
        page_module = importlib.import_module(f"src.pages.{page}.page")
        page = Page(**page_module.page_arguments)
        job_base.append_pages(page)
        
    create_directory_if_not_exists(job_base.load_data_path)
    
    message("read data")
    pages_with_status_true = get_pages_with_status_true(job_base)
    df_products_transform_csl = read_and_stack_csvs_dataframes(job_base.src_data_path, pages_with_status_true, "transform_csl.csv", dtype={'ref': str})
    df_products_transform_csl = df_products_transform_csl.drop_duplicates(subset='ref').reset_index(drop=True)
    df_products_transform_csl = df_products_transform_csl.sample(frac=1).reset_index(drop=True)
    
    # load(conf, df_products_transform_csl)
    # Carregar os DataFrames e adicionar a coluna 'is_transform_data'
    columns = df_products_transform_csl.columns
    df_products_transform_csl['is_transform_data'] = 1
    
    
    df_last_load = create_or_read_df(job_base.path_memory_shopify)
    if df_last_load.empty:
        message("flag - carregando df_last_load inicial")
        df_last_load = create_or_read_df(job_base.path_load_csl, df_products_transform_csl.columns)
    
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

    brands = [page.brand for page in job_base.pages]
    
    
    if (not df.empty):
        refs = df_products_transform_csl["ref"].values
        process_and_ingest_products(job_base, df, refs, brands)
        print(brands)
        exit()
        df.to_csv(conf['path_products_shopify_csl'], index=False)
        message(f"path_products_shopify_csl - {path_exists(conf['path_products_shopify_csl'])}")
    
    df_products_transform_csl.to_csv(conf['path_products_load_csl'], index=False)
    delete_file(conf['path_products_memory_shopify'])
    message(f"path_products_load_csl - {path_exists(conf['path_products_load_csl'])}")
    message("LOAD END")