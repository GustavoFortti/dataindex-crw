from config.env import LOCAL

from .extract import extract
from .dry import dry
from .vars import PRODUCT_DESC_TAG, DYNAMIC_SCROLL

from utils.wordlist import WORD_LIST
from utils.general_functions import create_directory_if_not_exists

from shared.ingestion import ingestion

CONF = {
    "name": "integralmedica",
    "word_list": WORD_LIST["supplement"],
    "brand": "integralmedica",
    "product_desc_tag": PRODUCT_DESC_TAG,
    "dynamic_scroll": DYNAMIC_SCROLL,
    "data_path" : f"{LOCAL}/data/supplement/brazil/integralmedica",
    "seed_path": f"{LOCAL}/pages/supplement/brazil/integralmedica",
    "index_name": "brazil_supplement",
    "index_type": "supplement"
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)
    create_directory_if_not_exists(CONF['data_path'])

    options = {"extract": extract,
                "dry": dry,
                "ingestion": ingestion}
    
    exec = options.get(job_type)
    exec(CONF)