from config.env import LOCAL

from .extract import extract
from .dry import dry
from .vars import (
    PRODUCT_DESC_TAG, 
    DYNAMIC_SCROLL, 
    JOB_NAME, 
    BRAND
)

from utils.wordlist import WORDLIST
from utils.general_functions import create_directory_if_not_exists

from shared.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from shared.ingestion import ingestion

conf = {
    "name": JOB_NAME,
    "wordlist": WORDLIST["supplement"],
    "brand": BRAND,
    "product_desc_tag": PRODUCT_DESC_TAG,
    "dynamic_scroll": DYNAMIC_SCROLL,
    "data_path": f"{LOCAL}/data/supplement/brazil/{JOB_NAME}",
    "seed_path": f"{LOCAL}/pages/supplement/brazil/{JOB_NAME}",
    "index_name": INDEX_SUPPLEMENT_BRAZIL["index"],
    "index_type": INDEX_SUPPLEMENT_BRAZIL["type"]
}

def run(args):
    print(f"JOB_NAME: {conf['name']}", end="")
    conf.update(vars(args))

    job_type = conf["job_type"]
    print(f" - EXEC: {job_type}")
    create_directory_if_not_exists(conf['data_path'])

    options = {
        "extract": extract,
        "dry": dry,
        "ingestion": ingestion
    }
    
    exec_function = options.get(job_type)
    if (exec_function):
        exec_function(conf)
