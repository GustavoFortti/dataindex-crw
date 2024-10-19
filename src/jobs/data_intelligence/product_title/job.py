import os
import time
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

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
            "limit": 1373,
            "requests": 0,
            "tokens_in": 0,
            "tokens_out": 0
        }
    
    message(f"requests: {control_data[today_str]["requests"]}")
    message(f"limit: {control_data[today_str]["limit"]}")
    
    if control_data[today_str]["requests"] >= control_data[today_str]["limit"]:
        message(f"Daily limit of {control_data[today_str]['limit']} description_ais reached for {today_str}.")
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
    
    df = df[['ref', 'title', 'brand', 'page_name']]
    df_product_info = create_or_read_df(
        path=f"{CONF["data_path"]}/product_info.csv", 
        columns=[
            "ref",
            "brand",
            "page_name",
            "hash",
            "has_origin",
            "origin_is_updated"
            "description_ai_exists",
            "latest_description_ai_update",
        ], 
        dtype={'ref': str}
    )
    
    df["hash"] = None
    df["has_origin"] = False
    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        page_name: str = str(row['page_name'])
        
        path_products = f"{CONF['src_data_path']}/{page_name}/products"
        path_product_description_ai = f"{path_products}/{ref}_description_ai.txt"
        product_description_ai = read_file(path_product_description_ai)
        
        hash = None
        if product_description_ai:
            hash = generate_hash(product_description_ai)
            df.at[idx, "hash"] = hash
            df.at[idx, "has_origin"] = True
        
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
        
        file_status = file_exists_with_modification_time(path_products, f"{ref}_title_ai.txt")
        df.at[idx, "description_ai_exists"] = 1 if file_status[0] else 0
        df.at[idx, "latest_description_ai_update"] = file_status[1]
    
    df = df.sort_values(["description_ai_exists", "origin_is_updated", "latest_description_ai_update", "has_origin"])
    df.to_csv(f"{CONF["data_path"]}/product_info.csv", index=False)
    
    
    df = df[df['has_origin'] == True]
    df = df.loc[(df['origin_is_updated'] == 0) | (df['description_ai_exists'] == 0)]

    
    # Iterate over DataFrame rows
    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        page_name: str = str(row['page_name'])
        
        # Check if 'ref' matches the expected value and continue if it doesn't
        
        # Construct the product description_ai file path
        path_products = f"{CONF['src_data_path']}/{page_name}/products"
        path_product_description_ai = f"{path_products}/{ref}_description_ai.txt"
        product_description_ai = read_file(path_product_description_ai)
        
        if (not product_description_ai):
            continue
        
        product_description_ai = "TITULO ANTIGO: " + row["title"] + "\n" + product_description_ai
        
        message(f"REQUEST - {control_data[today_str]["requests"]}")
        message(f"ref - {ref}")
        message(f"path - {path_product_description_ai}")
        path_product_title_ai = f"{path_products}/{ref}_title_ai.txt"
        path_product_flavor_ai = f"{path_products}/{ref}_flavor_ai.txt"
        product_title_ai, product_flavor_ai = refine_description_ai(product_description_ai, "asst_B04KA1YIRe8pTnfJP05u76hf")
        
        if (product_title_ai):
            message(f"{ref} - product_title_ai - OK")
            save_file_with_line_breaks(path_product_title_ai, product_title_ai)
            save_file_with_line_breaks(path_product_flavor_ai, product_flavor_ai)
            save_json(path_file_control, control_data)
            
        control_data[today_str]["requests"] += 1
        time.sleep(2)
        
        if control_data[today_str]["requests"] >= control_data[today_str]["limit"]:
            save_json(path_file_control, control_data)
            message(f"Daily limit of {control_data[today_str]['limit']} description_ais reached for {today_str}.")
            return
        exit()
    
def refine_description_ai(description_ai: str, assistant_id: str) -> Optional[Tuple[str, str]]:
    """
    Utiliza a API da OpenAI para gerar uma versão refinada da descrição do produto
    e faz uma segunda pergunta no mesmo chat.

    Args:
        description_ai (str): A descrição do produto a ser refinada.
        assistant_id (str): O ID do assistente a ser utilizado.

    Returns:
        Optional[Tuple[str, str]]: Um tuplo contendo as respostas do assistente.
    """
    try:
        # Configura o cliente da OpenAI
        client = openai.Client()

        # Cria um novo thread (apenas na primeira vez)
        thread = client.beta.threads.create()

        # Adiciona a descrição do produto como a primeira mensagem
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=description_ai
        )

        # Executa o assistente para gerar a primeira resposta (título refinado)
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Aguarda a conclusão da execução
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                raise Exception("A execução falhou.")
            time.sleep(1)  # Espera um pouco antes de verificar novamente

        # Obtém a primeira resposta do assistente
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_response = None
        for message_obj in messages.data[::-1]:
            if message_obj.role == "assistant":
                assistant_response = message_obj.content[0].text.value
                break

        if not assistant_response:
            raise Exception("Não foi possível obter a resposta do assistente.")

        # Agora, envia a segunda pergunta no mesmo thread
        second_question = "Quais sabores estão disponíveis?"

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=second_question
        )

        # Executa o assistente novamente para responder à segunda pergunta
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Aguarda a conclusão da execução
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                raise Exception("A execução falhou na segunda pergunta.")
            time.sleep(1)

        # Obtém a segunda resposta do assistente
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        second_response = None
        for message_obj in messages.data[::-1]:
            if message_obj.role == "assistant" and message_obj.content[0].text.value != assistant_response:
                second_response = message_obj.content[0].text.value
                break

        if not second_response:
            raise Exception("Não foi possível obter a resposta do assistente para a segunda pergunta.")

        # Retorna as respostas
        return assistant_response, second_response

    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        return None
