from .extract import extract
from .dry import dry
from shared.elastic_funcions import ingestion
from utils.wordlist import WORD_LIST

CONF = {
    "name": "black_skull",
    "tipo_produto": "suplemento",
    "word_list": WORD_LIST["suplemento"],
    "marca": "black skull",
    "location_type_product": [{'tag': 'div', 'class': 'vtex-breadcrumb-1-x-container'}],
    "data_path" : "./pages/black_skull/data",
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