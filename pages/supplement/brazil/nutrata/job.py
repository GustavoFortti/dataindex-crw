from .extract import extract
from .dry import dry

from utils.wordlist import WORD_LIST
from utils.general_functions import create_directory_if_not_exists

from shared.ingestion import ingestion

CONF = {
    "name": "nutrata",
    "tipo_produto": "suplemento",
    "word_list": WORD_LIST["suplemento"],
    "marca": "nutrata",
    "location_type_product": [{'tag': 'span', 'class': 'tagged_as'}, {'tag': 'nav', 'class': 'woocommerce-breadcrumb'}, {'tag': 'div', 'class': 'woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab'}],
    "data_path" : "./data/supplement/brazil/nutrata",
    "seed_path": "./pages/supplement/brazil/nutrata",
    "index_name": "brazil_supplement",
    "index_type": "supplement"
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF["option"] = args.option

    job_type = args.job_type
    print(" - EXEC: " + job_type)
    create_directory_if_not_exists(CONF['data_path'])

    options = {"extract": extract,
                "dry": dry,
                "ingestion": ingestion}
    
    exec = options.get(job_type)
    exec(CONF)