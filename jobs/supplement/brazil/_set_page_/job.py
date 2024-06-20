import importlib

from config.env import LOCAL
from lib.elasticsearch.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from lib.ingestion import ingestion
from lib.extract import extract
from utils.log import message
from utils.general_functions import create_directory_if_not_exists
from utils.wordlist import PRONOUNS, WORDLIST

CONF = {
    "wordlist": WORDLIST["supplement"],
    "pronouns": PRONOUNS["brazil"],
    "product_def_path": f"{LOCAL}/data/supplement/brazil/_set_product_def_",
    "src_data_path": f"{LOCAL}/data/supplement/brazil",
    "index_name": INDEX_SUPPLEMENT_BRAZIL["index"]["product"],
    "index_type": INDEX_SUPPLEMENT_BRAZIL["type"]
}

def run(args):
    job_name = args.job_name
    page_name = args.page_name
    page_type = args.page_type
    country = args.country
    
    message(f"JOB NAME: {job_name}")
    message(f"PAGE NAME: {page_name}")
    
    module_name = f"jobs.{page_type}.{country}.pages.{page_name}.conf"
    page_conf = importlib.import_module(module_name)
    
    CONF["name"] = page_conf.JOB_NAME
    CONF["brand"] = page_conf.BRAND
    CONF["url"] = page_conf.URL
    CONF["product_definition_tag"] = page_conf.PRODUCT_DEFINITION_TAG
    CONF["dynamic_scroll"] = page_conf.DYNAMIC_SCROLL
    CONF["data_path"] = f"{LOCAL}/data/supplement/brazil/{page_conf.JOB_NAME}"
    CONF["seed_path"] = f"{LOCAL}/jobs/supplement/brazil/pages/{page_conf.JOB_NAME}"
    CONF.update(args.__dict__)

    job_type = CONF["job_type"]
    page_type = CONF["page_type"]
    message(f"JOB_TYPE: {job_type}")
    message(f"PAGE_TYPE: {page_type}")
    create_directory_if_not_exists(CONF['data_path'])

    module_name = f"jobs.{page_type}.{country}.pages.{page_name}.dry"
    dry = importlib.import_module(module_name)
    
    options = {
        "extract": extract,
        "dry": dry.dry,
        "ingestion": ingestion
    }
    
    exec_function = options.get(job_type)
    if (exec_function):
        exec_function(CONF)