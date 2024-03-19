from config.env import LOCAL
from utils.wordlist import WORDLIST
from utils.log import message

import os
import pandas as pd
from elasticsearch import helpers
from shared.elasticsearch_functions import create_connection, create_documents_with_pandas
from shared.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL

CONF = {
    "name": "_set_carousel_",
}

def filter_dataframe_for_columns(df, columns, keywords, blacklist=None):
    # Inicializa uma máscara global com False para todos os registros
    global_mask = pd.Series([False] * len(df), index=df.index)
    
    for col in columns:
        # Atualiza a máscara global para incluir registros que contêm as palavras-chave
        global_mask |= df[col].str.contains('|'.join(keywords), case=False, na=False)
    
    # Aplica a máscara global para filtrar as linhas com palavras-chave
    filtered_df = df[global_mask]
    
    # Se uma blacklist é fornecida, aplica a blacklist para remover linhas indesejadas
    if blacklist:
        for col in columns:
            # Cria uma máscara para excluir linhas com substrings da blacklist
            blacklist_mask = ~filtered_df[col].str.contains('|'.join(blacklist), case=False, na=False)
            # Aplica a máscara da blacklist
            filtered_df = filtered_df[blacklist_mask]
    
    # Remove linhas duplicadas do resultado final
    filtered_df = filtered_df.drop_duplicates().reset_index(drop=True)
    
    return filtered_df


def get_all_origins():
    diretorio_inicial = f'{LOCAL}/data/supplement/brazil'
    nome_arquivo = 'origin_csl.csv'

    dataframes = []

    # Percorre recursivamente o diretório e seus subdiretórios
    for pasta_raiz, _, arquivos in os.walk(diretorio_inicial):
        for nome_arquivo_encontrado in arquivos:
            if nome_arquivo_encontrado == nome_arquivo:
                caminho_completo = os.path.join(pasta_raiz, nome_arquivo_encontrado)
                df = pd.read_csv(caminho_completo)
                dataframes.append(df)

    # Una todos os DataFrames em um único DataFrame
    df = pd.concat(dataframes, ignore_index=True)
    return df

def create_index(es, indice_elasticsearch):
    if not es.indices.exists(index=indice_elasticsearch):
        es.indices.create(index=indice_elasticsearch)
        print(f"Index '{indice_elasticsearch}' created.")
    else:
        print(f"Index '{indice_elasticsearch}' exists.")

def elasticsearch_ingestion(es, indice_elasticsearch, df):
    create_index(es, indice_elasticsearch)
    es.delete_by_query(index=indice_elasticsearch, body={"query": {"match_all": {}}})
    success, errors = helpers.bulk(es, create_documents_with_pandas(df, indice_elasticsearch))
    print(success, errors)

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)

    es = create_connection()
    
    df = get_all_origins()
    df = df.drop_duplicates(subset='ref').reset_index(drop=True)

    wordlist = WORDLIST["supplement"]

    message("set whey")
    keywords = wordlist["whey"]["subject"]
    barrinha = wordlist["barrinha"]["subject"]
    alfajor = wordlist["alfajor"]["subject"]
    wafer = wordlist["wafer"]["subject"]
    blacklist = ["combo", "pack", "kit"] + barrinha + alfajor + wafer

    df_whey = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_whey = df_whey.sample(18)
    print(df_whey)
    elasticsearch_ingestion(es, INDEX_SUPPLEMENT_BRAZIL["set"]["whey"], df_whey)

    message("set barrinha")
    keywords = wordlist["barrinha"]["subject"]
    blacklist = ["combo", "pack", "kit"]

    df_barrinha = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_barrinha = df_barrinha.sample(18)
    print(df_barrinha)
    elasticsearch_ingestion(es, INDEX_SUPPLEMENT_BRAZIL["set"]["bar"], df_barrinha)

    message("set pretreino")
    keywords = wordlist["pretreino"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "pack", "kit", "brain"] + beauty

    df_pretreino = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_pretreino = df_pretreino.sample(18)
    print(df_pretreino)
    elasticsearch_ingestion(es, INDEX_SUPPLEMENT_BRAZIL["set"]["preworkout"], df_pretreino)