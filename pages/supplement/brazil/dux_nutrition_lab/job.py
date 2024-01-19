from .extract import extract
from .dry import dry
from shared.elastic_funcions import ingestion
from utils.wordlist import WORD_LIST
from utils.dry_functions import create_directory_if_not_exists

CONF = {
    "name": "dux_nutrition_lab",
    "tipo_produto": "suplemento",
    "word_list": WORD_LIST["suplemento"],
    "marca": "dux nutrition lab",
    "location_type_product": [{'tag': 'div', 'class': 'duxnutrition-product-0-x-basic-description'}],
    "data_path" : "./data/supplement/brazil/dux_nutrition_lab",
    "seed_path": "./pages/supplement/brazil/dux_nutrition_lab",
    "index_name": "brazil_supplement"
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF["option"] = args.option

    job_type = args.job_type
    print(" - EXEC: " + job_type)
    
    options = {"extract": extract,
                "dry": dry,
                "ingestion": ingestion}
    
    exec = options.get(job_type)
    exec(CONF)