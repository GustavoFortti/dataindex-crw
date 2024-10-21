import os
import time
from datetime import datetime
from typing import Any, Dict, Optional

import openai
import pandas as pd

from src.lib.utils.dataframe import (create_or_read_df,
                                     read_and_stack_csvs_dataframes)
from src.lib.utils.file_system import (create_directory_if_not_exists, create_file_if_not_exists,
    DATE_FORMAT, file_exists_with_modification_time, read_file, read_json,
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
    
    create_directory_if_not_exists(CONF["data_path"])

    # Caminho do arquivo de controle
    path_file_control = os.path.join(CONF["data_path"], "control.json")
    print(path_file_control)
    create_file_if_not_exists(path_file_control, "{}")
    control_data = read_json(path_file_control)

    # Data atual no formato YYYY-MM-DD
    today_str = datetime.now().strftime(DATE_FORMAT)

    # Inicializa a entrada para a data atual se não existir
    if today_str not in control_data:
        control_data[today_str] = {
            "limit": 200,
            "requests": 0,
            "tokens_in": 0,
            "tokens_out": 0
        }
    
    message(f"requests: {control_data[today_str]["requests"]}")
    message(f"limit: {control_data[today_str]["limit"]}")
    
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
    
    df = df[df["page_name"] == "growth_supplements"]
    df = df[['ref', 'brand', 'page_name']]
    
    
    # Iterate over DataFrame rows
    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        page_name: str = str(row['page_name'])
        
        # Check if 'ref' matches the expected value and continue if it doesn't
        
        # Construct the product description file path
        path_products = f"{CONF['src_data_path']}/{page_name}/products"
        path_product_description = f"{path_products}/{ref}_description_ai.txt"
        product_description = read_file(path_product_description)
        
        if (not product_description):
            continue
        
        message(f"REQUEST - {control_data[today_str]["requests"]}")
        message(f"ref - {ref}")
        message(f"path - {path_product_description}")

        path_product_description_ai = f"{path_products}/{ref}_description_ai.txt"
        product_description_ai = refine_description(product_description, "asst_MCh0pbhWcLYlZojeqJf26gjO")
        
        if (product_description_ai):
            message(f"{ref} - product_description_ai - OK")
            save_file_with_line_breaks(path_product_description_ai, product_description_ai)
            save_json(path_file_control, control_data)
            
        control_data[today_str]["requests"] += 1
        time.sleep(2)
        
        if control_data[today_str]["requests"] >= control_data[today_str]["limit"]:
            save_json(path_file_control, control_data)
            message(f"Daily limit of {control_data[today_str]['limit']} descriptions reached for {today_str}.")
            return
    
def refine_description(description: str, assistant_id: str) -> Optional[str]:
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