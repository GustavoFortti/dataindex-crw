import os

import pandas as pd
from elasticsearch import helpers

from config.env import LOCAL
from shared.elasticsearch_functions import (create_connection,
                                            create_documents_with_pandas)
from shared.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_carousel_",
}

def filter_dataframe_for_columns(df, columns, keywords, blacklist=None):
    # Inicializa uma máscara global com False para todos os registros
    global_mask = pd.Series([False] * len(df), index=df.index)
    
    for col in columns:
        # Converte a coluna para string e substitui valores nulos por string vazia
        df[col] = df[col].astype(str).fillna('')
        # Atualiza a máscara global para incluir registros que contêm as palavras-chave
        global_mask |= df[col].str.contains('|'.join(keywords), case=False)
    
    # Aplica a máscara global para filtrar as linhas com palavras-chave
    filtered_df = df[global_mask]
    
    # Se uma blacklist é fornecida, aplica a blacklist para remover linhas indesejadas
    if blacklist:
        for col in columns:
            # Cria uma máscara para excluir linhas com substrings da blacklist
            blacklist_mask = ~filtered_df[col].str.contains('|'.join(blacklist), case=False)
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

def promocoes(es, df):
    keywords = wordlist["pretreino"]["subject"]
    blacklist = ""
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["promocoes"]
    # elasticsearch_ingestion(es, index, df_filtered)

def whey_protein(es, df):
    keywords = wordlist["whey"]["subject"]
    barrinha = wordlist["barrinha"]["subject"]
    alfajor = wordlist["alfajor"]["subject"]
    wafer = wordlist["wafer"]["subject"]
    blacklist = ["combo", "kit"] + barrinha + alfajor + wafer
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["whey_protein"]
    # elasticsearch_ingestion(es, index, df_filtered)

def creatina(es, df):
    keywords = wordlist["creatina"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["creatina"]
    # elasticsearch_ingestion(es, index, df_filtered)

def proteinas(es, df):
    keywords = (wordlist["protein"]["subject"] + 
                 wordlist["whey"]["subject"] + 
                 wordlist["carn"]["subject"] + 
                 wordlist["albumina"]["subject"] + 
                 wordlist["soy"]["subject"] + 
                 wordlist["ervilha"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["proteinas"]
    # elasticsearch_ingestion(es, index, df_filtered)

def barrinhas_de_proteina(es, df):
    keywords = wordlist["barrinha"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["barrinhas_de_proteina"]
    # elasticsearch_ingestion(es, index, df_filtered)

def pre_treino(es, df):
    keywords = wordlist["pretreino"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["pre_treino"]
    # elasticsearch_ingestion(es, index, df_filtered)

def cafeina(es, df):
    keywords = wordlist["cafein"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["cafeina"]
    # elasticsearch_ingestion(es, index, df_filtered)

def energia(es, df):
    keywords = (wordlist["pretreino"]["subject"] + 
                wordlist["taurina"]["subject"] +
                wordlist["palatinose"]["subject"] +
                wordlist["cafein"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["energia"]
    # elasticsearch_ingestion(es, index, df_filtered)

def resistencia(es, df):
    keywords = (wordlist["bcaa"]["subject"] + 
                wordlist["betaalanina"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["resistencia"]
    # elasticsearch_ingestion(es, index, df_filtered)

def imunidade(es, df):
    keywords = (wordlist["glutamin"]["subject"] + 
                wordlist["propolis"]["subject"] +
                wordlist["curcuma"]["subject"] +
                wordlist["vitamina d"]["subject"] +
                wordlist["vitamina c"]["subject"] +
                wordlist["carnitin"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["imunidade"]
    # elasticsearch_ingestion(es, index, df_filtered)

def hipercalorico(es, df):
    keywords = wordlist["hipercalorico"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["hipercalorico"]
    # elasticsearch_ingestion(es, index, df_filtered)

def carboidratos(es, df):
    keywords = (wordlist["malto"]["subject"] + 
                wordlist["waxymaize"]["subject"] +
                wordlist["palatinose"]["subject"] +
                wordlist["dextrose"]["subject"] +
                wordlist["carboidrato"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["carboidratos"]
    # elasticsearch_ingestion(es, index, df_filtered)

def beta_alanina(es, df):
    keywords = wordlist["betaalanina"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["beta_alanina"]
    # elasticsearch_ingestion(es, index, df_filtered)

def termogenico(es, df):
    keywords = wordlist["termogenico"]["subject"] + wordlist["cafein"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["termogenico"]
    # elasticsearch_ingestion(es, index, df_filtered)

def oleos(es, df):
    keywords = (wordlist["cartamo"]["subject"] + 
                ["oleo de coco"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["oleos"]
    # elasticsearch_ingestion(es, index, df_filtered)

def temperos(es, df):
    keywords = (wordlist["curcuma"]["subject"] + 
                wordlist["tempero"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["temperos"]
    # elasticsearch_ingestion(es, index, df_filtered)

def adocantes(es, df):
    keywords = wordlist["xylitol"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["adocantes"]
    # elasticsearch_ingestion(es, index, df_filtered)

def pasta_de_amendoim(es, df):
    keywords = wordlist["peanut"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["pasta_de_amendoim"]
    # elasticsearch_ingestion(es, index, df_filtered)

def vegano(es, df):
    keywords = wordlist["veg"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["vegano"]
    # elasticsearch_ingestion(es, index, df_filtered)

def vegetariano(es, df):
    keywords = wordlist["vegetarian"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["vegetariano"]
    # elasticsearch_ingestion(es, index, df_filtered)

def vitaminas(es, df):
    keywords = (wordlist["vitamina"]["subject"] + 
                wordlist["vitamina a"]["subject"] +
                wordlist["vitamina b1"]["subject"] +
                wordlist["vitamina b10"]["subject"] +
                wordlist["vitamina b11"]["subject"] +
                wordlist["vitamina b12"]["subject"] +
                wordlist["vitamina b13"]["subject"] +
                wordlist["vitamina b15"]["subject"] +
                wordlist["vitamina b17"]["subject"] +
                wordlist["vitamina b2"]["subject"] +
                wordlist["vitamina b22"]["subject"] +
                wordlist["vitamina b3"]["subject"] +
                wordlist["vitamina b4"]["subject"] +
                wordlist["vitamina b5"]["subject"] +
                wordlist["vitamina b6"]["subject"] +
                wordlist["vitamina b7"]["subject"] +
                wordlist["vitamina b8"]["subject"] +
                wordlist["vitamina b9"]["subject"] +
                wordlist["vitamina c"]["subject"] +
                wordlist["vitamina d"]["subject"] +
                wordlist["vitamina e"]["subject"] +
                wordlist["vitamina f"]["subject"] +
                wordlist["vitamina g"]["subject"] +
                wordlist["vitamina h"]["subject"] +
                wordlist["vitamina j"]["subject"] +
                wordlist["vitamina k"]["subject"] +
                wordlist["vitamina k1"]["subject"] +
                wordlist["vitamina k2"]["subject"] +
                wordlist["vitamina k7"]["subject"] +
                wordlist["vitamina l"]["subject"] +
                wordlist["vitamina l1"]["subject"] +
                wordlist["vitamina l2"]["subject"] +
                wordlist["vitamina m"]["subject"] +
                wordlist["vitamina n"]["subject"] +
                wordlist["vitamina o"]["subject"] +
                wordlist["vitamina p"]["subject"] +
                wordlist["vitamina q"]["subject"] +
                wordlist["vitamina r"]["subject"] +
                wordlist["vitamina s"]["subject"] +
                wordlist["vitamina t"]["subject"] +
                wordlist["vitamina w"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["vitaminas"]
    # elasticsearch_ingestion(es, index, df_filtered)

def minerais(es, df):
    keywords = (wordlist["calcio"]["subject"] + 
                wordlist["cromo"]["subject"] +
                wordlist["magnesio"]["subject"] +
                wordlist["zinco"]["subject"] +
                wordlist["selenio"]["subject"] +
                wordlist["carboidrato"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["minerais"]
    # elasticsearch_ingestion(es, index, df_filtered)

def sono(es, df):
    keywords = (wordlist["melatonina"]["subject"] + 
                wordlist["magnesio"]["subject"] +
                wordlist["triptofano"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["sono"]
    # elasticsearch_ingestion(es, index, df_filtered)

def magnesio(es, df):
    keywords = wordlist["magnesio"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["magnesio"]
    # elasticsearch_ingestion(es, index, df_filtered)

def pele(es, df):
    keywords = wordlist["skin"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["pele"]
    # elasticsearch_ingestion(es, index, df_filtered)

def cabelo(es, df):
    keywords = wordlist["hair"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["cabelo"]
    # elasticsearch_ingestion(es, index, df_filtered)

def omega(es, df):
    keywords = wordlist["omega 3"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["omega"]
    # elasticsearch_ingestion(es, index, df_filtered)

def colageno(es, df):
    keywords = wordlist["colageno"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["colageno"]
    # elasticsearch_ingestion(es, index, df_filtered)

def combos(es, df):
    keywords = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL["combos"]
    # elasticsearch_ingestion(es, index, df_filtered)

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)
    
    global wordlist
    wordlist = WORDLIST["supplement"]
    es = create_connection()
    df = ""
    
    message("exec - promocoes")
    promocoes(es, df)
    message("exec - whey_protein")
    whey_protein(es, df)
    message("exec - creatina")
    creatina(es, df)
    message("exec - proteinas")
    proteinas(es, df)
    message("exec - barrinhas_de_proteina")
    barrinhas_de_proteina(es, df)
    message("exec - pre_treino")
    pre_treino(es, df)
    message("exec - cafeina")
    cafeina(es, df)
    message("exec - energia")
    energia(es, df)
    message("exec - resistencia")
    resistencia(es, df)
    message("exec - imunidade")
    imunidade(es, df)
    message("exec - hipercalorico")
    hipercalorico(es, df)
    message("exec - carboidratos")
    carboidratos(es, df)
    message("exec - beta_alanina")
    beta_alanina(es, df)
    message("exec - termogenico")
    termogenico(es, df)
    message("exec - oleos")
    oleos(es, df)
    message("exec - temperos")
    temperos(es, df)
    message("exec - adocantes")
    adocantes(es, df)
    message("exec - pasta_de_amendoim")
    pasta_de_amendoim(es, df)
    message("exec - vegano")
    vegano(es, df)
    message("exec - vegetariano")
    vegetariano(es, df)
    message("exec - vitaminas")
    vitaminas(es, df)
    message("exec - minerais")
    minerais(es, df)
    message("exec - sono")
    sono(es, df)
    message("exec - magnesio")
    magnesio(es, df)
    message("exec - pele")
    pele(es, df)
    message("exec - cabelo")
    cabelo(es, df)
    message("exec - omega")
    omega(es, df)
    message("exec - colageno")
    colageno(es, df)
    message("exec - combos")
    combos(es, df)