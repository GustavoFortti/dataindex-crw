import os
from copy import deepcopy
from typing import List, Tuple

import pandas as pd
from config.env import LOCAL
from elasticsearch import helpers
from shared.dataframe_functions import filter_dataframe_for_columns
from shared.elasticsearch_functions import (create_connection,
                                            create_documents_with_pandas,
                                            data_ingestion)
from shared.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from utils.general_functions import get_all_origins
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_search_def_",
    "wordlist": WORDLIST["supplement"],
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_search_def_",
    "all_data_path": f"{LOCAL}/data/supplement/brazil",
    "brand": False,
    "index_type": "supplement"
}

def promocoes(df):
    all_data_path = CONF['all_data_path']
    df_discount = pd.read_csv(f'{all_data_path}/_set_history_price_/history_price.csv')
    df_discount = df_discount[df_discount["price_discount_percent"] > 0]
    
    print(df_discount['ref'])

    # index = INDEX_SUPPLEMENT_BRAZIL['set']["promocoes"]
    # conf = deepcopy(CONF)
    # conf["index_name"] = index
    # data_ingestion(df_filtered, conf)

def whey_protein(df):
    keywords = wordlist["whey"]["subject"]
    barrinha = wordlist["barrinha"]["subject"]
    alfajor = wordlist["alfajor"]["subject"]
    wafer = wordlist["wafer"]["subject"]
    blacklist = ["combo", "kit"] + barrinha + alfajor + wafer
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["whey_protein"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def creatina(df):
    keywords = wordlist["creatina"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["creatina"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def proteinas(df):
    keywords = (wordlist["protein"]["subject"] + 
                 wordlist["whey"]["subject"] + 
                 wordlist["beef"]["subject"] + 
                 wordlist["albumina"]["subject"] + 
                 wordlist["soy"]["subject"] + 
                 wordlist["ervilha"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["proteinas"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def barrinhas_de_proteina(df):
    keywords = wordlist["barrinha"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["barrinhas_de_proteina"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def pre_treino(df):
    keywords = wordlist["pretreino"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["pre_treino"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def cafeina(df):
    keywords = wordlist["cafein"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["cafeina"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def energia(df):
    keywords = (wordlist["pretreino"]["subject"] + 
                wordlist["taurina"]["subject"] +
                wordlist["palatinose"]["subject"] +
                wordlist["cafein"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["energia"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def resistencia(df):
    keywords = (wordlist["bcaa"]["subject"] + 
                wordlist["betaalanina"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["resistencia"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def imunidade(df):
    keywords = (wordlist["glutamin"]["subject"] + 
                wordlist["propolis"]["subject"] +
                wordlist["curcuma"]["subject"] +
                wordlist["vitamina d"]["subject"] +
                wordlist["vitamina c"]["subject"] +
                wordlist["carnitin"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["imunidade"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def hipercalorico(df):
    keywords = wordlist["mass"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["hipercalorico"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def carboidratos(df):
    keywords = (wordlist["malto"]["subject"] + 
                wordlist["waxymaize"]["subject"] +
                wordlist["palatinose"]["subject"] +
                wordlist["dextrose"]["subject"] +
                wordlist["carboidrato"]["subject"])
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["carboidratos"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def beta_alanina(df):
    keywords = wordlist["betaalanina"]["subject"]
    beauty = wordlist["beauty"]["subject"]
    blacklist = ["combo", "kit"] + beauty
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["beta_alanina"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def termogenico(df):
    keywords = wordlist["termogenico"]["subject"] + wordlist["cafein"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["termogenico"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def oleos(df):
    keywords = (wordlist["cartamo"]["subject"] + 
                wordlist["oleo de coco"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["oleos"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def temperos(df):
    keywords = (wordlist["curcuma"]["subject"] + 
                wordlist["oleo de coco"]["subject"] + 
                wordlist["ketchup"]["subject"] + 
                wordlist["barbecue"]["subject"] + 
                wordlist["mostarda"]["subject"] + 
                wordlist["maionese"]["subject"] + 
                wordlist["tempero"]["subject"])
    blacklist = ["combo", "kit", "caps"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["temperos"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def adocantes(df):
    keywords = wordlist["xylitol"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["adocantes"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def pasta_de_amendoim(df):
    keywords = wordlist["peanut"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["pasta_de_amendoim"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def vegano(df):
    keywords = wordlist["veg"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["vegano"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def vegetariano(df):
    keywords = (wordlist["vegetarian"]["subject"] +
                wordlist["veg"]["subject"] + 
                wordlist["omega 3"]["subject"] + 
                wordlist["bcaa"]["subject"] + 
                wordlist["soy"]["subject"] + 
                 wordlist["ervilha"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["vegetariano"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def vitaminas(df):
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
    index = INDEX_SUPPLEMENT_BRAZIL['set']["vitaminas"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def minerais(df):
    keywords = (wordlist["calcio"]["subject"] + 
                wordlist["cromo"]["subject"] +
                wordlist["magnesio"]["subject"] +
                wordlist["zinco"]["subject"] +
                wordlist["selenio"]["subject"] +
                wordlist["carboidrato"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["minerais"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def sono(df):
    keywords = (wordlist["melatonina"]["subject"] + 
                wordlist["magnesio"]["subject"] +
                wordlist["triptofano"]["subject"])
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["sono"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def magnesio(df):
    keywords = wordlist["magnesio"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["magnesio"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def pele(df):
    keywords = wordlist["skin"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["pele"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def cabelo(df):
    keywords = wordlist["hair"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["cabelo"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def omega(df):
    keywords = wordlist["omega 3"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["omega"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def colageno(df):
    keywords = wordlist["colageno"]["subject"]
    blacklist = ["combo", "kit"]
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["colageno"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def combos(df):
    keywords = ["combo", "kit"]
    blacklist = []
    df_filtered = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    index = INDEX_SUPPLEMENT_BRAZIL['set']["combos"]
    conf = deepcopy(CONF)
    conf["index_name"] = index
    data_ingestion(df_filtered, conf)

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)
    
    global wordlist
    wordlist = WORDLIST["supplement"]
    df = get_all_origins(CONF['all_data_path'], "origin_csl.csv")
    df = df.drop_duplicates(subset='ref').reset_index(drop=True)
    
    message("exec - promocoes")
    promocoes(df)
    # message("exec - whey_protein")
    # whey_protein(df)
    # message("exec - creatina")
    # creatina(df)
    # message("exec - proteinas")
    # proteinas(df)
    # message("exec - barrinhas_de_proteina")
    # barrinhas_de_proteina(df)
    # message("exec - pre_treino")
    # pre_treino(df)
    # message("exec - cafeina")
    # cafeina(df)
    # message("exec - energia")
    # energia(df)
    # message("exec - resistencia")
    # resistencia(df)
    # message("exec - imunidade")
    # imunidade(df)
    # message("exec - hipercalorico")
    # hipercalorico(df)
    # message("exec - carboidratos")
    # carboidratos(df)
    # message("exec - beta_alanina")
    # beta_alanina(df)
    # message("exec - termogenico")
    # termogenico(df)
    # message("exec - oleos")
    # oleos(df)
    # message("exec - temperos")
    # temperos(df)
    # message("exec - adocantes")
    # adocantes(df)
    # message("exec - pasta_de_amendoim")
    # pasta_de_amendoim(df)
    # message("exec - vegano")
    # vegano(df)
    # message("exec - vegetariano")
    # vegetariano(df)
    # message("exec - vitaminas")
    # vitaminas(df)
    # message("exec - minerais")
    # minerais(df)
    # message("exec - sono")
    # sono(df)
    # message("exec - magnesio")
    # magnesio(df)
    # message("exec - pele")
    # pele(df)
    # message("exec - cabelo")
    # cabelo(df)
    # message("exec - omega")
    # omega(df)
    # message("exec - colageno")
    # colageno(df)
    # message("exec - combos")
    # combos(df)