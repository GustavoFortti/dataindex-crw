import ast
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import numpy as np
import openai
import pandas as pd

from src.lib.utils.dataframe import read_and_stack_csvs_dataframes
from src.lib.utils.file_system import create_directory_if_not_exists, save_file
from src.lib.utils.general_functions import get_pages_with_status_true
from src.lib.utils.log import message
from src.lib.utils.text_functions import generate_hash
from src.lib.wordlist.wordlist import WORDLIST

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def set_config(args: Any, local: str) -> Dict[str, Any]:
    """
    Sets up the configuration dictionary based on the job arguments and local environment.

    Args:
        args (Any): Job arguments.
        local (str): Local environment path.

    Returns:
        Dict[str, Any]: Configuration dictionary for the job.
    """
    config = {
        "local": local,
        "job_name": args.job_name,
        "page_name": args.page_name,
        "page_type": args.page_type,
        "country": args.country,
        "src_data_path": f"{local}/data/{args.page_type}/{args.country}",
        "wordlist": WORDLIST[args.page_type],
        "data_path": f"{local}/data/{args.page_type}/{args.country}/{args.job_name}",
        "pages_path": f"{local}/src/jobs/slave_page/pages/{args.country}"
    }
    return config


def run(args: Any) -> None:
    """
    Executa o trabalho de extração e processamento de dados.

    Args:
        args (Any): Argumentos do trabalho.
    """
    message("STARTING THE JOB")

    global CONF
    local = os.getenv('LOCAL')
    CONF = set_config(args, local)
    wordlist = CONF["wordlist"]
    
    create_directory_if_not_exists(CONF["data_path"])

    pages = get_pages_with_status_true(CONF)
    df = read_and_stack_csvs_dataframes(CONF["src_data_path"], pages, "products_transform_csl.csv", {"ref": str})
    
    df["is_drink"] = np.where(df["unit_of_measure"] == "ml", "drink", None)
    df['title_terms'] = df['title_terms'].apply(ast.literal_eval)
    df['product'] = df['title_terms'].apply(lambda x: x.get('product'))
    df['features'] = df['title_terms'].apply(lambda x: x.get('features'))
    df['ingredients'] = df['title_terms'].apply(lambda x: x.get('ingredients'))
    df['flavor'] = df['title_terms'].apply(lambda x: x.get('flavor'))

    df = df[[
        'ref',
        'title',
        'page_name',
        'product',
        'features',
        'ingredients',
        'flavor',
        'is_drink',
    ]]
    
    df['class_product'] = None
    df = specific_rules_for_whey(df)
    
    columns = ["is_crunch", "is_drink"]
    for row in df.itertuples(index=False):
        ref = row.ref
        page_name = row.page_name

        values = [getattr(row, col) for col in columns if getattr(row, col) is not None]
        values_string = ' '.join(values)
        
        if (values_string):
            save_file(values_string, f"{CONF['src_data_path']}/{page_name}/products/{ref}_class.txt")
        
def specific_rules_for_whey(df):
    df['is_crunch'] = None
    
    # situalçoes especificas
    df['is_crunch'] = df.apply(
        lambda row: 'crunch' 
        if row['page_name'] == 'atlhetica_nutrition' and  ('ball' in row['title'] or 'blitz' in row['title']) 
        else None, 
        axis=1
    )
    
    return df