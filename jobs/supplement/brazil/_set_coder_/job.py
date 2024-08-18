import importlib

from config.env import LOCAL
from lib.crawler import crawler
from utils.log import message

CONF = {
    "name": "_set_coder_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_coder_",
    "src_data_path": f"{LOCAL}/data/supplement/brazil",
    "pages_path": f"{LOCAL}/jobs/supplement/brazil/pages",
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
    CONF["product_definition_tag_map"] = page_conf.PRODUCT_DEFINITION_TAG_MAP
    CONF["dynamic_scroll"] = page_conf.DYNAMIC_SCROLL
    CONF["data_path"] = f"{LOCAL}/data/supplement/brazil/{page_conf.JOB_NAME}"
    CONF["seed_path"] = f"{LOCAL}/jobs/supplement/brazil/pages/{page_conf.JOB_NAME}"
    CONF.update(args.__dict__)

    job_type = CONF["job_type"]
    page_type = CONF["page_type"]
    message(f"JOB_TYPE: {job_type}")
    message(f"PAGE_TYPE: {page_type}")
    
def update():
    pass