from .extract import extract
from .dry import dry
from shared.elastic_funcions import ingestion
from utils.wordlist import WORD_LIST
from utils.general_functions import create_directory_if_not_exists

CONF = {
    "name": "boldsnacks",
    "tipo_produto": "suplemento",
    "word_list": WORD_LIST["suplemento"],
    "marca": "bold snacks",
    "location_type_product": [{'tag': 'div', 'class': 'product__description'}],
    "data_path" : "./data/supplement/brazil/boldsnacks",
    "seed_path": "./pages/supplement/brazil/boldsnacks",
    "index_name": "brazil_supplement"
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