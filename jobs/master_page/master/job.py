import importlib

from config.env import LOCAL
from utils.log import message

CONF = {}

def set_conf(args):
    CONF["job_name"] = args.job_name
    CONF["page_name"] = args.page_name
    CONF["page_type"] = args.page_type
    CONF["country"] = args.country
    CONF["src_data_path"] = f"{LOCAL}/data/{CONF["page_type"]}/{CONF["country"]}"

def run(args):
    message(f"START JOB")
    set_conf(args)
    
    message(CONF, is_json=True)
    
    module_name = f"jobs.{CONF["page_type"]}.{CONF["country"]}.pages.{CONF["page_name"]}.conf"
    page_conf = importlib.import_module(module_name)
    
    CONF["brand"] = page_conf.BRAND
    CONF["url"] = page_conf.URL
    CONF["product_definition_tag_map"] = page_conf.PRODUCT_DEFINITION_TAG_MAP
    CONF["dynamic_scroll"] = page_conf.DYNAMIC_SCROLL
    CONF["data_path"] = f"{CONF["src_data_path"]}/{page_conf.JOB_NAME}"
    CONF["seed_path"] = f"{LOCAL}/jobs/slave_page/pages/{CONF["country"]}/{page_conf.JOB_NAME}"
    CONF.update(args.__dict__)
    
    message("UPDATE CONF")
    message(CONF, is_json=True)
    
    
    exit()
    