from config.env import LOCAL
from lib.dataframe_functions import (filter_dataframe_for_columns,
                                     read_and_stack_csvs_dataframes)
from lib.elasticsearch.elasticsearch_functions import data_ingestion
from lib.elasticsearch.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from lib.set_functions import get_pages_with_status_true
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_carousel_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_carousel_",
    "src_data_path": f"{LOCAL}/data/supplement/brazil",
    "pages_path": f"{LOCAL}/jobs/supplement/brazil/pages",
    "wordlist": WORDLIST["supplement"],
    "index_name": "",
    "index_type": INDEX_SUPPLEMENT_BRAZIL['type'],
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)
    
    global WORDLIST
    WORDLIST = WORDLIST["supplement"]
    src_data_path = CONF["src_data_path"]

    pages_with_status_true = get_pages_with_status_true(CONF)
    df = read_and_stack_csvs_dataframes(src_data_path, pages_with_status_true, "origin_csl.csv")
    df = df.drop_duplicates(subset='ref').reset_index(drop=True)

    message("set whey")
    keywords = WORDLIST["whey"]["subject"]
    barrinha = WORDLIST["barrinha"]["subject"]
    alfajor = WORDLIST["alfajor"]["subject"]
    wafer = WORDLIST["wafer"]["subject"]
    blacklist = ["combo", "pack", "kit"] + barrinha + alfajor + wafer

    df_whey = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_whey = df_whey.sample(18)
    print(df_whey)
    CONF["index_name"] = INDEX_SUPPLEMENT_BRAZIL["index"]["whey"]
    data_ingestion(df, CONF)

    message("set barrinha")
    keywords = WORDLIST["barrinha"]["subject"]
    blacklist = ["combo", "pack", "kit"]

    df_barrinha = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_barrinha = df_barrinha.sample(18)
    print(df_barrinha)
    CONF["index_name"] = INDEX_SUPPLEMENT_BRAZIL["index"]["bar"]
    data_ingestion(df, CONF)

    message("set pretreino")
    keywords = WORDLIST["pretreino"]["subject"]
    beauty = WORDLIST["beauty"]["subject"]
    blacklist = ["combo", "pack", "kit", "brain"] + beauty

    df_pretreino = filter_dataframe_for_columns(df, ["title", "product_def", "product_def_pred"], keywords, blacklist)
    df_pretreino = df_pretreino.sample(18)
    print(df_pretreino)
    CONF["index_name"] = INDEX_SUPPLEMENT_BRAZIL["index"]["preworkout"]
    data_ingestion(df, CONF)