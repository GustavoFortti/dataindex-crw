import os
import time
from datetime import datetime
from typing import Any, Dict, Optional

import openai
import pandas as pd

from src.lib.utils.dataframe import (create_or_read_df,
                                     read_and_stack_csvs_dataframes)
from src.lib.utils.file_system import (create_file_if_not_exists,
                                       file_exists_with_modification_time,
                                       read_file, read_json,
                                       save_file_with_line_breaks, save_json)
from src.lib.utils.general_functions import get_pages_with_status_true
from src.lib.utils.log import message
from src.lib.utils.text_functions import generate_hash
from src.lib.wordlist.wordlist import WORDLIST


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

    # Caminho do arquivo de controle
    path_file_control = os.path.join(CONF["data_path"], "control.json")
    create_file_if_not_exists(path_file_control, "{}")
    control_data = read_json(path_file_control)

    # Data atual no formato YYYY-MM-DD
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Inicializa a entrada para a data atual se não existir
    if today_str not in control_data:
        control_data[today_str] = {
            "limit": 100,
            "requests": 0,
            "tokens_in": 0,
            "tokens_out": 0
        }
        
    if control_data[today_str]["requests"] >= control_data[today_str]["limit"]:
        message(f"Daily limit of {control_data[today_str]['limit']} descriptions reached for {today_str}.")
        return

    # Carrega as páginas com status 'True'
    pages_with_status_true = get_pages_with_status_true(CONF)

    # Carrega o DataFrame com os dados dos produtos
    df = read_and_stack_csvs_dataframes(
        CONF["src_data_path"],
        pages_with_status_true,
        "products_transform_csl.csv",
        dtype={'ref': str}
    )
    
    df = df[['ref', 'brand']]
    df_product_info = create_or_read_df(
        path=f"{CONF["data_path"]}/product_info.csv", 
        columns=[
            "ref",
            "brand",
            "hash",
            "has_origin",
            "origin_is_updated"
            "description_exists",
            "latest_description_update",
        ], 
        dtype={'ref': str}
    )
    
    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        brand: str = str(row['brand'])
        
        path_products = f"{CONF['src_data_path']}/{brand}/products"
        path_product_description = f"{path_products}/{ref}_description.txt"
        
        product_description = read_file(path_product_description)
        hash = None
        if product_description:
            hash = generate_hash(product_description)
            df.at[idx, "hash"] = hash
            df.at[idx, "has_origin"] = True
        else:
            df.at[idx, "hash"] = None
            df.at[idx, "has_origin"] = False
        
        if not df_product_info[df_product_info["ref"] == ref].empty:
            old_hash = df_product_info[df_product_info["ref"] == ref]["hash"].values[0]
        else:
            old_hash = None

        if old_hash and hash:
            if old_hash == hash:
                df.at[idx, "origin_is_updated"] = 1
            else:
                df.at[idx, "origin_is_updated"] = 0
        else:
            df.at[idx, "origin_is_updated"] = 0
        
        file_status = file_exists_with_modification_time(path_products, f"{ref}_description_ai.txt")
        df.at[idx, "description_exists"] = 1 if file_status[0] else 0
        df.at[idx, "latest_description_update"] = file_status[1]
    
    df = df.sort_values(["description_exists", "origin_is_updated", "latest_description_update", "has_origin"])
    df.to_csv(f"{CONF["data_path"]}/product_info.csv", index=False)

    df = df[df['has_origin'] == True]
    df = df.loc[(df['origin_is_updated'] == 0) | (df['description_exists'] == 0)]
    
    # Iterate over DataFrame rows
    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        brand: str = str(row['brand'])

        # Check if 'ref' matches the expected value and continue if it doesn't
        
        # Construct the product description file path
        path_products = f"{CONF['src_data_path']}/{brand}/products"
        path_product_description = f"{path_products}/{ref}_description.txt"
        product_description = read_file(path_product_description)
        
        if (not product_description):
            continue
        
        message(f"REQUEST - {control_data[today_str]["requests"]}")
        message(f"ref - {ref}")
        message(f"brand - {brand}")
        path_product_description_ai = f"{path_products}/{ref}_description_ai.txt"
        product_description_ai = refine_description(product_description)
        
        if (product_description_ai):
            message(f"{ref} - product_description_ai - OK")
            save_file_with_line_breaks(path_product_description_ai, product_description_ai)
        
            save_json(path_file_control, control_data)
            
        control_data[today_str]["requests"] += 1
        time.sleep(2)
        
        if control_data[today_str]["requests"] >= control_data[today_str]["limit"]:
            message(f"Daily limit of {control_data[today_str]['limit']} descriptions reached for {today_str}.")
            return
    
def refine_description(description: str) -> Optional[str]:
    """
    Uses the OpenAI API to generate a refined version of the product description.

    Args:
        description (str): The product description to be refined.

    Returns:
        Optional[str]: Refined text or None in case of an error.
    """
    try:
        # Set up the OpenAI client
        client = openai.OpenAI()

        # Set the assistant ID
        assistant_id = "asst_Gg9EqaQUrMv0o2tUap14sgEX"

        # Create a new thread
        thread = client.beta.threads.create()

        # Add a message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=description
        )

        # Execute the assistant to generate a response
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Periodically check the run status
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                raise Exception("The execution failed.")

        # List all the messages in the thread
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        # Get the last message from the assistant
        for message in messages.data:
            if message.role == "assistant" and hasattr(message.content[0], 'text'):
                return message.content[0].text.value

        return None

    except Exception as e:
        print(f"Error calling the OpenAI API: {e}")
        return None