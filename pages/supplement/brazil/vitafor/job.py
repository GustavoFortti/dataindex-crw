from config.env import LOCAL

from .extract import extract
from .dry import dry

from utils.wordlist import WORD_LIST
from utils.general_functions import create_directory_if_not_exists

from shared.ingestion import ingestion

CONF = {
    "name": "vitafor",
    "word_list": WORD_LIST["supplement"],
    "brand": "vitafor",
    "product_desc_tag_loc": [{'tag': 'p', 'class': 'vitafor-store-theme-7-x-productPageShortDescription'}],
    "data_path" : f"{LOCAL}/data/supplement/brazil/vitafor",
    "seed_path": f"{LOCAL}/pages/supplement/brazil/vitafor",
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