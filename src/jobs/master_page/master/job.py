import importlib
import os

from src.lib.utils.file_system import create_directory_if_not_exists, path_exists
from src.lib.utils.log import message
from src.lib.extract.extract import extract
from src.lib.load.load import load
from src.lib.wordlist.wordlist import WORDLIST
from src.lib.wordlist.wordlist_flavor import WORDLIST_FLAVOR
from src.lib.wordlist.wordlist_format import WORDLIST_FORMAT

def set_conf(args, local):
    conf = {}
    conf["local"] = local
    conf["job_name"] = args.job_name
    conf["page_name"] = args.page_name
    conf["page_type"] = args.page_type
    conf["country"] = args.country
    conf["src_data_path"] = f"{local}/data/{conf['page_type']}/{conf['country']}"
    conf["wordlist"] = WORDLIST[conf['page_type']]
    conf["wordlist_flavor"] = WORDLIST_FLAVOR
    conf["wordlist_format"] = WORDLIST_FORMAT
    return conf

def update_conf_with_page_config(conf, page_conf, local, args):
    conf["name"] = page_conf.JOB_NAME
    conf["brand"] = page_conf.BRAND
    conf["url"] = page_conf.URL
    conf["product_definition_tag_map"] = page_conf.PRODUCT_DEFINITION_TAG_MAP
    conf["product_description_tag_map"] = page_conf.PRODUCT_DESCRIPTION_TAG_MAP
    conf["product_nutricional_table_tag_map"] = page_conf.PRODUCT_NUTRICIONAL_TABLE_TAG_MAP
    conf["tag_map_preference"] = page_conf.TAG_MAP_PREFERENCE
    conf["dynamic_scroll"] = page_conf.DYNAMIC_SCROLL
    conf["user_agent"] = page_conf.USER_AGENT
    conf["cupom_code"] = page_conf.CUPOM_CODE
    conf["discount_percent_cupom"] = page_conf.DISCOUNT_PERCENT_CUPOM
    conf["tail_platform_link"] = page_conf.TAIL_PLATFORM_LINK
    conf["data_path"] = f"{conf['src_data_path']}/{page_conf.JOB_NAME}"
    conf["control_products_update"] = f"{conf["data_path"]}/_products_update_success_"
    conf["control_products_metadata_update"] = f"{conf["data_path"]}/_products_metadata_update_success_"
    conf["control_products_metadata_update_old_pages"] = f"{conf["data_path"]}/_products_metadata_update_old_pages_success_"
    conf["seed_path"] = f"{local}/src/jobs/slave_page/pages/{conf['country']}/{page_conf.JOB_NAME}"
    conf["product_definition"] = f"{local}/data/{conf['page_type']}/brazil/product_definition"
    conf["scroll_page"] = True
    conf["status_job"] = False
    conf["products_update"] = False
    conf["products_metadata_update"] = False
    
    create_directory_if_not_exists(conf['data_path'] + "/products")
    conf.update(vars(args))
    
    conf["path_products_extract_csl"] = os.path.join(conf['data_path'], "products_extract_csl.csv")
    conf["path_products_extract_temp"] = os.path.join(conf['data_path'], "products_extract_temp.csv")
    conf["path_products_transform_csl"] = os.path.join(conf['data_path'], "products_transform_csl.csv")
    conf["path_products_metadata_transform"] = os.path.join(conf['data_path'], "products_metadata_transform.csv")
    
    if ((not path_exists(conf["path_products_extract_csl"])) & (conf["exec_flag"] != "status_job")):
        conf["exec_flag"] = "new_page"
        
    return conf

def run(args):
    message("INICIANDO O JOB")
    
    local = os.getenv('LOCAL')
    conf = set_conf(args, local)
    
    module_name = f"src.jobs.slave_page.pages.{conf['country']}.{conf['page_name']}.conf"
    page_conf = importlib.import_module(module_name)
    
    conf = update_conf_with_page_config(conf, page_conf, local, args)

    module_name = f"src.jobs.slave_page.pages.{conf['country']}.{conf['page_name']}.dry"
    dry = importlib.import_module(module_name)
    
    options = {
        "extract": extract,
        "transform": dry.dry,
        "load": load
    }
    
    exec_function = options.get(conf["exec_type"])
    if (exec_function):
        exec_function(conf)