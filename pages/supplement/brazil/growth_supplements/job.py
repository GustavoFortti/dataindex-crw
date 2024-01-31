from .extract import extract
from .dry import dry

from utils.wordlist import WORD_LIST
from utils.general_functions import create_directory_if_not_exists

from shared.ingestion import ingestion

CONF = {
    "name": "growth_supplements",
    "tipo_produto": "suplemento",
    "word_list": WORD_LIST["suplemento"],
    "marca": "growth supplements",
    "location_type_product": [{'tag': 'section', 'class': 'breadcrumb-produto'}],
    "data_path" : "./data/supplement/brazil/growth_supplements",
    "seed_path": "./pages/supplement/brazil/growth_supplements",
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