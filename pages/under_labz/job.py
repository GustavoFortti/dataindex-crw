from .extract import extract
from .dry import dry
from shared.elastic_funcions import ingestion
from utils.wordlist import WORD_LIST

CONF = {
    "name": "under_labz",
    "tipo_produto": "suplemento",
    "word_list": WORD_LIST["suplemento"],
    "marca": "under labz",
    "location_type_product": [{'tag': 'div', 'class': 'breadcrumbs'}, {'tag': 'p', 'class': 'western'}, {'tag': 'div', 'class': 'tab-pane active'}],
    "data_path" : "./pages/under_labz/data",
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