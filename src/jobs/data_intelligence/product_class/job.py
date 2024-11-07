import ast
import os
from typing import Any, Dict

import numpy as np
import pandas as pd

from src.lib.utils.dataframe import read_and_stack_csvs_dataframes
from src.lib.utils.file_system import create_directory_if_not_exists, save_file
from src.lib.utils.general_functions import get_pages_with_status_true
from src.lib.utils.log import message
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

def safe_literal_eval(val):
    try:
        # Verifica se o valor é NaN
        if pd.isna(val):
            return None  # Ou qualquer outro valor que faça sentido
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return None  # Ou qualquer outra forma de tratamento de erro

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
    df['title_terms'] = df['title_terms'].apply(safe_literal_eval)
    df['product'] = df['title_terms'].apply(lambda x: x.get('product') if x else None)
    df['features'] = df['title_terms'].apply(lambda x: x.get('features') if x else None)
    df['ingredients'] = df['title_terms'].apply(lambda x: x.get('ingredients') if x else None)
    df['flavor'] = df['title_terms'].apply(lambda x: x.get('flavor') if x else None)
    df["is_small_10_to_50"] = np.where((df["quantity"] > 10) & (df["quantity"] < 50), True, None)
    df['whey_sache'] = df.apply(lambda x: 'sache' if 'whey' in str(x['product']) and x["is_small_10_to_50"] else None, axis=1)

    df = df[[
        'ref',
        'title',
        'page_name',
        'product',
        'features',
        'ingredients',
        'flavor',
        'is_drink',
        'whey_sache',
    ]]
    
    df['class_product'] = None
    df = specific_rules(df)
    
    columns = ["is_crunch", "is_drink", "whey_sache", "is_what"]
    for row in df.itertuples(index=False):
        ref = row.ref
        page_name = row.page_name

        values = [getattr(row, col) for col in columns if getattr(row, col) is not None]
        values_string = ' '.join(values)
        
        if (values_string):
            save_file(values_string, f"{CONF['src_data_path']}/{page_name}/products/{ref}_class.txt")
        
def specific_rules(df):
    df['is_crunch'] = None
    
    # situalçoes especificas
    df['is_crunch'] = df.apply(
        lambda row: 'crunch' 
        if row['page_name'] == 'atlhetica_nutrition' and  ('ball' in row['title'] or 'blitz' in row['title']) 
        else None, 
        axis=1
    )
    
    df['is_what'] = None
    
    # Isofort Ultra Imuno - 900g baunilha - Vitafor
    df.loc[df["ref"] == "ef7970b3", 'is_what'] = "whey protein, isolado, hidrolisado"
    
    # N.O Xplosion Frutas Vermelhas 240G
    df.loc[df["ref"] == "9da89a4f", 'is_what'] = "pre-treino"
    
    # WHEY PROTEIN ISOLADO
    df.loc[df["ref"] == "292a3fcd", 'is_what'] = "whey protein, sache"
    df.loc[df["ref"] == "b265d7c0", 'is_what'] = "whey protein, sache"
    
    # Super Gainers Refil 3Kg
    df.loc[df["ref"] == "2a090f2d", 'is_what'] = "hipercalorico"
    
    return df