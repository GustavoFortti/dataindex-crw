import importlib

from config.env import LOCAL
from utils.log import message
from utils.general_functions import create_directory_if_not_exists

CONF = {
    "product_def_path": f"{LOCAL}/data/cuts/all/_set_product_def_",
    "src_data_path": f"{LOCAL}/data/cuts/all",
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
    CONF["dynamic_scroll"] = page_conf.DYNAMIC_SCROLL
    CONF["data_path"] = f"{LOCAL}/data/cuts/all/{page_conf.JOB_NAME}"
    CONF["seed_path"] = f"{LOCAL}/jobs/cuts/all/pages/{page_conf.JOB_NAME}"
    CONF.update(args.__dict__)

    job_type = CONF["job_type"]
    page_type = CONF["page_type"]
    message(f"JOB_TYPE: {job_type}")
    message(f"PAGE_TYPE: {page_type}")
    create_directory_if_not_exists(CONF['data_path'])

    module_name = f"jobs.{page_type}.{country}.pages.{page_name}.extract"
    extract = importlib.import_module(module_name)
    
    options = {
        "extract": extract.extract,
    }
    
    exec_function = options.get(job_type)
    if (exec_function):
        exec_function(CONF)